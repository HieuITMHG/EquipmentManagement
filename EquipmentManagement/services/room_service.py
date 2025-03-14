from models.database import get_connection

class RoomService:
    @staticmethod
    def get_all_room():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM room")
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()