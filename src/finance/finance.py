import requests
import functools

import pandas as pd
import yfinance as yf
import altair as alt

# timeout 設定
# https://github.com/ranaroussi/yfinance/issues/539
session = requests.Session()
session.headers.update({
    'Accept-Encoding': 'gzip, deflate'
})
session.request = functools.partial(session.request, timeout=1)
yf.base._requests = session
yf.utils._requests = session
yf.ticker._requests = session

def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        # 読み込み
        ticker = yf.Ticker(tickers[company])
        hist = ticker.history(period=f'{days}d')
        # 整形
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = "Name"
        # 格納
        df = pd.concat([df, hist])
    return df

days =  10
tickers = {
    'google': 'GOOGL',
    'amazon': 'AMZN',
    'facebook': 'FB',
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
}
df = get_data(days, tickers)

companies = ['google', 'amazon', 'facebook', 'apple', 'microsoft', 'netflix']
data = df.loc[companies]
data = data.sort_index()
data = data.T.reset_index()
data = pd.melt(data, id_vars=['Date']).rename(columns={'value':'Stock Prices(USD)'})

# グラフ描画
ymin, ymax = 200, 500
chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x='Date:T',
        y=alt.Y('Stock Prices(USD):Q', stack=None, scale=alt.Scale(domain=[ymin, ymax])),
        color='Name:N'
    )
)

chart.show()