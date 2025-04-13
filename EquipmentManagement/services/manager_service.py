from models.database import get_connection
from werkzeug.security import generate_password_hash

class ManagerService:
    @staticmethod
    def get_all_accounts():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM AccountInfo WHERE role_id = 3")  # chỉ lấy nhân viên
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_account_by_id(account_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM account WHERE id = %s", (account_id,))
            account = cursor.fetchone()
            return account
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_account(password, role_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            hashed_pw = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO account (password, role_id, is_active) VALUES (%s, %s, %s)",
                (hashed_pw, role_id, True)
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_account(account_id, password=None, role_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if password:
                hashed_pw = generate_password_hash(password)
                cursor.execute("UPDATE account SET password = %s WHERE id = %s", (hashed_pw, account_id))

            if role_id is not None:
                cursor.execute("UPDATE account SET role_id = %s WHERE id = %s", (role_id, account_id))

            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_account(account_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM account WHERE id = %s", (account_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
