import mysql.connector
from models.database import get_connection  # Đảm bảo bạn có hàm này để kết nối DB

class LiquidationSlipService:
    @staticmethod
    def get_pending_liquidation():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phieu_thanh_ly WHERE trang_thai = 'CHO_DUYET'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_liquidation_slip(staff_id=None, status=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if staff_id != None:
                cursor.execute("SELECT * FROM phieu_thanh_ly WHERE nhan_vien_id = %s AND trang_thai = %s", (staff_id, status))
            else:
                cursor.execute("SELECT * FROM phieu_thanh_ly WHERE trang_thai = %s", (status,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_total_cost(ticket_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT SUM(liquidation_value) AS total_cost FROM view_equipment_liquidation_details WHERE phieu_thanh_ly_id = %s", (ticket_id,))
            result = cursor.fetchone()  # Lấy hàng đầu tiên (chỉ có một hàng vì SUM)
            
            # Kiểm tra và trả về tổng dưới dạng số nguyên
            if result and result['total_cost'] is not None:
                return int(result['total_cost'])
            return 0  # Trả về 0 nếu không có dữ liệu hoặc tổng là NULL
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_history_liquidation_slip(start_date=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM phieu_thanh_ly WHERE trang_thai IN ('DA_DUYET', 'HOAN_THANH', 'TU_CHOI')"
            params = []
            
            if start_date:
                query += " AND DATE(ngay_thanh_ly) = %s"
                params.append(start_date)
                
            query += " ORDER BY ngay_thanh_ly DESC"
            cursor.execute(query, params)
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
            cursor.execute("DELETE FROM phieu_thanh_ly WHERE id = %s", (liquidation_slip_id,))
            
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
            cursor.execute("SELECT * FROM view_equipment_liquidation_details WHERE phieu_thanh_ly_id = %s", (liquidation_slip_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remove_equipment_from_slip(liquidation_slip_id, equipment_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            print(f"Calling remove_equipment_from_liquidation_slip with liquidation_slip_id={liquidation_slip_id}, equipment_id={equipment_id}")
            cursor.callproc("remove_equipment_from_liquidation_slip", [liquidation_slip_id, equipment_id])
            
            for result in cursor.stored_results():
                result_set = result.fetchone()
                print(f"Procedure result: success={result_set['success']}, error_code={result_set['error_code']}, message={result_set['message']}")
                
                if result_set['success'] == 0:
                    print(f"Procedure failed: {result_set['message']}")
                    conn.rollback()
                    return False
            conn.commit()
            return True

        except Exception as e:
            print(f"Error removing equipment from slip: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def get_existing_ticket(staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phieu_thanh_ly WHERE nhan_vien_id = %s AND trang_thai = 'CHUAN_BI'", (staff_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_equipment_to_ticket(staff_id, equipment_id, description=None, price=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            print(f"Calling them_thiet_bi_thanh_ly with staff_id={staff_id}, equipment_id={equipment_id}, price={price}, description={description}")
            cursor.callproc("them_thiet_bi_thanh_ly", [staff_id, equipment_id, price, description])
            
            # Fetch the result set from the procedure
            for result in cursor.stored_results():
                result_set = result.fetchone()
                print(f"Procedure result: success={result_set['success']}, error_code={result_set['error_code']}, message={result_set['message']}")
                
                if result_set['success'] == 0:
                    print(f"Procedure failed: {result_set['message']}")
                    conn.rollback()
                    return False
            
            conn.commit()
            print("Equipment added successfully")
            return True
        except Exception as e:
            print(f"Error adding equipment to ticket: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_my_liquidation_slip(staff_id=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phieu_thanh_ly WHERE nhan_vien_id = %s AND (trang_thai = 'CHO_DUYET' OR trang_thai = 'CHUAN_BI')", (staff_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def confirm_liquidation_slip(request_id, role_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if role_id == 2:
                cursor.execute("UPDATE phieu_thanh_ly SET trang_thai = 'CHO_DUYET' WHERE id = %s", (request_id,))
            else:
                cursor.execute("UPDATE phieu_thanh_ly SET trang_thai = 'DA_DUYET' WHERE id = %s", (request_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating repair ticket status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_processing_equipment():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT DISTINCT thiet_bi_id
                FROM (
                    SELECT thiet_bi_id
                    FROM chi_tiet_sua_chua ctsc
                    JOIN phieu_sua_chua psc ON ctsc.phieu_sua_chua_id = psc.id
                    WHERE psc.trang_thai IN ('CHUAN_BI', 'CHO_DUYET')

                    UNION

                    SELECT thiet_bi_id
                    FROM chi_tiet_thanh_ly cttl
                    JOIN phieu_thanh_ly ptl ON cttl.phieu_thanh_ly_id = ptl.id
                    WHERE ptl.trang_thai IN ('CHUAN_BI', 'CHO_DUYET')
                ) AS processing_equipment;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [row['thiet_bi_id'] for row in results]
        finally:
            cursor.close()
            conn.close()



