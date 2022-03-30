import streamlit as st

# テキスト入力
st.header('基本情報')
name = st.text_input('名前')
st.write(f'名前は {name} です．')

# ドロップダウンリスト
st.write('生年月日')
columns = st.columns(3)
birth_year = columns[0].selectbox('年', list(range(1900, 2001)))
birth_month = columns[1].selectbox('月', list(range(1, 13)))

if birth_month == 2:
    if birth_year % 400 == 0 or (birth_year % 4 == 0 and birth_year % 100 != 0):
        dates = list(range(1, 30))
    else:
        dates = list(range(1, 29))
elif birth_month in (4, 6, 9, 11):
    dates = list(range(1, 31))
else:
    dates = list(range(1, 32))

birth_date = columns[2].selectbox('日', dates)
st.write(f'生年月日は {birth_year}/{birth_month}/{birth_date} です．')

# チェックボックス
st.header('健康状態')
years = [1, 2, 3, 4, 5, 10]
freq = list(range(1, 8))
is_alcohol = st.checkbox('飲酒')
is_smoking = st.checkbox('喫煙')
if is_alcohol:
    alcohol_years = st.selectbox('飲酒歴', years)
    alcohol_freq = st.selectbox('飲酒頻度', freq)
    st.write(f'1 週間に {alcohol_freq} 日, {alcohol_years} 年間飲酒の習慣がある．')
if is_smoking:
    smoking_years = st.selectbox('喫煙歴', years)
    smoking_freq = st.selectbox('喫煙頻度', freq)
    st.write(f'1 週間に {smoking_freq} 日, {smoking_years} 年間喫煙の習慣がある．')

# スライダー
st.header('こころの健康')
motivation = st.slider("仕事のモチベーション", 0, 100, 50, 10)
st.write(f'仕事のモチベーションは {motivation} %です．')

# エクスパンダー
st.header('FAQ')
expander1 = st.expander('よくある質問1')
expander1.write('回答')
expander2 = st.expander('よくある質問2')
expander2.write('回答')
expander3 = st.expander('よくある質問3')
expander3.write('回答')