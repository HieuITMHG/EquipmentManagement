from models.database import get_connection
from datetime import datetime

class InventoryService:
    @staticmethod
    def get_num_by_quarter(quarter_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Truy vấn tổng số thiết bị, số thiết bị hư, số thiết bị đang sửa, số thiết bị thanh lý
            cursor.execute("""
                SELECT 
                    SUM(d.total_devices) AS total_devices,
                    SUM(d.broken_count) AS total_broken,
                    SUM(d.repairing_count) AS total_repairing,
                    SUM(d.liquidated_count) AS total_liquidated
                FROM 
                    inventory_form i
                JOIN 
                    detail_inventory_form d ON i.id = d.inventory_form_id
                WHERE 
                    i.quarter_id = %s
            """, (quarter_id,))
            
            # Lấy kết quả trả về
            result = cursor.fetchone()
            
            # Trả về kết quả dưới dạng danh sách
            return [result['total_devices'], result['total_broken'], result['total_repairing'], result['total_liquidated']]
        
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_room_detail_by_quarter(quarter_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM inventory_summary WHERE quarter_id = %s", (quarter_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_quarters():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, year, quarter_number
                FROM quarter
                ORDER BY year DESC, quarter_number DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def get_or_create_quarter_id(start_date):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Check if a quarter exists
            cursor.execute("""
                SELECT id
                FROM quarter
                WHERE %s BETWEEN start_date AND end_date
            """, (start_date,))
            result = cursor.fetchone()
            if result:
                return result['id']

            # Create new quarter (6-month period)
            year = start_date.year
            month = start_date.month
            if 1 <= month <= 6:
                quarter_number = 1
                quarter_start = datetime(year, 1, 1).date()
                quarter_end = datetime(year, 6, 30).date()
            else:
                quarter_number = 2
                quarter_start = datetime(year, 7, 1).date()
                quarter_end = datetime(year, 12, 31).date()

            cursor.execute("""
                INSERT INTO quarter (year, quarter_number, start_date, end_date)
                VALUES (%s, %s, %s, %s)
            """, (year, quarter_number, quarter_start, quarter_end))
            quarter_id = cursor.lastrowid
            conn.commit()
            return quarter_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_inventory_form(staff_id, start_date, end_date, room_details):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Validate staff_id
            cursor.execute("""
                SELECT id
                FROM staff
                WHERE id = %s AND is_working = TRUE
            """, (staff_id,))
            if cursor.fetchone() is None:
                raise ValueError(f"Nhân viên với ID {staff_id} không tồn tại hoặc không đang làm việc.")

            # Get or create quarter_id
            quarter_id = InventoryService.get_or_create_quarter_id(start_date)

            # Minimal room validation
            rooms = InventoryService.get_all_rooms()
            room_ids = {room['id'] for room in rooms}
            submitted_room_ids = {detail['room_id'] for detail in room_details}
            if submitted_room_ids != room_ids:
                raise ValueError("Phải cung cấp dữ liệu cho tất cả các phòng.")

            for detail in room_details:
                if any(count < 0 for count in [
                    detail['total_devices'],
                    detail['broken_count'],
                    detail['repairing_count'],
                    detail['liquidated_count']
                ]):
                    raise ValueError(f"Dữ liệu số lượng cho phòng {detail['room_id']} không được âm.")
                if detail['broken_count'] + detail['repairing_count'] + detail['liquidated_count'] > detail['total_devices']:
                    raise ValueError(f"Tổng số thiết bị hỏng, đang sửa, và thanh lý cho phòng {detail['room_id']} không được vượt quá tổng số thiết bị.")

            # Insert into inventory_form
            cursor.execute("""
                INSERT INTO inventory_form (quarter_id, staff_id, start_date, end_date)
                VALUES (%s, %s, %s, %s)
            """, (quarter_id, staff_id, start_date, end_date))
            inventory_form_id = cursor.lastrowid
            if not inventory_form_id:
                raise ValueError("Không thể lấy ID của phiếu kiểm kê vừa tạo.")

            # Insert room details into detail_inventory_form
            for detail in room_details:
                cursor.execute("""
                    INSERT INTO detail_inventory_form (inventory_form_id, room_id, total_devices, broken_count, repairing_count, liquidated_count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    inventory_form_id,
                    detail['room_id'],
                    detail['total_devices'],
                    detail['broken_count'],
                    detail['repairing_count'],
                    detail['liquidated_count']
                ))

            conn.commit()
            return inventory_form_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def get_all_rooms():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM room ORDER BY id")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
