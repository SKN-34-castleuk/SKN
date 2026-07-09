import streamlit as st
import pandas as pd
from datetime import date,time

# 가상 데이터 생성
df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '이영희'],
    '점수': [85, 90, 95]
})

# CSV로 변환
csv = df.to_csv().encode('utf-8')

# 다운로드 버튼
st.download_button(label="CSV 다운로드", data=csv, file_name='data.csv', mime='text/csv')

# 피드백 버튼
# thumbs, faces, stars 
# 가상 피드백 데이터
selected = st.feedback("stars")

if selected is not None:
    st.write(f"별점 {selected + 1}을 선택하셨습니다.")


# 폼 제출 버튼
# 가상 폼 생성
with st.form("my_form"):
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=0)
    submit = st.form_submit_button("제출")

if submit:
    st.write(f"이름: {name}, 나이: {age}")

# 링크 버튼
# 외부 링크로 연결되는 버튼 생성
st.link_button("Google로 이동", url="https://www.google.com")

#체크박스 버튼
# 체크박스 생성
agree = st.checkbox("동의합니다")

if agree:
    st.write("동의해주셔서 감사합니다!")
else:
    st.write(" 동의해주셔야합니다! ")

# 토글 스위치 생성
activated = st.toggle("기능 활성화")

if activated:
    st.write("기능이 활성화되었습니다.")
else:
    st.write("기능이 비활성화되었습니다.")

# 라디오 버튼 생성
choice = st.radio("선호하는 색상을 선택하세요:", ["검정", "노랑", "파랑"])

st.write(f"선택된 색상: {choice}")

# 드롭다운 선택 박스 생성
option = st.selectbox("가장 좋아하는 언어를 선택하세요:", ["Python", "JavaScript", "Java"])

st.write(f"선택된 언어: {option}")

# 멀티 셀렉트 박스 생성
selected = st.multiselect("구매할 품목을 선택하세요:", ["사과", "바나나", "딸기"])

st.write(f"선택된 품목: {selected}")


# 셀렉트 슬라이더 생성
size = st.select_slider("사이즈를 선택하세요:", options=["S", "M", "L", "XL"])

st.write(f"선택된 사이즈: {size}")



# 텍스트 입력 위젯 생성
name = st.text_input("이름을 입력하세요:", value="홍길동")

st.write(f"입력된 이름: {name}")


# 숫자 입력 창 생성
number = st.number_input("나이를 입력하세요:", min_value=0, max_value=120)

st.write(f"입력된 나이는 {number}세 입니다.")


# 날짜 입력 위젯 생성
selected_date = st.date_input("날짜를 선택하세요:", value=date.today())

st.write(f"선택된 날짜: {selected_date}")

# 시간 입력 위젯 생성
selected_time = st.time_input("시간을 선택하세요:", value=time(12, 30))

st.write(f"선택된 시간: {selected_time}")

# 파일 업로드 위젯 생성
uploaded_file = st.file_uploader("파일을 업로드하세요:", type=["csv", "txt"])

if uploaded_file is not None:
    st.write(f"업로드된 파일: {uploaded_file.name}")

# 성공 메시지 출력
st.success('데이터가 성공적으로 저장되었습니다!', icon="✅")

# 정보 메시지 출력
st.info('이 페이지는 실시간으로 업데이트됩니다.', icon="ℹ️")

# 경고 메시지 출력
st.warning('저장 공간이 90% 사용되었습니다.', icon="⚠️")

# 오류 메시지 출력
st.error('파일을 로드하는 중 오류가 발생했습니다.', icon="❌")