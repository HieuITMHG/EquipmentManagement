import mysql.connector
from models.database import get_connection  # Đảm bảo bạn có hàm này để kết nối DB

class LiquidationSlipService:
    @staticmethod
    def create_liquidation_slip(staff_id, lst_equipment_id, role):
        conn = get_connection()  # Giả định hàm này đã được định nghĩa để lấy kết nối DB
        cursor = conn.cursor()
        try:
            # Chuyển danh sách equipment_id thành chuỗi phân tách bằng dấu phẩy
            equipment_ids_str = ','.join(map(str, lst_equipment_id))
            
            # Gọi stored procedure với 3 tham số
            cursor.callproc('CreateLiquidationSlip', (staff_id, equipment_ids_str, role))
            
            # Lấy ID của liquidation_slip mới tạo
            cursor.execute("SELECT LAST_INSERT_ID()")
            liquidation_slip_id = cursor.fetchone()[0]
            
            conn.commit()  # Xác nhận thay đổi
            return liquidation_slip_id
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback()  # Hoàn tác nếu lỗi
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_liquidation_slip(staff_id=None, status=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if staff_id != None:
                cursor.execute("SELECT * FROM liquidation_slip WHERE staff_id = %s AND status = %s", (staff_id, status))
            else:
                cursor.execute("SELECT * FROM liquidation_slip WHERE status = %s", (status,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_history_liquidation_slip():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM liquidation_slip WHERE status IN ('ACCEPTED', 'COMPLETED', 'REJECTED') ORDER BY liquidation_date DESC")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_liquidation_slip(liquidation_slip_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Thực hiện lệnh DELETE với liquidation_slip_id
            cursor.execute("DELETE FROM liquidation_slip WHERE id = %s", (liquidation_slip_id,))
            
            # Kiểm tra xem có bản ghi nào bị xóa không
            if cursor.rowcount > 0:
                conn.commit()  # Xác nhận thay đổi
                return True
            else:
                conn.rollback()  # Hoàn tác nếu không có bản ghi nào bị xóa
                return False
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback()  # Hoàn tác nếu có lỗi
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_in_liquidation(liquidation_slip_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM v_liquidation_full_details WHERE liquidation_id = %s", (liquidation_slip_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def complete_liquidation_slip(liquidation_slip_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('CompleteLiquidationSlip', [liquidation_slip_id])
            conn.commit()
            return True  # ✅ Procedure chạy thành công
        except Exception as e:
            print(f"Error completing liquidation slip: {e}")
            return False  # ❌ Có lỗi xảy ra
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def accept_liquidation_slip(ticket_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE liquidation_slip SET status = 'ACCEPTED' WHERE id = %s", (ticket_id,))
            conn.commit()
            return cursor.rowcount > 0  
        finally:
            cursor.close()
            conn.close()
