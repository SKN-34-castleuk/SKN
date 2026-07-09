import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 가상 일일 매출 데이터 생성
dates = pd.date_range(start='2024-01-01', periods=50)
sales = np.random.randint(100, 500, 50)  # 일일 매출액 (100 ~ 500 사이)

# 데이터프레임 생성
df = pd.DataFrame({
    "날짜": dates,
    "매출액": sales
})

# 데이터프레임 출력
st.write("일일 매출 데이터프레임:", df)

# Matplotlib 선 그래프 생성
fig, ax = plt.subplots()
ax.plot(df["날짜"], df["매출액"], marker='o', linestyle='-')
ax.set_title("2024년 1월 일일 매출 추이")
ax.set_xlabel("날짜")
ax.set_ylabel("매출액 (단위: 원)")
plt.xticks(rotation=45)  # x축 레이블을 회전하여 날짜가 겹치지 않게 함

# 그래프 출력
st.write(fig)