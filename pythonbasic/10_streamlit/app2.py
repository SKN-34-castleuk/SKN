import streamlit as st

st.title("최고의 데이터 분석 앱")

st.divider()

st.header("데이터 시각화 기능")
st.subheader("2026년 매출 추이 데이터 시각화")
st.write("차트를 통한 매출 추이를 한눈에 보고 싶으신가요?")

st.divider()

st.markdown("""
##분석결과
- **매출 성장률**: 15%
- _고객 만족도_: 90%

[자세한 내용 보기]<https://www.exmaple.com>)
""")

st.divider()

st.image("sales_trend.png", caption="2026년 예측 매출 차트")
st.caption("이 차트는 최신 AI 모델을 사용하여 생성되었습니다.")