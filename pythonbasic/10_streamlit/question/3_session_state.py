import streamlit as st
import pandas as pd

st.title("Counter")


st.divider()

if 'customer_count' not in st.session_state:
    st.session_state.customer_count = 0

if not 'customer_count':
    st.session_state.customer_count = 0

a = st.button("손님 한 명 추가요~!")

if a:
    st.session_state.customer_count += 1

b = st.button("오늘 장사 끝! 손님 수 초기화할게요~")

if b:
    st.session_state.customer_count = 0

customer_count = st.session_state.customer_count

st.divider()

st.write(f"지금까지 온 손님 수: {customer_count}")