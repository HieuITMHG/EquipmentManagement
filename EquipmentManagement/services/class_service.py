from models.database import get_connection

class ClassService:
    @staticmethod
    def get_all_class():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM class")
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_class_by_id(class_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM class WHERE id = %s", (class_id,))
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()
