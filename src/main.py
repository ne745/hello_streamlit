import streamlit as st
import numpy as np
import pandas as pd

st.title("Streamlit 超入門")

st.write("DataFrame")


# テーブルの表示
df = pd.DataFrame({
    "1列目": [1, 2, 3, 4],
    "2列目": [10, 20, 30, 40]
})

# 動的なテーブル (ソートができる)
st.dataframe(df.style.highlight_max(axis=0))
# 静的なテーブル (ソートができない)
# st.table(df.style.highlight_max(axis=0))