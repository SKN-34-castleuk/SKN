import streamlit as st
import pandas as pd

st.title("게임 캐릭터의 인지도")

data = pd.DataFrame({
    "캐릭터": ["전사", "법사", "힐러", "탱커", "랜덤"],
    "선택횟수": [120, 95, 150, 80, 111],
    "승률 (%)": [52, 48, 56, 60, 49],
    "인지도 (%)": [25, 20, 30, 15, 22]
})

st.bar_chart(data.set_index("캐릭터")["선택횟수"])
st.line_chart(data.set_index("캐릭터")["승률 (%)"])