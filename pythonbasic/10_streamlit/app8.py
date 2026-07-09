import streamlit as st
import pandas as pd

# 데이터 생성
data = {
    'name': ['A', 'B', 'C'], 
    '가격': [1000, 1500, 2000]}
df = pd.DataFrame(data)

st.data_editor(
    df,
    column_config={
    "name": st.column_config.Column("제품 이름", width="large", required=True)
})