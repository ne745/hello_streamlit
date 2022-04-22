import requests

from bs4 import BeautifulSoup
import pandas as pd

def get_data_udemy():
    url = 'https://scraping-for-beginner.herokuapp.com/udemy'
    respons = requests.get(url)
    soup = BeautifulSoup(respons.text, 'html.parser')

    n_subscriber = soup.find('p', {'class': 'subscribers'}).text
    n_subscriber = int(n_subscriber.split('：')[1])

    n_review = soup.find('p', {'class': 'reviews'}).text
    n_review = int(n_review.split('：')[1])

    return {'n_subscriber': n_subscriber, 'n_review': n_review}

def get_data_ec():
    url = 'https://scraping.official.ec/'
    respons = requests.get(url)
    soup = BeautifulSoup(respons.text, 'html.parser')

    item_list = soup.find('ul', {'id': 'itemList'})
    items = item_list.find_all('li')

    data = []
    for item in items:
        datum = {}
        datum['title'] = item.find('p', {'class': 'items-grid_itemTitleText_5a0255a1'}).text
        price = item.find('p', {'class': 'items-grid_price_5a0255a1'}).text
        datum['price'] = int(price.replace('¥', '').replace(',', '').replace(' ', ''))
        datum['link'] = item.find('a')['href']
        datum['is_stock'] = '在庫あり' if item.find('p', {'class': 'items-grid_soldOut_5a0255a1'}) is None else '在庫なし'
        data.append(datum)

    df = pd.DataFrame(data)
    return df

print(get_data_udemy())
print(get_data_ec())