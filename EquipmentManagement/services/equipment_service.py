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
            cursor.execute("SELECT * FROM equipment WHERE room_id = %s AND status='AVAILABLE' AND equipment_type='MOBILE' OR equipment_type='SHARED'", (room_id,))
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

    @staticmethod
    def get_equipment_id_by_name_and_room(equipment_name, room_id):
        """Tìm equipment.id bằng equipment_name và room_id"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Truy vấn tìm kiếm thiết bị theo tên và room_id
            cursor.execute("""
                SELECT id 
                FROM equipment 
                WHERE equipment_name LIKE %s AND room_id = %s
            """, (f"%{equipment_name}%", room_id))  # Dùng LIKE để tìm kiếm gần đúng tên

            # Đọc kết quả
            result = cursor.fetchone()  # Trả về một kết quả nếu tìm thấy

            return result['id'] if result else None  # Trả về id nếu tìm thấy, ngược lại trả về None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_broken_equipment():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE status = 'BROKEN'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_shared_equipment():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE equipment_type = 'SHARED' AND status = 'AVAILABLE'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def search_equipment( room_id=None, status=None, equipment_type=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM equipment WHERE 1=1"
        params = []

        if room_id:
            query += " AND room_id LIKE %s"
            params.append(f"%{room_id}%")

        if status:
            query += " AND status = %s"
            params.append(status)

        if equipment_type:
            query += " AND equipment_type = %s"
            params.append(equipment_type)

        cursor.execute(query, params)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results