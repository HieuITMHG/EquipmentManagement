from models.database import get_connection

class EquipmentService:
    @staticmethod
    def get_all_equipment():
        """Lấy danh sách tất cả thiết bị từ DB"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment")
            return cursor.fetchall()  # Trả về trực tiếp danh sách dictionary
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_by_mtype(mtype):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE management_type = %s", (mtype,))
            return cursor.fetchall()  # Trả về trực tiếp danh sách dictionary
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def get_equipment_by_id(equipment_id):
        """Lấy thiết bị theo ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE id = %s", (equipment_id,))
            equipment = cursor.fetchone()
            return equipment if equipment else None  # Trả về None nếu không tìm thấy
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_by_room(room_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE room_id = %s", (room_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_borrowable_equipment_by_room(room_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM equipment WHERE room_id = %s AND status='AVAILABLE' AND equipment_type='MOBILE'", (room_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_equipment(new_name, new_type, new_management_type, new_room, new_quantity, new_image_url):
        """Thêm thiết bị mới vào hệ thống"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Gọi stored procedure để thêm thiết bị mới
            cursor.callproc('create_equipment', [
                new_name,             # p_equipment_name
                new_type,             # p_equipment_type ('MOBILE' hoặc 'FIXED')
                new_management_type,  # p_management_type ('QUANTITY' hoặc 'INDIVIDUAL')
                new_room,             # p_room_id
                new_quantity,         # p_quantity
                new_image_url         # p_image_url (ví dụ: 'img/filename.png')
            ])

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
    def delete_equipment_by_id(equipment_id):
        """Xóa thiết bị theo ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Gọi stored procedure để xóa thiết bị
            cursor.execute("DELETE FROM equipment WHERE id = %s", (equipment_id,))

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
            cursor.execute("SELECT * FROM equipment WHERE broken_quantity > 0")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search_equipment(room_id=None, status=None, equipment_type=None, equipment_name=None, management_type=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM equipment WHERE 1=1"
        params = []

        if room_id:
            query += " AND room_id LIKE %s"
            params.append(f"%{room_id}%")

        if status:
            query += " AND status = %s"
            params.append(status)

        if equipment_type:
            query += " AND equipment_type = %s"
            params.append(equipment_type)

        if equipment_name:
            query += " AND equipment_name LIKE %s"
            params.append(f"%{equipment_name}%")
        
        if management_type:
            query += " AND management_type = %s"
            params.append(management_type)

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
            cursor.execute("SELECT * FROM borrow_request WHERE person_id = %s AND status = 'PENDING'", (nguoi_id,))
            phieu_muon = cursor.fetchone()
            if phieu_muon:
                id_phieu_muon = phieu_muon['id']
                cursor.execute("SELECT * FROM borrow_item WHERE borrow_request_id = %s", (id_phieu_muon,))
                lst_equipment_id = [x['equipment_id'] for x in cursor.fetchall()]
                if not lst_equipment_id:
                    return []  # Nếu không có thiết bị thì trả về mảng rỗng luôn

                # Nếu có thiết bị thì mới thực thi câu query
                query = "SELECT * FROM equipment WHERE ID IN (%s)" % ','.join(['%s'] * len(lst_equipment_id))
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
            cursor.execute("SELECT * FROM borrow_request WHERE person_id = %s AND status = 'ACCEPTED'", (user_id,))
            request = cursor.fetchone()
            if not request:
                return []
            room_id = request['room_id']
            cursor.execute("SELECT * FROM equipment WHERE room_id = %s AND status = 'BORROWED'", (room_id,))
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
                SELECT * FROM equipment
                WHERE equipment_name = %s AND room_id = %s
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
    def update_quantity(equipment_id, new_quantity):
        """Cập nhật số lượng thiết bị"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE equipment SET quantity = %s WHERE id = %s"
            cursor.execute(query, (new_quantity, equipment_id))
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
    def update_equipment_info(id, name, status, room_id, image_url=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('update_equipment_info', [id, name, status, room_id, image_url])
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
    def update_equipment_quantities(equipment_id, new_quantity, new_broken_quantity):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE equipment
                SET quantity = %s,
                    broken_quantity = %s
                WHERE id = %s
            """
            cursor.execute(query, (new_quantity, new_broken_quantity, equipment_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating quantities: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_statistical_number():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            r = {}

            cursor.execute("SELECT COUNT(*) AS so_don_le FROM equipment WHERE management_type = 'INDIVIDUAL'")
            so_don_le = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(quantity) AS so_nhieu FROM equipment WHERE management_type = 'QUANTITY'")
            so_nhieu = cursor.fetchone()[0]

            r['total'] = int(so_don_le + so_nhieu)

            cursor.execute("SELECT SUM(broken_quantity) AS so_hong FROM equipment")
            r['broken_quantity'] = int(cursor.fetchone()[0])

            cursor.execute("SELECT SUM(under_repair_quantity) AS so_sua FROM equipment")
            r['under_repair_quantity'] = int(cursor.fetchone()[0])

            cursor.execute("SELECT COUNT(borrow_item_id) AS so_muon FROM BorrowDetails WHERE borrow_status = 'ACCEPTED'")
            r['borrowing_quantity'] = int(cursor.fetchone()[0])

            return r
        except Exception as e:
            print(f"Error getting equipment statistics: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def allocate_equipment(equipment_id, allocate_quantity):
        if allocate_quantity <= 0:
            return False, "Số lượng cấp phải lớn hơn 0"

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Fetch the equipment to get its equipment_name
            cursor.execute(
                "SELECT equipment_name FROM equipment WHERE id = %s",
                (equipment_id,)
            )
            equipment = cursor.fetchone()
            
            if not equipment:
                return False, "Không tìm thấy thiết bị"

            # Fetch warehouse equipment (same equipment_name, room_id='HVCS')
            cursor.execute(
                "SELECT id, quantity FROM equipment WHERE equipment_name = %s AND room_id = %s",
                (equipment['equipment_name'], 'HVCS')
            )
            warehouse_equipment = cursor.fetchone()
            
            if not warehouse_equipment:
                return False, "Không tìm thấy thiết bị trong kho (HVCS)"
            
            if warehouse_equipment['quantity'] < allocate_quantity:
                return False, "Số lượng trong kho không đủ để cấp"
            
            # Increase quantity of the target equipment
            cursor.execute(
                "UPDATE equipment SET quantity = quantity + %s WHERE id = %s",
                (allocate_quantity, equipment_id)
            )
            
            # Decrease quantity in the warehouse
            cursor.execute(
                "UPDATE equipment SET quantity = quantity - %s WHERE id = %s",
                (allocate_quantity, warehouse_equipment['id'])
            )
            
            # Commit transaction
            conn.commit()
            return True, "Cấp thiết bị thành công"
            
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi khi cấp thiết bị: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def retrieve_equipment(equipment_id, available_quantity, broken_quantity, under_repair_quantity):
        if available_quantity < 0 or broken_quantity < 0 or under_repair_quantity < 0:
            return False, "Số lượng thu hồi phải lớn hơn hoặc bằng 0"

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Fetch the equipment to get its equipment_name and quantities
            cursor.execute(
                "SELECT equipment_name, quantity, broken_quantity, under_repair_quantity FROM equipment WHERE id = %s",
                (equipment_id,)
            )
            equipment = cursor.fetchone()
            
            if not equipment:
                return False, "Không tìm thấy thiết bị"

            # Check if room has enough quantities
            if (equipment['quantity'] < available_quantity or
                equipment['broken_quantity'] < broken_quantity or
                equipment['under_repair_quantity'] < under_repair_quantity):
                return False, "Số lượng trong phòng không đủ để thu hồi"

            # Fetch warehouse equipment (same equipment_name, room_id='HVCS')
            cursor.execute(
                "SELECT id, quantity, broken_quantity, under_repair_quantity FROM equipment WHERE equipment_name = %s AND room_id = %s",
                (equipment['equipment_name'], 'HVCS')
            )
            warehouse_equipment = cursor.fetchone()
            
            if not warehouse_equipment:
                return False, "Không tìm thấy thiết bị trong kho (HVCS)"

            # Decrease quantities in the room
            cursor.execute(
                """
                UPDATE equipment 
                SET quantity = quantity - %s,
                    broken_quantity = broken_quantity - %s,
                    under_repair_quantity = under_repair_quantity - %s
                WHERE id = %s
                """,
                (available_quantity, broken_quantity, under_repair_quantity, equipment_id)
            )

            # Increase quantities in the warehouse
            cursor.execute(
                """
                UPDATE equipment 
                SET quantity = quantity + %s,
                    broken_quantity = broken_quantity + %s,
                    under_repair_quantity = under_repair_quantity + %s
                WHERE id = %s
                """,
                (available_quantity, broken_quantity, under_repair_quantity, warehouse_equipment['id'])
            )

            # Commit transaction
            conn.commit()
            return True, "Thu hồi thiết bị thành công"
            
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi khi thu hồi thiết bị: {str(e)}"
        finally:
            cursor.close()
            conn.close()