import streamlit as st
import pandas as pd
import altair as alt

# 가상 데이터 생성: 월별 매출 및 이익 데이터
data = pd.DataFrame({
    '월': pd.date_range(start='2026-01-01', periods=12, freq='ME'),
    '매출': [500, 600, 700, 800, 900, 850, 950, 1100, 1050, 1200, 1250, 1300],
    '이익': [50, 60, 70, 85, 90, 80, 95, 100, 105, 110, 120, 130]
})

# Altair 차트 생성
chart = alt.Chart(data).mark_line(point=True).encode(
    x='월:T',
    y='매출:Q',
    tooltip=['월:T', '매출:Q', '이익:Q']
).properties(
    title="2026년 월별 매출 및 이익"
)

# 차트 출력
st.altair_chart(chart, use_container_width=True)