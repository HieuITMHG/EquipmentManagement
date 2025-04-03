from models.database import get_connection
class StaffService:
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
    def get_all_equipment_with_room():
        """Lấy danh sách tất cả thiết bị kèm room_id"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, equipment_name, room_id FROM equipment")
            return cursor.fetchall()  # Trả về danh sách dictionary chứa room_id
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def change_equi_info(new_id,new_name,new_room):
        """Lấy danh sách tất cả thiết bị kèm room_id"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Gọi stored procedure để từ chối yêu cầu mượn
            cursor.callproc('change_equi_info', [new_id, new_name,new_room])

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