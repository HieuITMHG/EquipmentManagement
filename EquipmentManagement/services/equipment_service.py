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

    @staticmethod
    def add_equipment(new_name, new_status, new_type, new_room):
        """Thêm thiết bị mới vào hệ thống"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Gọi stored procedure để thêm thiết bị mới
            cursor.callproc('add_equipment', [new_name, new_status, new_type, new_room])

            # Commit để xác nhận thay đổi
            conn.commit()
            return True
        except Exception as e:
            # Nếu có lỗi, rollback transaction
            conn.rollback()
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_equipment_by_id(equipment_id):
        """Xóa thiết bị theo ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Gọi stored procedure để xóa thiết bị
            cursor.callproc('delete_equipment_by_id', [equipment_id])

            # Commit để xác nhận thay đổi
            conn.commit()
            return True
        except Exception as e:
            # Nếu có lỗi, rollback transaction
            conn.rollback()
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()