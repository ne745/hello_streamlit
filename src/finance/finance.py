import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# 読み込み
aapl = yf.Ticker('AAPL')
days =  20
hist = aapl.history(period=f'{days}d')

# 整形
hist.index = hist.index.strftime('%d %B %Y')
hist = hist[['Close']]
hist.columns = ['apple']
hist = hist.T
hist.index.name = "Name"
print(hist.head(5))