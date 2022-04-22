from tkinter import W
import requests
from bs4 import BeautifulSoup

url = 'https://scraping-for-beginner.herokuapp.com/udemy'

respons = requests.get(url)

soup = BeautifulSoup(respons.text, 'html.parser')

n_subscriber = soup.find('p', {'class': 'subscribers'}).text
n_subscriber = int(n_subscriber.split('：')[1])

n_review = soup.find('p', {'class': 'reviews'}).text
n_review = int(n_review.split('：')[1])

url_ec = 'https://scraping.official.ec/'
respons = requests.get(url_ec)
soup = BeautifulSoup(respons.text, 'html.parser')

item_list = soup.find('ul', {'id': 'itemList'})
items = item_list.find_all('li')

data_ec = []
for item in items:
    datum_ec = {}
    datum_ec['title'] = item.find('p', {'class': 'items-grid_itemTitleText_5a0255a1'}).text
    price = item.find('p', {'class': 'items-grid_price_5a0255a1'}).text
    datum_ec['price'] = int(price.replace('¥', '').replace(',', '').replace(' ', ''))
    datum_ec['link'] = item.find('a')['href']
    datum_ec['is_stock'] = '在庫あり' if item.find('p', {'class': 'items-grid_soldOut_5a0255a1'}) is None else '在庫なし'
    data_ec.append(datum_ec)
