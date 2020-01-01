import requests
import pandas as pd
from bs4 import BeautifulSoup

nylist = pd.DataFrame()

for the_year in range(2019, 2020):
    for the_month in range(1, 13):

        url = 'https://www.nytimes.com/books/best-sellers/{0}/{1}/01/business-books/'.format(the_year, str(the_month).zfill(2))
        page = requests.get(url)
        print(" --  try: {0}, {1} -- ".format(the_year, str(the_month).zfill(2)))

        if page.status_code != 200:
            print(" --  Unable to Process: {0}, {1} -- ".format(the_year, str(the_month).zfill(2)))
            continue

        soup = BeautifulSoup(page.text, 'html.parser')
        top_list = soup.findAll('ol',{'class':'css-12yzwg4'})
        books = top_list[0].findAll('li', {'class': 'css-13y32ub'})
        print("Processing: Year: {0}, Month: {1}, No of Books {2}".format(the_year, the_month, len(books)))

        for i in range(len(books)):
            book = books[i].contents[0]
            title = book.find('h3',{'class': 'css-5pe77f'}).text
            author = book.find("p", {"class": "css-hjukut"}).text.split('by ')[1]
            review =  book.find('a', href=True)['href']
            #print("{0}, {1}; review: {2}".format(title, author, review))
            one_item = pd.Series([title,author, int(the_year),the_month,review], index=['Title', 'Author','Year', 'Month',  'Review'])
            nylist = nylist.append(one_item, ignore_index=True, sort=False)

nylist.drop_duplicates(subset='Title', inplace = True)
col_index = ['Title', 'Author','Year', 'Month',  'Review']
nylist = nylist.reindex(columns=col_index)

nylist.to_csv("nylist.csv", index=False)

