import mysql.connector
from models.database import get_connection  

class RepairTicketService:
    @staticmethod
    def create_repair_ticket(staff_id, equipment_price_list, role):
        conn = get_connection()  # Giả định hàm này trả về kết nối DB
        cursor = conn.cursor()
        try:
            # Chuyển danh sách equipment_id và price thành chuỗi "id:price,id:price"
            # equipment_price_list là danh sách dạng [(equipment_id, price), ...]
            equipment_price_str = ','.join([f"{equip_id}:{price}" for equip_id, price in equipment_price_list])
            
            # Gọi stored procedure với 3 tham số
            cursor.callproc('create_repair_ticket', (staff_id, equipment_price_str, role))
            
            # Lấy ID của repair_ticket vừa tạo
            cursor.execute("SELECT LAST_INSERT_ID()")
            repair_ticket_id = cursor.fetchone()[0]
            
            conn.commit()  # Xác nhận thay đổi
            return repair_ticket_id
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback()  # Hoàn tác nếu lỗi
            return None
        finally:
            cursor.close()
            conn.close()

    
    @staticmethod
    def get_repair_ticket(staff_id=None, status=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if staff_id != None:
                cursor.execute("SELECT * FROM repair_ticket WHERE staff_id = %s AND status = %s", (staff_id, status))
            else:
                cursor.execute("SELECT * FROM repair_ticket WHERE status = %s", (status,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_history_repair_ticket():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM repair_ticket WHERE status = 'COMPLETED' OR status = 'REJECTED' OR status = 'ACCEPTED' ORDER BY start_date DESC")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_total_cost(repair_ticket_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT SUM(price) AS total_cost FROM detail_repair_ticket WHERE repair_ticket_id = %s", (repair_ticket_id,))
            result = cursor.fetchone()  # Lấy hàng đầu tiên (chỉ có một hàng vì SUM)
            
            # Kiểm tra và trả về tổng dưới dạng số nguyên
            if result and result['total_cost'] is not None:
                return int(result['total_cost'])
            return 0  # Trả về 0 nếu không có dữ liệu hoặc tổng là NULL
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_repair_ticket(repair_ticket_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM repair_ticket WHERE id = %s", (repair_ticket_id,))
            
            if cursor.rowcount > 0:
                conn.commit() 
                return True
            else:
                conn.rollback() 
                return False
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback() 
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_in_repair_ticket(repair_ticket_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM v_repair_ticket_details WHERE repair_ticket_id = %s", (repair_ticket_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def complete_repair_ticket(repair_ticket_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('CompleteRepairTicket', [repair_ticket_id])
            conn.commit()
            return True  # ✅ Procedure chạy thành công
        except Exception as e:
            print(f"Error completing repair ticket: {e}")
            return False  # ❌ Có lỗi xảy ra
        finally:
            cursor.close()
            conn.close()
