import mysql.connector
import os 
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

db_password = os.getenv("DB_PASSWORD")
print(db_password)
# MySQL 연결 설정
with mysql.connector.connect(
    host="localhost",       # MySQL 서버 주소
    user="root",            # 사용자 이름
    password= db_password,        # 비밀번호
    database="menudb"  # 사용할 데이터베이스
) as connection:

    with connection.cursor(dictionary= True) as cursor:  # 데이터베이스 작업 커서

        cursor.execute("select* from tbl_menu") # 쿼리 실행

        a = cursor.fetchall()
        # print(rows)
        # for row in rows:
        #     print(row)
     

        connection.commit() # 변경사항 커밋(저장)x

df = pd.DataFrame(a)
st.header("메뉴판")
st.subheader("맛있는 메뉴는 무엇인가요")
st.data_editor(df)
st.write(f"총 메뉴수 : {len(a)}")
