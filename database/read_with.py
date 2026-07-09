import mysql.connector
import os 
from dotenv import load_dotenv
load_dotenv()

db_password = os.getenv("DB_PASSWORD")
print(db_password)
# MySQL 연결 설정
with mysql.connector.connect(
    host="localhost",       # MySQL 서버 주소
    user="root",            # 사용자 이름
    password= db_password,        # 비밀번호
    database="python_test"  # 사용할 데이터베이스
) as connection:

    with connection.cursor() as cursor:  # 데이터베이스 작업 커서

    # with connection.cursor(dictionary= True) as cursor:  딕셔너리로 값을 가져옴

        cursor.execute("select*from users") # 쿼리 실행

        rows = cursor.fetchall()
        # print(rows)
        # for row in rows:
        #     print(row)
        print(rows)

        connection.commit() # 변경사항 커밋(저장)

