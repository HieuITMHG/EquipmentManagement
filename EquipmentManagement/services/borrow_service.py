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