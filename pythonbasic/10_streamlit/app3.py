import streamlit as st
import pandas as pd
import numpy as np

# 판매 데이터 생성
data = {
    "Product": ["A", "B", "C", "D"],
    "Sales": [500, 300, 400, 600],
    "Growth (%)": [10, -5, 15, 7]
}
df = pd.DataFrame(data)

# DataFrame을 시각적으로 강조하여 출력
st.dataframe(df.style.highlight_max(subset="Sales", color="lightgreen").highlight_min(subset="Growth (%)", color="pink"))

# 열 설정을 추가한 DataFrame 표시
st.dataframe(df, column_config={
    "Sales": st.column_config.NumberColumn("Total Sales", format="%d units"),
    "Growth (%)": st.column_config.NumberColumn("Growth Percentage", format="%.1f%%")
}, use_container_width=True)