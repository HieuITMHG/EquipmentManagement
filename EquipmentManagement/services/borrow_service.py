import mysql.connector
from models.database import get_connection  # Đảm bảo bạn có hàm này để kết nối DB

class BorrowService:
    @staticmethod
    def create_borrow_request(student_id, equipment_ids, expect_returning_time):
        """
        Gọi stored procedure CreateBorrowRequestWithItems để tạo borrow request
        :param student_id: ID của sinh viên
        :param equipment_ids: Danh sách equipment_id (chuỗi, phân tách bởi dấu phẩy)
        :param expect_returning_time: Thời gian dự kiến trả
        :return: ID của borrow_request vừa tạo hoặc None nếu thất bại
        """
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
