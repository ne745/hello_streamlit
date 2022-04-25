import requests

from bs4 import BeautifulSoup
import pandas as pd

from google.oauth2.service_account import Credentials
import gspread

import streamlit as st

import altair as alt

def fetch_data_ec():
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

def fetch_data():
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

    # データの取得
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.astype({'n_subscriber': int, 'n_review': int})
    return df

def draw_graph(df_udemy):
    # グラフ描画
    base = alt.Chart(df_udemy).encode(
        alt.X('date:T', axis=alt.Axis(title=None))
    )
    line1 = base.mark_line(stroke='#57A44C').encode(
        alt.Y(
            'n_subscriber',
            axis=alt.Axis(title='受講生数', titleColor='#57A44C'),
            scale=alt.Scale(
                domain=[
                    df_udemy['n_subscriber'].min() - 10,
                    df_udemy['n_subscriber'].max() + 10
                ]
            )
        )
    )
    line2 = base.mark_line(stroke='#5276A7').encode(
        alt.Y(
            'n_review',
            axis=alt.Axis(title='レビュー数', titleColor='#5276A7'),
            scale=alt.Scale(
                domain=[
                    df_udemy['n_review'].min() - 10,
                    df_udemy['n_review'].max() + 10
                ]
            )
            )
    )
    chart = alt.layer(line1, line2).resolve_scale(y='independent')
    return chart

def main():
    df_udemy = fetch_data()
    chart = draw_graph(df_udemy)

    df_ec = fetch_data_ec()

    st.title('ウェブスクレイピング活用アプリ')

    st.write('## Udemy 情報')
    st.altair_chart(chart, use_container_width=True)

    st.write('## EC 在庫情報', df_ec)

if __name__ == '__main__':
    main()