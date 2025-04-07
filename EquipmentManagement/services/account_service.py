from models.database import get_connection

class AccountService:
    @staticmethod
    def get_all_account():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM AccountInfo")
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def get_account_by_person_id(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM AccountInfo WHERE person_id = %s", (user_id,))
            account = cursor.fetchone()
            return account if account else None  
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_account_personal_id_by_person_id(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT person_id FROM AccountInfo WHERE person_id = %s", (user_id,))
            account = cursor.fetchone()
            return account if account else None  
        finally:
            cursor.close()
            conn.close()
    
