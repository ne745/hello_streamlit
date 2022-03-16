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

# テキストをマークダウンで表示
"""
# 章
## 節
### 項
```python
import streamlit as st
import numpy as np
import pandas as pd
```
"""

# グラフの表示
df = pd.DataFrame(np.random.rand(20, 3), columns=['a', 'b', 'c'])
st.line_chart(df)
st.bar_chart(df)

# 地図の表示
df = pd.DataFrame(
    np.random.rand(100, 2) / [50, 50] + [35.69, 139.70],
    columns=['lat', 'lon']
)
st.map(df)