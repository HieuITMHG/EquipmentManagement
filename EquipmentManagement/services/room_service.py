from models.database import get_connection

class RoomService:
    @staticmethod
    def get_all_room():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phong")
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

    def get_available_room():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""SELECT * 
            FROM phong 
            WHERE id NOT IN (
                SELECT DISTINCT phong_id 
                FROM phieu_muon 
                WHERE trang_thai = 'DA_DUYET'
                AND DATE(ca) = CURDATE()
                AND (
                    TIME(ca) BETWEEN '06:00:00' AND '10:15:00'
                    OR TIME(ca) BETWEEN '12:00:00' AND '16:15:00'
                )
            )
            """)
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()