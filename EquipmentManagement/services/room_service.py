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

    @staticmethod
    def get_room_by_id(room_id):
        """Lấy thiết bị theo ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM room WHERE id = %s", (room_id,))
            room = cursor.fetchone()
            return room if room else None  # Trả về None nếu không tìm thấy
        finally:
            cursor.close()
            conn.close()