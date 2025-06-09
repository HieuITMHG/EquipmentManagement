from models.database import get_connection
from datetime import datetime
from dateutil import parser

class InventoryService:
    @staticmethod
    def get_num_by_inventory(phieu_kiem_ke_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT 
                SUM(ct.tong_so) AS total_devices,
                SUM(ct.so_luong_hong) AS total_broken,
                SUM(ct.so_luong_sua_chua) AS total_repairing,
                SUM(ct.so_luong_thanh_ly) AS total_liquidated
            FROM phieu_kiem_ke pk
            JOIN chi_tiet_kiem_ke ct ON pk.id = ct.phieu_kiem_ke_id
            WHERE pk.id = %s
            """
            cursor.execute(query, (phieu_kiem_ke_id,))
            result = cursor.fetchone()
            total_devices = result['total_devices'] if result and result['total_devices'] else 0
            total_broken = result['total_broken'] if result and result['total_broken'] else 0
            total_repairing = result['total_repairing'] if result and result['total_repairing'] else 0
            total_liquidated = result['total_liquidated'] if result and result['total_liquidated'] else 0
            return (total_devices, total_broken, total_repairing, total_liquidated)
        except Exception as e:
            print(f"Error in get_num_by_inventory: {e}")
            return (0, 0, 0, 0)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def get_room_detail_by_inventory(phieu_kiem_ke_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT 
                ct.phong_id AS room_id,
                ct.tong_so AS total_devices,
                ct.so_luong_hong AS broken_count,
                ct.so_luong_sua_chua AS repairing_count,
                ct.so_luong_thanh_ly AS liquidated_count
            FROM phieu_kiem_ke pk
            JOIN chi_tiet_kiem_ke ct ON pk.id = ct.phieu_kiem_ke_id
            WHERE pk.id = %s
            """
            cursor.execute(query, (phieu_kiem_ke_id,))
            room_details = cursor.fetchall()
            return room_details
        except Exception as e:
            print(f"Error in get_room_detail_by_inventory: {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def get_all_inventories():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT 
                id,
                thoi_gian_bat_dau AS start_date,
                thoi_gian_ket_thuc AS end_date
            FROM phieu_kiem_ke
            ORDER BY thoi_gian_bat_dau DESC
            """
            cursor.execute(query)
            inventories = cursor.fetchall()
            # Format dates as DD/MM/YYYY HH:MM
            for inv in inventories:
                inv['start_date'] = inv['start_date'].strftime('%d/%m/%Y %H:%M') if inv['start_date'] else ''
                inv['end_date'] = inv['end_date'].strftime('%d/%m/%Y %H:%M') if inv['end_date'] else 'Chưa kết thúc'
            return inventories
        except Exception as e:
            print(f"Error in get_all_inventories: {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def get_all_rooms():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, suc_chua, tang, khu FROM phong"
            cursor.execute(query)
            rooms = cursor.fetchall()
            return rooms
        except Exception as e:
            print(f"Error in get_all_rooms: {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def create_inventory_form(staff_id, start_date, end_date, room_details):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM nhan_vien WHERE id = %s AND dang_lam_viec = TRUE", (staff_id,))
            if not cursor.fetchone():
                raise ValueError("Nhân viên không tồn tại hoặc không đang làm việc.")
            cursor.execute(
                """
                INSERT INTO phieu_kiem_ke (nhan_vien_id, thoi_gian_bat_dau, thoi_gian_ket_thuc)
                VALUES (%s, %s, %s)
                """,
                (staff_id, start_date, end_date)
            )
            phieu_kiem_ke_id = cursor.lastrowid
            for room in room_details:
                cursor.execute(
                    """
                    CALL them_chi_tiet_kiem_ke(%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        phieu_kiem_ke_id,
                        room['room_id'],
                        room['total_devices'],
                        '',
                        room['broken_count'],
                        room['repairing_count'],
                        room['liquidated_count']
                    )
                )
            conn.commit()
        except Exception as e:
            if conn is not None:
                conn.rollback()
            raise e
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def update_inventory_form(phieu_kiem_ke_id, start_date, end_date, room_details):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Validate phieu_kiem_ke_id exists
            cursor.execute("SELECT id FROM phieu_kiem_ke WHERE id = %s", (phieu_kiem_ke_id,))
            if not cursor.fetchone():
                raise ValueError("Phiếu kiểm kê không tồn tại.")

            # Update phieu_kiem_ke
            cursor.execute(
                """
                UPDATE phieu_kiem_ke
                SET thoi_gian_bat_dau = %s, thoi_gian_ket_thuc = %s
                WHERE id = %s
                """,
                (start_date, end_date, phieu_kiem_ke_id)
            )

            # Delete existing chi_tiet_kiem_ke records for this phieu_kiem_ke_id
            cursor.execute("DELETE FROM chi_tiet_kiem_ke WHERE phieu_kiem_ke_id = %s", (phieu_kiem_ke_id,))

            # Insert updated room details using stored procedure
            for room in room_details:
                cursor.execute(
                    """
                    CALL them_chi_tiet_kiem_ke(%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        phieu_kiem_ke_id,
                        room['room_id'],
                        room['total_devices'],
                        '',  # ghi_chu
                        room['broken_count'],
                        room['repairing_count'],
                        room['liquidated_count']
                    )
                )

            conn.commit()
        except Exception as e:
            if conn is not None:
                conn.rollback()
            raise e
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()