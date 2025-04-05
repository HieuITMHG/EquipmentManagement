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
