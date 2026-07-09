import streamlit as st
import pandas as pd

# 데이터 생성
data_df = pd.DataFrame({
    "상품명": ["A 위젯", "B 위젯", "C 위젯"],
    "가격": [1000, 2000, 1500],
    "favorite": [False, True, False]   # 체크박스 컬럼
})

st.data_editor(
    data_df,
    column_config={
        "favorite": st.column_config.CheckboxColumn(
        "Favorite Widget", default=False
        )
    },
    hide_index=True,
)