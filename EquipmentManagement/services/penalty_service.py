from models.database import get_connection

class PenaltyService:
    @staticmethod
    def get_violation_by_id(student_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM PenaltyDetails WHERE student_id = %s", (student_id,))
            lst_violation = cursor.fetchall()
            return lst_violation
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def get_violation_by_in_ticket(penalty_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM PenaltyDetails WHERE penalty_ticket_id = %s", (penalty_id,))
            lst_violation = cursor.fetchall()
            return lst_violation
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_pending_penalty_ticket(staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM penalty_ticket WHERE status = 'PENDING' AND staff_id = %s", (staff_id,))
            lst_violation = cursor.fetchall()
            return lst_violation
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_history_penalty_ticket():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM penalty_ticket WHERE status IN ('ACCEPTED', 'REJECTED', 'COMPLETED') ORDER BY create_time DESC")
            lst_violation = cursor.fetchall()
            return lst_violation
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def create_penalty_ticket(student_id, staff_id, violation_ids, role):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Chuyển list[int] -> chuỗi CSV, ví dụ: '1,2,3'
            violation_ids_str = ",".join(str(v_id) for v_id in violation_ids)
            cursor.callproc('CreatePenaltyTicket', (student_id, staff_id, violation_ids_str, role))
            conn.commit()
            return True
        except Exception as e:
            print("Lỗi khi tạo phiếu phạt:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_penalty_ticket_by_id(ticket_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM penalty_ticket WHERE id = %s", (ticket_id,))
            conn.commit()
            return True
        except Exception as e:
            print("Lỗi khi xóa phiếu phạt:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def complete_penalty_ticket_by_id(ticket_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Cập nhật trạng thái thành COMPLETED dựa trên id, không kiểm tra trạng thái cũ
            cursor.execute(
                "UPDATE penalty_ticket SET status = 'COMPLETED' WHERE id = %s",
                (ticket_id,)
            )
            conn.commit()
            
            # Trả về True nếu có bản ghi được cập nhật, False nếu không
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Lỗi khi cập nhật phiếu phạt: {str(e)}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
