import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        user='root',
        password='123456',
        database='defaultdb',
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci"
    )