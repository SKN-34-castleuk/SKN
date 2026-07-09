import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 가상 데이터 생성: 시간에 따른 주가 변동 시뮬레이션
days = np.linspace(1, 100, 100)  # 100일간의 데이터
stock_price = 100 + np.random.normal(0, 1, 100).cumsum()  # 랜덤하게 변동하는 주가

# 그래프 생성
fig, ax = plt.subplots()
ax.plot(days, stock_price, label="Stock Price", color='blue', linestyle='-', marker='o')
ax.set_title("100일 동안의 주가 변동")
ax.set_xlabel("날짜")
ax.set_ylabel("주가 (단위: $)")
ax.legend()

# Streamlit에서 그래프 출력
st.pyplot(fig)