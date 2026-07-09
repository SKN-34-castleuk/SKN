import streamlit as st
import pandas as pd

# 데이터 생성
data = {'제품': ['A', 'B', 'C'], 
        '가격': [1000, 1500, 2000]}
df = pd.DataFrame(data)

# 정적 테이블 출력
st.table(df)