from models.database import get_connection
class ManagerService:
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
    def get_equipment_to_select():
        """Lấy danh sách thiết bị không trùng tên"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT DISTINCT equipment_name FROM equipment")
            return cursor.fetchall()
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
   
    @staticmethod
    def get_all_repair_ticket():
        """Lấy tất cả các phiếu sửa chữa"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('get_all_repair_ticket')

            result_data = []
            for result in cursor.stored_results():
                result_data = result.fetchall()
            
            return result_data if result_data else []  # Trả về danh sách, không bao giờ là None

        except Exception as e:
            print(f"[get_all_repair_ticket] Error: {e}")
            return []  # Trả về danh sách rỗng thay vì None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_detail_repair_ticket_by_id(ticket_id):
        """Lấy thông tin một phiếu sửa chữa theo ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM detail_repair_ticket WHERE repair_ticket_id = %s"
            cursor.execute(query, (ticket_id,))
            return cursor.fetchone()  # Trả về dictionary hoặc None nếu không tìm thấy
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_infor_detail_ticket(ticket_id):
        """Lấy thông tin chi tiết thiết bị của một phiếu sửa chữa theo repair_ticket_id"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM RepairEquipmentDetails WHERE repair_ticket_id = %s"
            cursor.execute(query, (ticket_id,))
            result = cursor.fetchall()
            return result if result else []
        except Exception as e:
            print(f"[get_infor_detail_ticket] Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_ticket_status_returned(ticket_id):
        """Gọi stored procedure để cập nhật trạng thái phiếu sửa chữa thành 'RETURNED'"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('update_ticket_status_returned', (ticket_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"[update_ticket_status_returned] Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def check_equipment_in_room(room_id, equipment_id):
        """Kiểm tra thiết bị có thuộc phòng đó không bằng cách gọi stored procedure"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)  # Trả về dạng dict
        try:
            cursor.callproc('check_equipment_in_room', (room_id, equipment_id))
            
            # Lấy kết quả trả về từ stored procedure
            for result in cursor.stored_results():
                data = result.fetchall()
                if data:
                    return True  # Có kết quả → thiết bị thuộc phòng
                else:
                    return False
        except Exception as e:
            print(f"[check_equipment_in_room] Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_repair_ticket(staff_id, equipment_id, price, room_id):
        """Tạo một phiếu sửa chữa bằng cách gọi stored procedure create_repair_ticket"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Gọi stored procedure
            cursor.callproc('create_repair_ticket', (
                staff_id,
                equipment_id,
                price,
                room_id
            ))

            conn.commit()
            print("[create_repair_ticket] Tạo phiếu sửa chữa thành công.")
            return True
        except Exception as e:
            print(f"[create_repair_ticket] Lỗi: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
