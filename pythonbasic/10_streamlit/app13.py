import streamlit as st
import pandas as pd

data_df = pd.DataFrame({
    "name": ["홍길동", "이몽룡", "성춘향"],
    "birthday": ["1990-01-01", "1995-05-20", "2000-12-31"]   # 문자열
})

data_df["birthday"] = pd.to_datetime(data_df["birthday"])

st.data_editor(
    data_df,
    column_config={
        "birthday": st.column_config.DateColumn(
            "Birthdate"
        )
    },
    hide_index=True,
)