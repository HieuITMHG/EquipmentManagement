import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWD'),
        database=os.getenv('DB_NAME'),
    )