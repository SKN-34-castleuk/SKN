import streamlit as st
import pandas as pd

# 데이터 생성
data = pd.DataFrame({
    "제품": ["A", "B", "C"],
    "growth": [
        [5, 10, 20, 800000],   # A 제품 성장 추이
        [3, 8, 15, 25],    # B 제품 성장 추이
        [10, 12, 18, 22],  # C 제품 성장 추이
    ]
})

st.data_editor(
    data,
    column_config={
        "growth": st.column_config.LineChartColumn(
            "Growth Over Time",
            y_min=0,
            y_max=40
        )
    }
)