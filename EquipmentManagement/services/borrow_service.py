import mysql.connector
from models.database import get_connection  # Đảm bảo bạn có hàm này để kết nối DB

class BorrowService:
    @staticmethod
    def create_borrow_request(student_id, equipment_ids, expect_returning_time):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Gọi stored procedure
            cursor.callproc('CreateBorrowRequestWithItems', (student_id, equipment_ids, expect_returning_time))
            
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