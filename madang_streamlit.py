import streamlit as st
import pymysql
import pandas as pd

# 데이터베이스 연결 설정
dbConn = pymysql.connect(user='root', passwd='1234',host='192.168.217.129', db='madang', charset='utf8')
cursor = dbConn.cursor(pymysql.cursors.DictCursor)

# 각 컨테이너 만들기
c1 = st.container()
c2 = st.container()

with c1:
    col1, col2 = st.columns([3, 1])

    # 검색어 입력
    search_term = col1.text_input("Enter search term")

    # Search 버튼 생성
    search_button = col2.button("Search")

# 검색 버튼을 누를 때만 실행
if search_button:
    if search_term:
        # 각 테이블에서 검색
        queries = {
            "Customer": f"""
                SELECT * FROM Customer
                WHERE name LIKE '%{search_term}%'
                OR address LIKE '%{search_term}%'
                OR phone LIKE '%{search_term}%';
            """,
            "Orders": f"""
                SELECT * FROM Orders
                WHERE CAST(orderid AS CHAR) LIKE '%{search_term}%'
                OR CAST(custid AS CHAR) LIKE '%{search_term}%'
                OR CAST(bookid AS CHAR) LIKE '%{search_term}%'
                OR CAST(saleprice AS CHAR) LIKE '%{search_term}%'
                OR CAST(orderdate AS CHAR) LIKE '%{search_term}%';
            """,
            "Book": f"""
                SELECT * FROM Book
                WHERE bookname LIKE '%{search_term}%'
                OR publisher LIKE '%{search_term}%'
                OR CAST(price AS CHAR) LIKE '%{search_term}%';
            """
        }

        # 각 테이블에서 결과 가져와서 출력
        for table_name, query in queries.items():
            cursor.execute(query)
            result = cursor.fetchall()

            if result:
                # 결과가 있으면 DataFrame으로 변환 후 표시
                df = pd.DataFrame(result)
                c2.subheader(f"{table_name} Results")
                c2.write(df)
            else:
                c2.subheader(f"{table_name} Results")
                c2.write("No results found.")
    else:
        c2.write("Please enter a search term.")

# 데이터베이스 연결 종료
cursor.close()
dbConn.close()
