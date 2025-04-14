import mysql.connector
from models.database import get_connection  # Đảm bảo bạn có hàm này để kết nối DB

class BorrowService:
    @staticmethod
    def create_borrow_request(student_id, equipment_ids, expect_returning_time, room_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Gọi stored procedure
            cursor.callproc('CreateBorrowRequestWithItems', (student_id, equipment_ids, expect_returning_time, room_id))
            
            # Lấy ID của borrow_request mới tạo
            cursor.execute("SELECT LAST_INSERT_ID()")
            borrow_request_id = cursor.fetchone()[0]
            
            conn.commit()  # Xác nhận thay đổi
            return borrow_request_id
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback()  # Hoàn tác nếu lỗi
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_borrow_equipment(student_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM BorrowDetails WHERE student_id = %s AND borrow_status='BORROWED' OR borrow_status='PENDING'", (student_id,))
            equipment = cursor.fetchall()
            return equipment
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_borrow_history(student_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM BorrowDetails WHERE student_id = %s", (student_id,))
            equipment = cursor.fetchall()
            return equipment
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_borrow_equipment_by_date(student_id, borrowing_date):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
            SELECT * FROM BorrowDetails 
            WHERE student_id = %s AND DATE(borrowing_time) = %s
            """
            cursor.execute(query, (student_id, borrowing_date))  # Chỉ so sánh theo ngày
            lst_borrow = cursor.fetchall()
            return lst_borrow
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_existing_borrow_request(student_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
            SELECT * FROM borrow_request
            WHERE student_id = %s AND status = 'PENDING'
            """
            # Bọc student_id trong tuple bằng cách thêm dấu phẩy
            cursor.execute(query, (student_id,))
            lst_borrow = cursor.fetchall()
            return lst_borrow
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_borrow_request(equipment_ids, borrow_request_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Convert equipment_ids list to comma-separated string if it's a list
            if isinstance(equipment_ids, list):
                equipment_ids = ','.join(map(str, equipment_ids))
                
            # Call the stored procedure
            cursor.callproc('AddEquipmentsToBorrowRequest', [borrow_request_id, equipment_ids])
            
            # Commit the changes
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback()  # Rollback in case of error
            return False
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def get_equipment_by_request_id(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM BorrowDetails WHERE borrow_request_id=%s", (request_id,))  
            lst_equipment = cursor.fetchall()
            return lst_equipment
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_pending_borrow_request():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM borrow_request WHERE status = 'PENDING'")  
            lst_borrow = cursor.fetchall()
            return lst_borrow
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def accept_borrow_request(request_id, staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Gọi stored procedure để chấp nhận yêu cầu mượn
            cursor.callproc('accept_borrow_request', [request_id, staff_id])
            # Commit để xác nhận thay đổi
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def reject_borrow_request(request_id, staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Gọi stored procedure để từ chối yêu cầu mượn
            cursor.callproc('reject_borrow_request', [request_id, staff_id])

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
    def get_accepted_or_returned_borrow_request():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
            SELECT borrow_request_id, student_id, staff_id, borrow_status, 
                   borrowing_time, expect_returning_time
            FROM BorrowDetails
            WHERE borrow_status = 'ACCEPTED' OR borrow_status = 'RETURNED'
            GROUP BY borrow_request_id
        """)  
            lst_borrow = cursor.fetchall()
            return lst_borrow
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def return_equi(request_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('return_equi', [request_id])
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_accepted_borrow_request():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT borrow_request_id, student_id, staff_id, borrow_status, 
                    borrowing_time, expect_returning_time
                FROM BorrowDetails
                WHERE borrow_status = 'ACCEPTED'
                GROUP BY borrow_request_id
            """)  
            lst_borrow = cursor.fetchall()
            return lst_borrow
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_returned_borrow_request():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT borrow_request_id, student_id, staff_id, borrow_status, 
                    borrowing_time, expect_returning_time
                FROM BorrowDetails
                WHERE borrow_status = 'RETURNED'
                GROUP BY borrow_request_id
            """)  
            lst_borrow = cursor.fetchall()
            return lst_borrow
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def cancel_borrow_equipment(equipment_id, borrow_request_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Gọi procedure return_equipment (đã tạo trong MySQL)
            cursor.callproc('cancel_borrow_equipment', [equipment_id, borrow_request_id])
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search_borrow_request_by_date_and_status(borrowing_date=None, status=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Query cơ bản lấy tất cả cột
            query = """
                SELECT *
                FROM borrow_request
                WHERE 1=1
            """
            params = []
            
            # Thêm điều kiện borrowing_date nếu có
            if borrowing_date:
                query += " AND DATE(borrowing_time) = %s"
                params.append(borrowing_date)
                
            # Thêm điều kiện status nếu có
            if status:
                query += " AND borrow_status = %s"
                params.append(status)
                
            # Thực thi query
            cursor.execute(query, params)
            borrow_requests = cursor.fetchall()
            return borrow_requests
            
        except Exception as e:
            print(f"Error searching borrow requests: {str(e)}")
            return []
            
        finally:
            cursor.close()
            conn.close()