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

def add_today_data():
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
    data_udemy['date'] = datetime.date.today().strftime('%Y/%m/%d')
    df = df.append(data_udemy, ignore_index=True)
    set_with_dataframe(worksheet, df, row=1, col=1)

if __name__ == '__main__':
    add_today_data()