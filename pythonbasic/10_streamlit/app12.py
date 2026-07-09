import streamlit as st
import pandas as pd

# 데이터 생성
df = pd.DataFrame({
    "제품명": ["A 제품", "B 제품", "C 제품"],
    "가격": [1000, 2000, 3000],
    "category": ["전자제품", "의류", "가전제품"]   # selectbox 컬럼
})

st.data_editor(
    df,
    column_config={
        "category": st.column_config.SelectboxColumn(
        "카테고리",
        options=["전자제품", "의류", "가전제품"],
        default="전자제품"
        )
    }
)