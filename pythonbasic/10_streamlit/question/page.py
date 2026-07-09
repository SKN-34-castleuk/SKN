import streamlit as st
import pandas as pd
from streamlit_extras.chartjs_chart import *
with st.sidebar:
    st.title("🐍 Python")

    st.info("""
    쉽고 강력한 프로그래밍 언어
    """)

    st.divider()

    st.subheader("🔹--간략하게--🔹")

    menu = st.radio(
        "",
        [
            "파이썬 소개",
            "Python의 특징",
            "예제 코드",
            "활용 분야",
            "인기 분야"
        ]
    )
    if menu == "파이썬 소개":
        st.info("""
        Python은 쉽고 강력한 프로그래밍 언어로
        AI, 데이터 분석, 웹 개발 등 다양한 분야에서 사용됩니다.
        """)

    elif menu == "Python의 특징":
        st.info("""
        
        ✔ 쉬운 문법
        
        ✔ 높은 가독성
        
        ✔ 풍부한 라이브러리
        
        ✔ 높은 생산성
        """)

    elif menu == "예제 코드":
        st.code(
            """
print("Hello Python")

for i in range(5):
    print(i)
            """,
            language="python"
        )

    elif menu == "활용 분야":
        st.info("""
        • 데이터 분석 & 시각화
        
        • 웹 개발
        
        • 인공지능(AI) & 머신러닝(ML)
        
        • 웹 파싱/크롤링
        
        • 시스템 자동화
        """)

    elif menu == "인기 분야":
        st.info("""
        현재 Python은 AI와 데이터 분석 분야에서
        가장 많이 활용되고 있습니다.
        """)

    elif menu == "배우면 좋은 이유":
        st.success("""
        ✔ 입문자가 배우기 쉬움
        
        ✔ 취업 시장 수요가 높음
        
        ✔ 다양한 분야에 활용 가능
        """)
    st.divider()
    

    st.subheader("🔹 추천 학습 순서 🔹")
    st.markdown("""
    - #### 기본 문법 ➡️ 조건문/반복문 ➡️ 함수 ➡️ 클래스 ➡️ 데이터 분석 ➡️ AI / 머신러닝
    """)
    st.divider()
    st.subheader("🔹 학습 체크리스트 🔹")

    checks = [
        st.checkbox("Python 기본 문법"),
        st.checkbox("조건문 / 반복문"),
        st.checkbox("함수"),
        st.checkbox("클래스"),
        st.checkbox("데이터 분석"),
        st.checkbox("AI & 머신러닝")
    ]

    completed = sum(checks)
    total = len(checks)

    st.progress(completed / total)

    st.caption(f"진행률 : {completed}/{total} ({completed/total*100:.0f}%)")
    st.divider()
    

st.title("🐍 Python")
st.subheader("🔹쉽고 강력한 프로그래밍 언어")
st.divider()

st.header("Python이란👓​")
st.info(
    "Python은 데이터 분석, AI, 웹 개발 등 다양한 분야에서 사용되는 대표적인 프로그래밍 언어입니다."
)

st.divider()

# 첫 번째 행
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Python의 특징")
    st.markdown("""
    - 배우기 쉬운 문법
    - 간결하고 높은 가독성
    - 다양한 라이브러리 제공
    - 높은 생산성
    - 플랫폼 독립적
    """)

with col2:
    st.subheader("📌 예제 코드")
    st.code(
        """
print("Hello Python!")

for i in range(5):
    print(i)
        """,
        language="python"
    )

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("📌 활용 분야")

    select = st.selectbox(
        "분야를 선택하세요",
        ["데이터 분석 & 시각화", 
         "웹 개발", 
         "인공지능(AI) & 머신러닝(ML)", 
         "웹 파싱/크롤링",
         "시스템 자동화",
         ]
    )

    if select == "데이터 분석 & 시각화":
        st.success("""
        - Pandas, NumPy, Matplotlib 등을 사용
        - 데이터 전처리 및 분석: 대규모 데이터 가공 및 통계 분석
        - 데이터 시각화: 분석 결과를 차트나 그래프로 도표화하여 대시보드 구축
        """)
    elif select == "웹 개발":
        st.success("""
        - Django,FastAPI,Flask 등을 사용        
        - 백엔드 서버 구축: 대규모 트래픽 처리 및 데이터베이스 연동
        - 풀스택 개발: 프론트엔드와 백엔드를 아우르는 웹 애플리케이션 제작      
        """)
    elif select == "인공지능(AI) & 머신러닝(ML)":
        st.success("""
        - TensorFlow, PyTorch 등을 사용
        - 머신러닝·딥러닝: 데이터 학습을 통한 예측 모델 구축, 컴퓨터 비전, 이미지 및 음성 인식
        - 생성형 AI: 거대언어모델(LLM) 기반의 챗봇 및 AI 에이전트 개발
        """)
    elif select == "웹 파싱/크롤링":
        st.success("""
        - BeautifulSoup, Selenium, Requests 등을 사용
        - 웹 스크래핑(크롤링): 웹사이트의 데이터를 자동으로 수집 및 저장        
        """)

    else:
        st.success("""
        - 문서 및 파일 자동화: 엑셀, 워드, PDF 등의 문서 자동 생성 및 데이터 추출
        - 매크로: 마우스 클릭 및 키보드 입력 자동화           
        """)

with col4:
    st.subheader("📌Python 인기 분야")

   
    spec = {
        "type" : "pie",
        "data" : {
            "labels": ["인공지능(AI) & 머신러닝(ML)","데이터 분석 & 시각화", "웹 개발", "시스템 자동화","웹 파싱/크롤링"],
            "datasets": [{"data":[30, 25, 20, 15, 10]}]
        },
        "options": {
        "plugins": {
            "title": {
                "display": True,
                "text": "Python 주요 활용 분야( % )"
            },
            "legend": {
                "position": "top"
            }
            
        }
    }
}
    


   
    chartjs_chart(spec)
  


st.divider()

# 마지막 영역
st.subheader("📌Python을 배우면 좋은 이유")

col5, col6, col7 = st.columns(3)

with col5:
    st.markdown("""
            - #### 난이도
                 쉬움👌   
""")

with col6:
    st.markdown("""
            - ####  활용도
                매우 높음⬆️  
""")

with col7:
    st.markdown("""
            - ####  취업 시장
                인기👍  
""")


