import streamlit as st
import pandas as pd
import datetime as dt

# 데이터 생성
data_df = pd.DataFrame({
    "name": ["홍길동", "이몽룡", "성춘향"],
    "appointment": [
        dt.time(9, 30),   # 09:30
        dt.time(14, 0),   # 14:00
        dt.time(18, 45),  # 18:45
    ]
})

st.data_editor(
    data_df,
    column_config={
        "appointment": st.column_config.TimeColumn(
            "Appointment Time"
        )
    },
    hide_index=True,
)