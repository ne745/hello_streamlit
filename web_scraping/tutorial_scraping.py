import requests
import datetime

from bs4 import BeautifulSoup
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
from gspread_dataframe import set_with_dataframe

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

# print(get_data_udemy())
# print(get_data_ec())

# https://docs.gspread.org/en/latest/oauth2.html

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    './data/service_account.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

SP_SHEET_KEY = '1iRmrAm4_560L-zqv18-4bsGK1LwgjgTBfydWddCegCY'
SP_SHEET = 'db'
sh = gc.open_by_key(SP_SHEET_KEY)
worksheet = sh.worksheet(SP_SHEET)
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

#　今日のデータを追加
data_udemy = get_data_udemy()
today = datetime.date.today().strftime('%Y/%m/%d')
data_udemy['date'] = today
df = df.append(data_udemy, ignore_index=True)
set_with_dataframe(worksheet, df, row=1, col=1)