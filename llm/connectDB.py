import mysql.connector
from mysql.connector import Error

def connect_to_mariadb():
    try:
        # MariaDB에 연결
        connection = mysql.connector.connect(
            host=(입력),  # 또는 'localhost' for local connections
            user=(입력),
            password=(입력),
            database=(입력)
        )
        
        if connection.is_connected():
            print("연결 성공")
            
            cursor = connection.cursor()
            
            # 데이터베이스 버전 확인
            cursor.execute("SELECT VERSION();")
            record = cursor.fetchone()
            print("MariaDB 버전:", record)
            
            # 쿼리 실행 (테이블 생성)
            # cursor.execute("""
            # CREATE TABLE IF NOT EXISTS test_table (
            #     id INT AUTO_INCREMENT PRIMARY KEY,
            #     name VARCHAR(255) NOT NULL,
            #     age INT NOT NULL
            # );
            # """)
            # print("테이블 생성")
            
            # # 데이터 삽입
            # insert_query = "INSERT INTO test_table (name, age) VALUES (%s, %s)"
            # values = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
            # cursor.executemany(insert_query, values)
            # connection.commit()
            # print(f"삽입된 행의 수: {cursor.rowcount}")
            
            # 데이터 조회
            cursor.execute("SELECT * FROM test_table;")
            rows = cursor.fetchall()
            print("test_table의 데이터:")
            for row in rows:
                print(row)
    
    except Error as e:
        print("Error while connecting to MariaDB", e)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("연결 닫힘")

# 함수 호출
connect_to_mariadb()
