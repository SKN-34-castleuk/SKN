import streamlit as st

# JSON 데이터 출력
data = {
    "제품": "A",
    "가격": 1000,
    "재고": {
        "창고1": 50,
        "창고2": 30
    }
}

st.json(data, expanded=True)