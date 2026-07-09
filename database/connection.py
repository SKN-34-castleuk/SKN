import mysql.connector

# MySQL 연결 설정
connection = mysql.connector.connect(
    host="localhost",       # MySQL 서버 주소
    user="root",            # 사용자 이름
    password="1234",        # 비밀번호
    database="python_test"  # 사용할 데이터베이스
)

# 연결 확인
if connection.is_connected():
    print("MySQL에 성공적으로 연결되었습니다.")  # 연결 성공 메시지 출력

connection.close()  # 연결 종료