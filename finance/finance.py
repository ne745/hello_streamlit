import requests
import functools

import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')

# ---------- サイド ----------
st.sidebar.write("""
# 株価
こちらは株価可視化ツールです．
以下のオプションから表示日数を指定してください．
""")

st.sidebar.write("""
## 表示日数選択
""")
days = st.sidebar.slider('日数', 1, 50, 20)
# --------------------------

# ---------- メイン ----------
st.write(f"""
### 過去 **{days}日間** の株価
""")
# --------------------------

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

@st.cache
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
        hist.index.name = 'Name'
        # 格納
        df = pd.concat([df, hist])
    return df

# ---------- サイド ----------
st.sidebar.write("""
## 株価の範囲指定
""")
ymin, ymax = st.sidebar.slider('範囲', 0, 3500, (0, 3500))
# --------------------------

# 株価情報の取得
tickers = {
    'google': 'GOOGL',
    'amazon': 'AMZN',
    'facebook': 'FB',
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
}
df = get_data(days, tickers)

# ---------- メイン ----------
companies = st.multiselect(
    '会社を選択',
    tickers.keys()
)
# --------------------------

if not companies:
    st.error('少なくとも一社は選んでください')
else:
    data = df.loc[companies]
    data = data.sort_index()

    # ---------- メイン ----------
    # テーブル表示
    st.write("### 株価 (USD)", data)
    # --------------------------

    data = data.T.reset_index()
    data = pd.melt(data, id_vars=['Date']).rename(columns={'value':'Stock Prices(USD)'})

    # グラフ描画
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x='Date:T',
            y=alt.Y('Stock Prices(USD):Q', stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )

    # ---------- メイン ----------
    st.altair_chart(chart, use_container_width=True)
    # --------------------------