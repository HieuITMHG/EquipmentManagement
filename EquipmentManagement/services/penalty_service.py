from models.database import get_connection

class PenaltyService:
    @staticmethod
    def get_violation_by__id(student_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM PenaltyDetails WHERE student_id = %s", (student_id,))
            lst_violation = cursor.fetchall()
            return lst_violation
        finally:
            cursor.close()
            conn.close()
