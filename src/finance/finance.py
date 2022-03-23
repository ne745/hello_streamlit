import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

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
print(df)