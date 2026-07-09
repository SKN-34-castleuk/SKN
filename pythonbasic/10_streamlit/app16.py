import streamlit as st
import pandas as pd

# 데이터 생성
data_df = pd.DataFrame({
    "상품명": ["A", "B", "C"],
    "sales": [30, 75, 100]   # 숫자값(필수)
})

st.data_editor(
    data_df,
    column_config={
        "sales": st.column_config.ProgressColumn(
            "Sales Volume",
            min_value=0,
            max_value=100
        )
    },
    hide_index=True,
)