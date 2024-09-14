import streamlit as st # type: ignore
import time
import psycopg2
from psycopg2 import OperationalError
from psycopg2 import pool
import logging

import config

settings = config.get_settings()

DB_HOST = settings.db_host
DB_NAME = settings.db_name
DB_USER = settings.db_user
DB_PASS = settings.db_pass
DB_PORT = settings.db_port

# print(f"""
    
# DB_HOST = {settings.db_host}
# DB_NAME = {settings.db_name}
# DB_USER = {settings.db_user}
# DB_PASS = {settings.db_pass}
# DB_PORT = {settings.db_port}

# """)

# Configure logging
logging.basicConfig(level=logging.INFO)


# Create a connection pool
try:
    connection_pool = pool.SimpleConnectionPool(
        1,  # Minimum number of connections in the pool
        10,  # Maximum number of connections in the pool
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    if connection_pool:
        print("Connection pool created successfully")
except OperationalError as e:
    print(f"Error creating connection pool: {e}")

def fetch_data():
    try:
        # Get a connection from the pool
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sentences")
            rows = cursor.fetchall()
            cursor.close()

            # Release the connection back to the pool
            connection_pool.putconn(conn)

            return rows
    except OperationalError as e:
        st.err(f"OperationalError: {e}")
        return []
    except Exception as e:
        return []
    

def main():
    st.title("Sentiment Analysis Dashboard")
    st.write("Generated sentences and scores")

    unique_id = set()

    while True:
        data = fetch_data()
        if data:
            for row in data:
                id = row[0]
                if id in unique_id:
                    continue
                st.write(row)
                unique_id.add(id)
    
        else:
            st.write("")
        time.sleep(5)

if __name__=="__main__":
    main()