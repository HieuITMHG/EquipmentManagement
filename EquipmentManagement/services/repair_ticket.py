import mysql.connector
from models.database import get_connection  

class RepairTicketService:
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
    def get_my_repair_ticket(staff_id=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phieu_sua_chua WHERE nhan_vien_id = %s AND (trang_thai = 'CHO_DUYET' OR trang_thai = 'CHUAN_BI')", (staff_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_pending_repair_ticket():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phieu_sua_chua WHERE trang_thai = 'CHO_DUYET'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_history_repair_ticket(start_date=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT * FROM phieu_sua_chua 
                WHERE trang_thai IN ('HOAN_THANH', 'DA_DUYET')
            """
            params = []

            if start_date:
                query += " AND DATE(ngay_bat_dau) = %s"
                params.append(start_date)

            query += " ORDER BY ngay_bat_dau DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_total_cost(repair_ticket_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT SUM(repair_cost) AS total_cost FROM view_equipment_repair_details WHERE phieu_sua_chua_id = %s", (repair_ticket_id,))
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
            cursor.execute("DELETE FROM phieu_sua_chua WHERE id = %s", (repair_ticket_id,))
            
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
            cursor.execute("SELECT * FROM view_equipment_repair_details WHERE phieu_sua_chua_id = %s", (repair_ticket_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod 
    def get_all_processed_equipment():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT thiet_bi_id FROM view_equipment_repair_details WHERE repair_status = 'CHO_DUYET' OR repair_status = 'CHUAN_BI'")
            r = cursor.fetchall()
            return [x['thiet_bi_id'] for x in r]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_existing_ticket(staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phieu_sua_chua WHERE nhan_vien_id = %s AND trang_thai = 'CHUAN_BI'", (staff_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remove_equipment_from_repair_ticket(phieu_sua_chua_id, thiet_bi_id):
        # Validate inputs
        if not phieu_sua_chua_id or not isinstance(phieu_sua_chua_id, int):
            print(f"Error: Invalid or missing phieu_sua_chua_id: {phieu_sua_chua_id}")
            return False
        if not thiet_bi_id or not isinstance(thiet_bi_id, int):
            print(f"Error: Invalid or missing thiet_bi_id: {thiet_bi_id}")
            return False

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            print(f"Calling remove_equipment_from_repair_ticket with phieu_sua_chua_id={phieu_sua_chua_id}, thiet_bi_id={thiet_bi_id}")
            cursor.callproc("remove_equipment_from_repair_ticket", [phieu_sua_chua_id, thiet_bi_id])
            
            # Fetch the result set from the procedure
            for result in cursor.stored_results():
                result_set = result.fetchone()
                print(f"Procedure result: success={result_set['success']}, error_code={result_set['error_code']}, message={result_set['message']}")
                
                if result_set['success'] == 0:
                    print(f"Procedure failed: {result_set['message']}")
                    conn.rollback()
                    return False
            
            conn.commit()
            print("Equipment removed from repair ticket successfully")
            return True

        except Exception as e:
            print(f"Error removing equipment from repair ticket: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def complete_repair_ticket(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                UPDATE phieu_sua_chua
                SET trang_thai = 'HOAN_THANH', ngay_ket_thuc = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (request_id,)
            )
            if cursor.rowcount == 0:
                return False
        
            conn.commit()
            return True

        except Exception as e:
            print(f"Error completing repair ticket: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def confirm_repair_ticket(request_id, role_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if role_id == 2:
                cursor.execute("UPDATE phieu_sua_chua SET trang_thai = 'CHO_DUYET' WHERE id = %s", (request_id,))
            else:
                cursor.execute("UPDATE phieu_sua_chua SET trang_thai = 'DA_DUYET' WHERE id = %s", (request_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating repair ticket status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_equipment_to_repair_ticket(staff_id, equipment_id, description=None, price=None):
        # Validate inputs
        if not staff_id or not isinstance(staff_id, str):
            print(f"Error: Invalid or missing staff_id: {staff_id}")
            return False
        if not equipment_id or not isinstance(equipment_id, int):
            print(f"Error: Invalid or missing equipment_id: {equipment_id}")
            return False

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            print(f"Calling them_thiet_bi_sua_chua with staff_id={staff_id}, equipment_id={equipment_id}, price={price}, description={description}")
            cursor.callproc("them_thiet_bi_sua_chua", [staff_id, equipment_id, price, description])
            
            # Fetch the result set from the procedure
            for result in cursor.stored_results():
                result_set = result.fetchone()
                print(f"Procedure result: success={result_set['success']}, error_code={result_set['error_code']}, message={result_set['message']}")
                
                if result_set['success'] == 0:
                    print(f"Procedure failed: {result_set['message']}")
                    conn.rollback()
                    return False
            
            conn.commit()
            print("Equipment added to repair ticket successfully")
            return True
        except Exception as e:
            print(f"Error adding equipment to repair ticket: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()



