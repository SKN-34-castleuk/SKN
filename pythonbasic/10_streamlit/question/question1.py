import streamlit as st

st.title("오늘은 수요일")

st.divider()

st.header("오늘은 Streamlit 배우는 날​​​ ​")
st.subheader("Streamlit으로 나만의 데모 페이지 만들기~~~!🔥🔥🔥")

url = st.text_input("오늘은 내가 만들어보고 싶은 사이트는?!:")

st.write(f"입력된 사이트: {url}")

a = st.button(f"{url} 접속하기")
if a:
    st.write(f"{url} 접속중!!!!!🚀🚀🚀")
    
st.divider()
