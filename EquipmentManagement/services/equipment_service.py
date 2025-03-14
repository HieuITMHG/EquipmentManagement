from models.database import get_connection

class EquipmentService:
    @staticmethod
    def get_all_equipment():
        """Lấy danh sách tất cả thiết bị từ DB"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment")
            return cursor.fetchall()  # Trả về trực tiếp danh sách dictionary
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_by_id(equipment_id):
        """Lấy thiết bị theo ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE id = %s", (equipment_id,))
            equipment = cursor.fetchone()
            return equipment if equipment else None  # Trả về None nếu không tìm thấy
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_by_room(room_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE room_id = %s", (room_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_borrowable_equipment_by_room(room_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE room_id = %s AND status='AVAILABLE' AND equipment_type='MOBILE'", (room_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()