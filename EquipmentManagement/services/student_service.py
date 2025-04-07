from models.database import get_connection

class StudentService:
    @staticmethod
    def get_all_equipment():
        """Lấy danh sách tất cả thiết bị từ DB"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment")
            print(cursor.fetchone())
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_student_by_id(student_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM StudentInfo WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
            return student if student else None  
        finally:
            cursor.close()
            conn.close()
