import mysql.connector

# MySQL 연결 설정
with mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="python_test"
) as connection:
    with connection.cursor() as cursur:
        cursor.execute("Select * from users")
        