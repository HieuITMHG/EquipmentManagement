from models.database import get_connection
from services.borrow_service import BorrowService

class EquipmentService:
    def get_borrowable_equipment_by_room(room_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM thiet_bi WHERE phong_id = %s AND trang_thai='CO_SAN' AND loai_thiet_bi='DI_DONG'", (room_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_borrowable_equipment(room_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM thiet_bi WHERE (phong_id = %s OR phong_id = 'HVCS') AND trang_thai='CO_SAN' AND loai_thiet_bi='DI_DONG'", (room_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_equipment(ten_thiet_bi, loai_thiet_bi, phong_id, anh=None):
        """Thêm thiết bị mới vào hệ thống"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('them_thiet_bi_moi', [
                ten_thiet_bi,      # p_ten_thiet_bi
                loai_thiet_bi,     # p_loai_thiet_bi
                phong_id,          # p_phong_id
                anh                # p_anh
            ])
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
    def delete_equipment_by_id(equipment_id):
        """Xóa thiết bị theo ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("DELETE FROM thiet_bi WHERE id = %s", (equipment_id,))
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
    def get_equipment_id_by_name_and_room(equipment_name, room_id):
        """Tìm equipment.id bằng equipment_name và room_id"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Truy vấn tìm kiếm thiết bị theo tên và room_id
            cursor.execute("""
                SELECT id 
                FROM equipment 
                WHERE equipment_name LIKE %s AND room_id = %s
            """, (f"%{equipment_name}%", room_id))  # Dùng LIKE để tìm kiếm gần đúng tên

            # Đọc kết quả
            result = cursor.fetchone()  # Trả về một kết quả nếu tìm thấy

            return result['id'] if result else None  # Trả về id nếu tìm thấy, ngược lại trả về None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_broken_equipment():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM thiet_bi WHERE trang_thai = 'HU_HONG'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search_equipment(phong_id=None, trang_thai=None, loai_thiet_bi=None, ten_thiet_bi=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM thiet_bi WHERE 1=1"
        params = []
        if phong_id:
            query += " AND phong_id LIKE %s"
            params.append(f"%{phong_id}%")
        if trang_thai:
            query += " AND trang_thai = %s"
            params.append(trang_thai)
        if loai_thiet_bi:
            query += " AND loai_thiet_bi = %s"
            params.append(loai_thiet_bi)
        if ten_thiet_bi:
            query += " AND ten_thiet_bi LIKE %s"
            params.append(f"%{ten_thiet_bi}%")
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_borrowing_equipment(nguoi_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            phieu_muon = BorrowService.get_existing_borrow_request(nguoi_id)
            if phieu_muon:
                id_phieu_muon = phieu_muon['id']
                cursor.execute("SELECT * FROM chi_tiet_muon WHERE phieu_muon_id = %s AND thoi_gian_tra_thuc_te IS NULL", (id_phieu_muon,))
                lst_equipment_id = [x['thiet_bi_id'] for x in cursor.fetchall()]
                if not lst_equipment_id:
                    return []  # Nếu không có thiết bị thì trả về mảng rỗng luôn

                # Nếu có thiết bị thì mới thực thi câu query
                query = "SELECT * FROM thiet_bi WHERE id IN (%s) AND trang_thai = 'CO_SAN'" % ','.join(['%s'] * len(lst_equipment_id))
                cursor.execute(query, lst_equipment_id)
                return cursor.fetchall()
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_borrowed_equipment(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM phieu_muon WHERE sinh_vien_id = %s AND trang_thai = 'DA_DUYET'", (user_id,))
            request = cursor.fetchone()
            if not request:
                return []
            room_id = request['phong_id']
            cursor.execute("SELECT * FROM thiet_bi WHERE phong_id = %s AND trang_thai = 'DANG_MUON'", (room_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_by_name_and_room(name, room_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT * FROM thiet_bi
                WHERE ten_thiet_bi = %s AND phong_id = %s
                LIMIT 1
            """
            cursor.execute(query, (name, room_id))
            equipment = cursor.fetchone()
            return equipment or {'quantity': 0, 'borrowing_quantity': 0, 'under_repair_quantity': 0}
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_equipment_info(id, ten_thiet_bi, trang_thai, loai_thiet_bi, phong_id, anh=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('cap_nhat_thong_tin_thiet_bi', [id, ten_thiet_bi, trang_thai, loai_thiet_bi, phong_id])
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating equipment: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_by_id(equipment_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM thiet_bi WHERE id = %s", (equipment_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_statistical_number():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            r = {}
            cursor.execute("SELECT COUNT(*) AS total FROM thiet_bi")
            r['total'] = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS broken FROM thiet_bi WHERE trang_thai = 'HU_HONG'")
            r['broken'] = cursor.fetchone()['broken']

            cursor.execute("SELECT COUNT(*) AS liquidated FROM thiet_bi WHERE trang_thai = 'DA_THANH_LY'")
            r['liquidated'] = cursor.fetchone()['liquidated']

            cursor.execute("SELECT COUNT(*) AS lost FROM thiet_bi WHERE trang_thai = 'DA_MAT'")
            r['lost'] = cursor.fetchone()['lost']

            cursor.execute("SELECT COUNT(*) AS borrowed FROM thiet_bi WHERE trang_thai = 'DANG_MUON'")
            r['borrowed'] = cursor.fetchone()['borrowed']

            return r
        except Exception as e:
            print(f"Error getting equipment statistics: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()

    
