import streamlit as st
import pandas as pd

# 데이터 생성
data = {
    'name': ['A', 'B', 'C'],
    '가격': [1000, 1500, 2000],
    'description': [
        '고급 원단 사용',
        '친환경 소재',
        '내구성 강함'
    ]
}
df = pd.DataFrame(data)

st.data_editor(
    df, 
    column_config={
    "description": st.column_config.TextColumn(
        "제품 설명",
        max_chars=100,              # 최대 문자수 제한
        validate=r"^[가-힣 ]+$")    # 한글과 공백만 입력 가능
})