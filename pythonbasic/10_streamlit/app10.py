import streamlit as st
import pandas as pd

# 데이터 생성
data = {
    'name': ['A', 'B', 'C'], 
    'price': [1000, 1500, 2000]
}
df = pd.DataFrame(data)

st.data_editor(df,
                column_config={
    "price": st.column_config.NumberColumn(
    "가격", min_value=0, max_value=100000, format="₩%.0f")  # 소수점 없이 정수로 표시
})