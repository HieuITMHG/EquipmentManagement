import mysql.connector
from models.database import get_connection 
from helpers.helpers import get_expect_returning_time 

class BorrowService:
    @staticmethod
    def create_borrow_request_with_details(student_id, room_id, equipment_ids):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Bắt đầu transaction
            conn.start_transaction()

            # 1. Tạo phiếu mượn
            except_returning_time = get_expect_returning_time()
            cursor.execute(
                'INSERT INTO borrow_request (person_id, room_id, expect_returning_time) VALUES (%s, %s, %s)',
                (student_id, room_id, except_returning_time)
            )

            # Lấy ID của phiếu mượn vừa tạo
            borrow_id = cursor.lastrowid

            # 2. Tạo các chi tiết mượn
            for equipment_id in equipment_ids:
                cursor.execute(
                    "INSERT INTO borrow_item (borrow_request_id, equipment_id) VALUES (%s, %s)",
                    (borrow_id, equipment_id)
                )

            # Commit tất cả nếu không lỗi
            conn.commit()
            return True

        except Exception as e:
            # Rollback nếu có lỗi
            conn.rollback()
            return False

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
    def get_borrow_history(person_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM borrow_request WHERE person_id = %s", (person_id,))
            re = cursor.fetchall()
            for r in re:
                cursor.execute("SELECT equipment_id FROM borrow_item WHERE borrow_request_id = %s", (r['id'],))
                lst_e_id = [x['equipment_id'] for x in cursor.fetchall()]
                query = "SELECT * FROM equipment WHERE id IN (%s)"% ','.join(['%s'] * len(lst_e_id))
                cursor.execute(query, lst_e_id)
                r['equipments'] = cursor.fetchall()
            return re
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_borrow_history_by_date(person_id, bdate):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM borrow_request WHERE person_id = %s AND DATE(borrowing_time) = %s", (person_id, bdate))
            re = cursor.fetchall()
            print(re)
            for r in re:
                cursor.execute("SELECT equipment_id FROM borrow_item WHERE borrow_request_id = %s", (r['id'],))
                lst_e_id = [x['equipment_id'] for x in cursor.fetchall()]
                query = "SELECT * FROM equipment WHERE id IN (%s)"% ','.join(['%s'] * len(lst_e_id))
                cursor.execute(query, lst_e_id)
                r['equipments'] = cursor.fetchall()
            return re
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
            WHERE person_id = %s AND status = 'PENDING'
            """
            # Bọc student_id trong tuple bằng cách thêm dấu phẩy
            cursor.execute(query, (student_id,))
            lst_borrow = cursor.fetchone()
            return lst_borrow
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_equipment_to_request(equipment_ids, request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            for id in equipment_ids:
                cursor.execute("INSERT INTO borrow_item(borrow_request_id, equipment_id) VALUES(%s,%s)",(request_id,id))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            conn.rollback()
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
    def get_pending_borrow_request(person_id=None, borrowing_date=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM borrow_request WHERE status = 'PENDING'"
            params = []

            if person_id:
                query += " AND person_id = %s"
                params.append(person_id)

            if borrowing_date:
                query += " AND DATE(borrowing_time) = %s"
                params.append(borrowing_date)

            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_staff_borrow_history(person_id=None, borrowing_date=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM borrow_request WHERE status IN ('ACCEPTED', 'COMPLETED')"
            params = []

            if person_id:
                query += " AND person_id = %s"
                params.append(person_id)

            if borrowing_date:
                query += " AND DATE(borrowing_time) = %s"
                params.append(borrowing_date)

            cursor.execute(query, tuple(params))
            return cursor.fetchall()
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
            conn.commit()

            cursor.execute("SELECT * FROM borrow_item WHERE borrow_request_id=%s", (request_id,)) 
            lst_e_id = [x['equipment_id'] for x in cursor.fetchall()]
            
            # Update status equipment
            for id in lst_e_id:
                cursor.execute("UPDATE equipment SET status='BORROWED' WHERE id=%s", (id,))
            conn.commit()  # Chỉ commit 1 lần sau nhiều câu lệnh

            # Update các yêu cầu khác thành REJECTED nếu thiết bị đã mượn
            if lst_e_id:
                placeholders = ','.join(['%s'] * len(lst_e_id))
                query = f"SELECT borrow_request_id FROM borrow_item WHERE equipment_id IN ({placeholders})"
                cursor.execute(query, tuple(lst_e_id))
                lst_re_id = [x['borrow_request_id'] for x in cursor.fetchall()]

                for id in lst_re_id:
                    cursor.execute("UPDATE borrow_request SET status='REJECTED' WHERE id=%s AND status='PENDING'", (id,))
                conn.commit()  # Commit 1 lần luôn

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

    @staticmethod
    def remove_equipment_from_request(e_id, request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("DELETE FROM borrow_item WHERE borrow_request_id=%s AND equipment_id=%s",(request_id,e_id))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def count_equipment_in_request(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS quantity FROM borrow_item WHERE borrow_request_id = %s", (request_id,))
            result = cursor.fetchone()
            return result['quantity'] if result else 0
        except Exception as e:
            print(e)
            return 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_borrow_request(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("DELETE FROM borrow_request WHERE ID = %s",(request_id,))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_in_borrow_request(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM BorrowDetails WHERE borrow_request_id = %s", (request_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()