from models.database import get_connection

class ViolationService:
    @staticmethod
    def get_all_violation():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM violation")
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_violation_by_id(student_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM PenaltyDetails WHERE student_id = %s", (student_id,))
            lst_violation = cursor.fetchall()
            return lst_violation
        finally:
            cursor.close()
            conn.close()
