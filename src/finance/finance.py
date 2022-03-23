import pandas as pd
import yfinance as yf
import altair as alt

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
    # 'facebook': 'FB',
    # 'apple': 'AAPL',
    # 'microsoft': 'MSFT',
    # 'netflix': 'NFLX',
}
df = get_data(days, tickers)

companies = ['google', 'amazon']
data = df.loc[companies]
data = data.sort_index()
data = data.T.reset_index()
data = pd.melt(data, id_vars=['Date']).rename(columns={'value':'Stock Prices(USD)'})

# グラフ描画
chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8)
    .encode(
        x='Date:T',
        y=alt.Y('Stock Prices(USD):Q', stack=None),
        color='Name:N'
    )
)

chart.show()