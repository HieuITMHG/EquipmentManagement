from models.database import get_connection 
from datetime import datetime

class BorrowService:
    @staticmethod
    def create_borrow_request_with_details(student_id, equipment_ids):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            equipment_ids_str = ",".join(str(eid) for eid in equipment_ids)
            cursor.callproc("lap_phieu_muon", [equipment_ids_str, student_id])
            for result in cursor.stored_results():
                res = result.fetchone()
                if res:
                    success, error_code, message = res[0], res[1], res[2]
                    if success == 1:
                        conn.commit()
                        return True, None, None
                    else:
                        print(f"[lap_phieu_muon] {error_code}: {message}")
                        conn.rollback()
                        return False, message, error_code
            conn.rollback()
            return False, "Không xác định lỗi khi tạo phiếu mượn", "UNKNOWN"
        except Exception as e:
            conn.rollback()
            print("❌ Lỗi khi gọi procedure lap_phieu_muon:", str(e))
            return False, str(e), "EXCEPTION"
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
            cursor.execute("SELECT * FROM phieu_muon WHERE sinh_vien_id = %s", (person_id,))
            re = cursor.fetchall()
            for r in re:
                cursor.execute("SELECT thiet_bi_id FROM chi_tiet_muon WHERE phieu_muon_id = %s", (r['id'],))
                lst_e_id = [x['thiet_bi_id'] for x in cursor.fetchall()]
                if lst_e_id:
                    query = "SELECT * FROM thiet_bi WHERE id IN (%s)" % ','.join(['%s'] * len(lst_e_id))
                    cursor.execute(query, lst_e_id)
                    r['equipments'] = cursor.fetchall()
                else:
                    r['equipments'] = []
            return re
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_borrow_history_by_date(person_id, bdate):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phieu_muon WHERE sinh_vien_id = %s AND DATE(ca) = %s", (person_id, bdate))
            re = cursor.fetchall()
            for r in re:
                cursor.execute("SELECT thiet_bi_id FROM chi_tiet_muon WHERE phieu_muon_id = %s", (r['id'],))
                lst_e_id = [x['thiet_bi_id'] for x in cursor.fetchall()]
                if lst_e_id:
                    query = "SELECT * FROM thiet_bi WHERE id IN (%s)" % ','.join(['%s'] * len(lst_e_id))
                    cursor.execute(query, lst_e_id)
                    r['equipments'] = cursor.fetchall()
                else:
                    r['equipments'] = []
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
            SELECT * FROM phieu_muon
            WHERE sinh_vien_id = %s
            AND DATE(ca) = CURDATE()
            AND (
                (TIME(NOW()) BETWEEN '06:00:00' AND '10:15:00' AND TIME(ca) = '06:00:00')
                OR
                (TIME(NOW()) BETWEEN '12:00:00' AND '16:15:00' AND TIME(ca) = '12:00:00')
            )
            """
            cursor.execute(query, (student_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_equipment_to_request(equipment_ids, request_id, phong_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            equipment_id_str = ",".join(str(id) for id in equipment_ids)
            cursor.callproc('them_thiet_bi_vao_phieu_muon', [request_id, equipment_id_str, phong_id])
            for result in cursor.stored_results():
                res = result.fetchone()
                if res:
                    success, error_code, message = res[0], res[1], res[2]
                    if success == 1:
                        conn.commit()
                        return True, None, None
                    else:
                        print(f"[them_thiet_bi_vao_phieu_muon] {error_code}: {message}")
                        conn.rollback()
                        return False, message, error_code
            conn.rollback()
            return False, "Không xác định lỗi khi thêm thiết bị vào phiếu mượn", "UNKNOWN"
        except Exception as e:
            print(f"Lỗi trong Python: {e}")
            conn.rollback()
            return False, str(e), "EXCEPTION"
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
    def get_pending_borrow_requests():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """SELECT DISTINCT pm.*
                    FROM phieu_muon pm
                    JOIN chi_tiet_muon ctm ON pm.id = ctm.phieu_muon_id
                    JOIN thiet_bi tb ON ctm.thiet_bi_id = tb.id
                    WHERE tb.trang_thai = 'CO_SAN'
                    AND (
                        (TIME(pm.ca) BETWEEN '06:00:00' AND '10:15:00')
                        OR (TIME(pm.ca) BETWEEN '12:00:00' AND '16:15:00')
                    )
                    AND DATE(pm.ca) = CURRENT_DATE()
                    """
            cursor.execute(query)
            requests = cursor.fetchall()
            for req in requests:
                req['equipments'] = BorrowService.get_equipment_in_pending_borrow_request(req['id'])
            return requests
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_accepted_borrow_requests():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
            SELECT id, sinh_vien_id, nhan_vien_id, phong_id, ca, 
                   thoi_gian_tra_du_kien, trang_thai
            FROM phieu_muon
            WHERE trang_thai = 'DA_DUYET'
              AND (
                  (TIME(ca) BETWEEN '06:00:00' AND '10:15:00')
                  OR (TIME(ca) BETWEEN '12:00:00' AND '16:15:00')
              )
              AND DATE(ca) = CURDATE()
            """)
            requests = cursor.fetchall()
            for req in requests:
                req['equipments'] = BorrowService.get_equipment_in_borrow_request(req['id'])
            return requests
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_in_borrow_request(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT ctm.*, tb.*
                FROM chi_tiet_muon ctm
                JOIN thiet_bi tb ON ctm.thiet_bi_id = tb.id 
                WHERE ctm.phieu_muon_id = %s
            """, (request_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_in_pending_borrow_request(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT ctm.*, tb.*
                FROM chi_tiet_muon ctm
                JOIN thiet_bi tb ON ctm.thiet_bi_id = tb.id 
                WHERE ctm.phieu_muon_id = %s AND ctm.thoi_gian_tra_thuc_te IS NULL
            """, (request_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_historical_borrow_requests(limit=100):
        """
        Fetch up to 100 borrow requests from past time slots (6:00-10:15 or 12:00-16:15),
        excluding the current time slot, sorted by ca in descending order (most recent first).
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT id, sinh_vien_id, nhan_vien_id, phong_id, ca, 
                       thoi_gian_tra_du_kien, trang_thai
                FROM phieu_muon
                WHERE 
                    -- Ensure ca is in valid time slots
                    (
                        TIME(ca) BETWEEN '06:00:00' AND '10:15:00'
                        OR TIME(ca) BETWEEN '12:00:00' AND '16:15:00'
                    )
                    -- Exclude current time slot
                    AND (
                        -- If current time is in morning slot, exclude today's morning slot
                        NOT (
                            TIME(NOW()) BETWEEN '06:00:00' AND '10:15:00'
                            AND TIME(ca) BETWEEN '06:00:00' AND '10:15:00'
                            AND DATE(ca) = CURDATE()
                        )
                        -- If current time is in afternoon slot, exclude today's afternoon slot
                        AND NOT (
                            TIME(NOW()) BETWEEN '12:00:00' AND '16:15:00'
                            AND TIME(ca) BETWEEN '12:00:00' AND '16:15:00'
                            AND DATE(ca) = CURDATE()
                        )
                        -- Include all past days
                        OR DATE(ca) < CURDATE()
                    )
                ORDER BY ca DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            requests = cursor.fetchall()
            
            # Fetch equipment for each borrow request
            for req in requests:
                req['equipments'] = BorrowService.get_equipment_in_borrow_request(req['id'])
            
            return requests
        except Exception as e:
            print(f"Error fetching historical borrow requests: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def accept_borrow_request(request_id, staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for result set
        try:            
            cursor.callproc('xac_nhan_phieu_muon', (request_id, staff_id,))

            result = next(cursor.stored_results()).fetchall()[0]
            
            # Check the procedure's success status
            if result['success'] == 1:
                conn.commit()
                return True
            else:
                conn.rollback()
                print(f"Error logic: {result['error_code']} - {result['message']}")
                return False
                
        except Exception as e:
            conn.rollback()
            print(f"Error code: {e}")
            return False
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
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM chi_tiet_muon WHERE phieu_muon_id=%s AND thiet_bi_id=%s", (request_id, e_id))
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
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) AS quantity FROM chi_tiet_muon WHERE phieu_muon_id = %s", (request_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(e)
            return 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_borrow_request(request_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM phieu_muon WHERE id = %s", (request_id,))
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
    def accept_one_equipment(equipment_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('duyet_mot_thiet_bi', [equipment_id])
            conn.commit()
            return True
        except Exception as e:
            print("Error approving equipment borrow:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def reject_one_equipment(equipment_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('tu_choi_mot_thiet_bi', [equipment_id])
            conn.commit()
            return True
        except Exception as e:
            print("Error deleting equipment borrow detail:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_equipment_status(equipment_id, new_status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE thiet_bi
                SET trang_thai = %s
                WHERE id = %s
            """
            cursor.execute(query, (new_status, equipment_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error updating equipment status to lost:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def update_damaged_equipment(equipment_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Cập nhật trạng thái thiết bị
            cursor.execute(
                "UPDATE thiet_bi SET trang_thai = 'HU_HONG' WHERE id = %s",
                (equipment_id,)
            )

            # Cập nhật thời gian trả thực tế thành thời gian hiện tại
            current_time = datetime.now()
            cursor.execute(
                "UPDATE chi_tiet_muon SET thoi_gian_tra_thuc_te = %s WHERE thiet_bi_id = %s",
                (current_time, equipment_id)
            )

            conn.commit()
            return True
        except Exception as e:
            print("Error updating damaged equipment:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def return_equipment(phieu_muon_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('tra_thiet_bi', [phieu_muon_id])
            conn.commit()
            print(f"Trả thiết bị cho phiếu mượn {phieu_muon_id} thành công.")
            return True
        except Exception as e:
            print(f"Lỗi khi trả thiết bị cho phiếu mượn {phieu_muon_id}:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def return_one_equipment(equipment_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Cập nhật trạng thái thiết bị
            cursor.execute(
                "UPDATE thiet_bi SET trang_thai = 'CO_SAN' WHERE id = %s",
                (equipment_id,)
            )

            # Cập nhật thời gian trả thực tế thành thời gian hiện tại
            current_time = datetime.now()
            cursor.execute(
                "UPDATE chi_tiet_muon SET thoi_gian_tra_thuc_te = %s WHERE thiet_bi_id = %s",
                (current_time, equipment_id)
            )

            conn.commit()
            return True
        except Exception as e:
            print("Error return one equipment:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def reject_borrow_request(request_id):
        print("từ chối nè")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('tu_choi_phieu_muon', (request_id,))
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
    def add_addition_equipment(equipment_ids, request_id, phong_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Validate inputs
            if not equipment_ids or not request_id or not phong_id:
                return False, "Missing required parameters", "INVALID_INPUT"

            # Check if the borrow request exists and is in a valid state (e.g., Đã duyệt)
            cursor.execute("SELECT trang_thai FROM phieu_muon WHERE id = %s", (request_id,))
            request = cursor.fetchone()
            if not request:
                return False, "Phiếu mượn không tồn tại", "REQUEST_NOT_FOUND"
            if request[0] != "DA_DUYET":
                return False, "Phiếu mượn không ở trạng thái Đã duyệt", "INVALID_REQUEST_STATE"

            # Check if equipment exists, belongs to the room, and is available
            for equipment_id in equipment_ids:
                cursor.execute(
                    "SELECT trang_thai, phong_id FROM thiet_bi WHERE id = %s",
                    (equipment_id,)
                )
                equipment = cursor.fetchone()
                if not equipment:
                    conn.rollback()
                    return False, f"Thiết bị ID {equipment_id} không tồn tại", "EQUIPMENT_NOT_FOUND"
                if equipment[1] != phong_id:
                    conn.rollback()
                    return False, f"Thiết bị ID {equipment_id} không thuộc phòng {phong_id}", "EQUIPMENT_WRONG_ROOM"
                if equipment[0] != "CO_SAN":
                    conn.rollback()
                    return False, f"Thiết bị ID {equipment_id} không khả dụng", "EQUIPMENT_NOT_AVAILABLE"

            # Add equipment to chi_tiet_muon and update equipment status
            for equipment_id in equipment_ids:
                # Insert into chi_tiet_muon
                cursor.execute(
                    """
                    INSERT INTO chi_tiet_muon (phieu_muon_id, thiet_bi_id)
                    VALUES (%s, %s)
                    """,
                    (request_id, equipment_id)
                )
                # Update equipment status to DANG_MUON
                cursor.execute(
                    """
                    UPDATE thiet_bi
                    SET trang_thai = %s
                    WHERE id = %s
                    """,
                    ("DANG_MUON", equipment_id)
                )

            # Commit the transaction
            conn.commit()
            return True, None, None

        except Exception as e:
            print(f"Lỗi trong Python: {e}")
            conn.rollback()
            return False, str(e), "DATABASE_ERROR"
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            conn.rollback()
            return False, str(e), "EXCEPTION"
        finally:
            cursor.close()
            conn.close()