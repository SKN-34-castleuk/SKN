import streamlit as st

st.title("사용자 입력 받는 페이지")

st.divider()


col1, col2= st.columns(2)
with col1:
    name = st.text_input("닉네임 입력:", value="홍길동")
    age  = st.number_input("나이 입력",max_value=100,min_value=13)
    world = st.selectbox("국적",["한국",'중국','일본','미국','외계'])
    hobby = st.radio("취미",['맛집 탐방', '영화 감상', '음악 감상', '뜨개질'])
    option = st.checkbox("개인정보 제공 동의")
    if option:
        st.write("동의 완료")
    else:
        st.write("동의 해주셔야합니다.")

with col2:
    end = st.button("✅ 입력 완료")
    if end:
        st.write(f"""
이름이 뭐야?{name}\n
몇 살이야?{age}\n
어디서 왔어?{world}\n
취미가 뭐야?{hobby}\n
개인정보 제공에 동의해?{option}
""")

st.divider()
