import mysql.connector
from mysql.connector import Error

def connect_to_mariadb():
    try:
        # 데이터베이스 연결 설정
        connection = mysql.connector.connect(
            host='(입력)',  # 또는 'localhost' for local connections
            user='(입력)',
            password='(입력)',
            database='(입력)'
        )
        
        if connection.is_connected():
            print("MariaDB에 성공적으로 연결되었습니다.")
            
            # 커서 객체 생성
            cursor = connection.cursor()
            
            # 데이터베이스 이름 출력|
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("현재 연결된 데이터베이스:", record[0])
    
    except Error as e:
        print("Error while connecting to MariaDB", e)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MariaDB 연결이 닫혔습니다.")

# 함수 호출
connect_to_mariadb()
