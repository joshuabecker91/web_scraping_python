import requests
from bs4 import BeautifulSoup
import csv
# pip install beautifulsoup4
# https://developers.whatismybrowser.com/useragents/parse/?ae=y#parse-useragent use this to identify your browser for user agent

# ---------------------------------------------------------------------------------------------------------------------------------
baseurl = 'https://www.thewhiskyexchange.com'

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

# loop through each page and scrape the url for each item -------------------------------------------------------------------------
product_links = []
for x in range(1,6):
    r = requests.get(f'https://www.thewhiskyexchange.com/c/639/bourbon-whiskey?pg={x}')
    soup = BeautifulSoup(r.content, 'lxml') #lxml is the default for bs4 but can use html
    product_list = soup.find_all('li', attrs={'class':'product-grid__item'})
    print(product_list)
    for item in product_list:
        for link in item.find_all('a', href=True):
            print(link['href'])
            product_links.append(baseurl + link['href'])

# print(len(product_links))
print(product_links)


# itterate through each url, scrape the name, price, rating of each and save to csv -----------------------------------------------
# testlink = 'https://www.thewhiskyexchange.com/p/1251/woodford-reserve-distillers-select'
whisky_list = []
for link in product_links:
    r = requests.get(link, headers=headers)

    try:
        soup = BeautifulSoup(r.content, 'lxml')
        name = soup.find('h1', class_="product-main__name").text.strip()
        price = soup.find('p', class_='product-action__price').text.strip()
    except:
        continue

    try:
        rating = soup.find('div', class_='review-overview').text.strip()
    except:
        rating = "no rating"

    whisky = {
        'name': name,
        'price': price,
        'rating': rating
        }

    print(whisky)
    whisky_list.append(whisky)

with open('web_scraped.csv', 'a', newline='') as csvfile:
    fieldnames = ['name', 'price', 'rating']
    thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    thewriter.writeheader()
    for item in whisky_list:
        thewriter.writerow(item)

print(whisky_list)

# ---------------------------------------------------------------------------------------------------------------------------------

# can add dataframe and use pandas
# pip install pandas
# import pandas as pd
# df = pd.DataFrame(whisky_list)
# print(df.head(15))