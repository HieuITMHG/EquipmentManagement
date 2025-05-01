import mysql.connector
from models.database import get_connection  # Đảm bảo bạn có hàm này để kết nối DB

class LiquidationSlipService:
    @staticmethod
    def create_liquidation_slip(staff_id, lst_equipment_id, role):
        conn = get_connection()  # Giả định hàm này đã được định nghĩa để lấy kết nối DB
        cursor = conn.cursor()
        try:
            # Chuyển danh sách equipment_id thành chuỗi phân tách bằng dấu phẩy
            equipment_ids_str = ','.join(map(str, lst_equipment_id))
            
            # Gọi stored procedure với 3 tham số
            cursor.callproc('CreateLiquidationSlip', (staff_id, equipment_ids_str, role))
            
            # Lấy ID của liquidation_slip mới tạo
            cursor.execute("SELECT LAST_INSERT_ID()")
            liquidation_slip_id = cursor.fetchone()[0]
            
            conn.commit()  # Xác nhận thay đổi
            return liquidation_slip_id
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback()  # Hoàn tác nếu lỗi
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_pending_repair_ticket():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM liquidation_slip WHERE status = 'PENDING'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_liquidation_slip(staff_id=None, status=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if staff_id != None:
                cursor.execute("SELECT * FROM liquidation_slip WHERE staff_id = %s AND status = %s", (staff_id, status))
            else:
                cursor.execute("SELECT * FROM liquidation_slip WHERE status = %s", (status,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_total_cost(ticket_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT SUM(price) AS total_cost FROM detail_liquidation_slip WHERE liquidation_slip_id = %s", (ticket_id,))
            result = cursor.fetchone()  # Lấy hàng đầu tiên (chỉ có một hàng vì SUM)
            
            # Kiểm tra và trả về tổng dưới dạng số nguyên
            if result and result['total_cost'] is not None:
                return int(result['total_cost'])
            return 0  # Trả về 0 nếu không có dữ liệu hoặc tổng là NULL
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_history_liquidation_slip(start_date=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM liquidation_slip WHERE status IN ('ACCEPTED', 'COMPLETED', 'REJECTED')"
            params = []
            
            if start_date:
                query += " AND DATE(liquidation_date) = %s"
                params.append(start_date)
                
            query += " ORDER BY liquidation_date DESC"
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_liquidation_slip(liquidation_slip_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Thực hiện lệnh DELETE với liquidation_slip_id
            cursor.execute("DELETE FROM liquidation_slip WHERE id = %s", (liquidation_slip_id,))
            
            # Kiểm tra xem có bản ghi nào bị xóa không
            if cursor.rowcount > 0:
                conn.commit()  # Xác nhận thay đổi
                return True
            else:
                conn.rollback()  # Hoàn tác nếu không có bản ghi nào bị xóa
                return False
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback()  # Hoàn tác nếu có lỗi
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_in_liquidation(liquidation_slip_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM v_liquidation_full_details WHERE liquidation_id = %s", (liquidation_slip_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def complete_liquidation_slip(liquidation_slip_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('CompleteLiquidationSlip', [liquidation_slip_id])
            conn.commit()
            return True  # ✅ Procedure chạy thành công
        except Exception as e:
            print(f"Error completing liquidation slip: {e}")
            return False  # ❌ Có lỗi xảy ra
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def reject_liquidation_slip(ticket_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE liquidation_slip SET status = 'REJECTED' WHERE id = %s", (ticket_id,))
            conn.commit()
            return cursor.rowcount > 0  
        finally:
            cursor.close()
            conn.close()

    # Mới
    @staticmethod
    def create_liquidation_slip_with_equipment(staff_id, equipment_id, quantity=1, description=None, price=None, status='PREPARING'):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Step 1: Create a new liquidation slip
            query_slip = """
                INSERT INTO liquidation_slip (staff_id, status)
                VALUES (%s, %s)
            """
            cursor.execute(query_slip, (staff_id, status))
            
            # Get the ID of the newly created slip
            slip_id = cursor.lastrowid
            print("djfhkdjfkdsfhds")
            print(slip_id)
            
            # Step 2: Add the equipment to the slip
            query = """
                INSERT INTO detail_liquidation_slip (liquidation_slip_id, equipment_id, quantity, description, price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (slip_id, equipment_id, quantity, description, price))
            conn.commit()
            return True
        
        except Exception as e:
            print(f"Error creating liquidation slip: {e}")
            conn.rollback()
            return False
        
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remove_equipment_from_slip(liquidation_slip_id, equipment_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Step 1: Delete the equipment from detail_liquidation_slip
            query_delete = """
                DELETE FROM detail_liquidation_slip
                WHERE liquidation_slip_id = %s AND equipment_id = %s
            """
            cursor.execute(query_delete, (liquidation_slip_id, equipment_id))
            equipment_deleted = cursor.rowcount  # Number of rows deleted (0 or 1)

            # Step 2: Check if any equipment items remain in the slip
            query_count = """
                SELECT COUNT(*) AS item_count
                FROM detail_liquidation_slip
                WHERE liquidation_slip_id = %s
            """
            cursor.execute(query_count, (liquidation_slip_id,))
            item_count = cursor.fetchone()['item_count']

            # Step 3: If no items remain, delete the liquidation slip
            slip_deleted = False
            if item_count == 0:
                query_delete_slip = """
                    DELETE FROM liquidation_slip
                    WHERE id = %s
                """
                cursor.execute(query_delete_slip, (liquidation_slip_id,))
                slip_deleted = cursor.rowcount > 0  # True if slip was deleted

            # Step 4: Update equipment status (revert to AVAILABLE if not liquidated)
            cursor.execute(
                """
                UPDATE equipment
                SET status = 'AVAILABLE'
                WHERE id = %s AND status = 'BROKEN'
                """,
                (equipment_id,)
            )
            
            # Commit the transaction
            conn.commit()
            return {
                'success': True,
                'equipment_deleted': equipment_deleted,
                'slip_deleted': slip_deleted,
                'error': None
            }

        except Exception as e:
            print(f"Error removing equipment from slip: {e}")
            conn.rollback()
            return {
                'success': False,
                'equipment_deleted': 0,
                'slip_deleted': False,
                'error': str(e)
            }
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def cancel_liquidation_slip(slip_id, staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Step 1: Verify the slip exists and is in PREPARING or PENDING status
            cursor.execute(
                "SELECT status FROM liquidation_slip WHERE id = %s AND staff_id = %s",
                (slip_id, staff_id)
            )
            slip = cursor.fetchone()
            if not slip or slip['status'] not in ('PREPARING', 'PENDING'):
                return {'success': False, 'error': 'Slip not found or not in PREPARING/PENDING status'}

            # Step 2: Update liquidation_slip status to CANCELED
            cursor.execute(
                "UPDATE liquidation_slip SET status = 'CANCELED' WHERE id = %s",
                (slip_id,)
            )
            if cursor.rowcount == 0:
                return {'success': False, 'error': 'Failed to update slip status'}

            # Step 3: Revert equipment statuses to AVAILABLE
            cursor.execute(
                """
                UPDATE equipment e
                JOIN detail_liquidation_slip dls ON e.id = dls.equipment_id
                SET e.status = 'AVAILABLE'
                WHERE dls.liquidation_slip_id = %s
                """,
                (slip_id,)
            )

            # Commit the transaction
            conn.commit()
            return {'success': True, 'error': None}

        except Exception as e:
            print(f"Error canceling liquidation slip: {e}")
            conn.rollback()
            return {'success': False, 'error': str(e)}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def accept_liquidation_slip(slip_id, staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Step 1: Verify the slip exists and is in PREPARING or PENDING status
            cursor.execute(
                "SELECT status FROM liquidation_slip WHERE id = %s AND staff_id = %s",
                (slip_id, staff_id)
            )
            slip = cursor.fetchone()
            if not slip or slip['status'] not in ('PREPARING', 'PENDING'):
                return {'success': False, 'error': 'Slip not found or not in PREPARING/PENDING status'}

            cursor.execute(
                "UPDATE liquidation_slip SET status = 'COMPLETED' WHERE id = %s",
                (slip_id,)
            )
            if cursor.rowcount == 0:
                return False

            # Step 3: Fetch all equipment associated with the slip
            cursor.execute(
                """
                SELECT dls.equipment_id, dls.quantity, e.management_type
                FROM detail_liquidation_slip dls
                JOIN equipment e ON dls.equipment_id = e.id
                WHERE dls.liquidation_slip_id = %s
                """,
                (slip_id,)
            )
            equipment_list = cursor.fetchall()

            # Step 4: Process each equipment based on management_type
            for item in equipment_list:
                equipment_id = item['equipment_id']
                quantity = item['quantity']
                management_type = item['management_type']

                if management_type == 'INDIVIDUAL':
                    # For INDIVIDUAL: Set status=LIQUIDATED, broken_quantity=0, under_repair_quantity=0
                    cursor.execute(
                        """
                        UPDATE equipment
                        SET status = 'LIQUIDATED', broken_quantity = 0, under_repair_quantity = 0
                        WHERE id = %s
                        """,
                        (equipment_id,)
                    )
                elif management_type == 'QUANTITY':
                    # For QUANTITY: Deduct quantity, set broken_quantity=0, under_repair_quantity=0
                    cursor.execute(
                        """
                        UPDATE equipment
                        SET quantity = quantity - %s, broken_quantity = 0, under_repair_quantity = 0
                        WHERE id = %s
                        """,
                        (quantity, equipment_id)
                    )

                if cursor.rowcount == 0:
                    raise Exception(f"Failed to update equipment ID {equipment_id}")

            # Commit the transaction
            conn.commit()
            return True

        except Exception as e:
            print(f"Error confirming liquidation slip: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def complete_liquidation_slip(slip_id, staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Step 1: Verify the slip exists and is in ACCEPTED status
            cursor.execute(
                "SELECT status FROM liquidation_slip WHERE id = %s AND staff_id = %s",
                (slip_id, staff_id)
            )
            slip = cursor.fetchone()
            if not slip or slip['status'] != 'ACCEPTED':
                return {'success': False, 'error': 'Slip not found or not in ACCEPTED status'}

            # Step 2: Update liquidation_slip status to COMPLETED and set liquidation_date
            cursor.execute(
                """
                UPDATE liquidation_slip
                SET status = 'COMPLETED', liquidation_date = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (slip_id,)
            )
            if cursor.rowcount == 0:
                return {'success': False, 'error': 'Failed to update slip status'}

            # Step 3: Fetch all equipment associated with the slip
            cursor.execute(
                """
                SELECT dls.equipment_id, dls.quantity, e.management_type
                FROM detail_liquidation_slip dls
                JOIN equipment e ON dls.equipment_id = e.id
                WHERE dls.liquidation_slip_id = %s
                """,
                (slip_id,)
            )
            equipment_list = cursor.fetchall()

            # Step 4: Process each equipment based on management_type
            for item in equipment_list:
                equipment_id = item['equipment_id']
                quantity = item['quantity']
                management_type = item['management_type']

                if management_type == 'INDIVIDUAL':
                    # For INDIVIDUAL: Ensure status=LIQUIDATED, broken_quantity=0, under_repair_quantity=0
                    cursor.execute(
                        """
                        UPDATE equipment
                        SET status = 'LIQUIDATED', broken_quantity = 0, under_repair_quantity = 0
                        WHERE id = %s
                        """,
                        (equipment_id,)
                    )
                elif management_type == 'QUANTITY':
                    # For QUANTITY: Ensure quantity is deducted, broken_quantity=0, under_repair_quantity=0
                    cursor.execute(
                        """
                        UPDATE equipment
                        SET quantity = quantity - %s, broken_quantity = 0, under_repair_quantity = 0
                        WHERE id = %s
                        """,
                        (quantity, equipment_id)
                    )

                if cursor.rowcount == 0:
                    raise Exception(f"Failed to update equipment ID {equipment_id}")

            # Commit the transaction
            conn.commit()
            return {'success': True, 'error': None}

        except Exception as e:
            print(f"Error completing liquidation slip: {e}")
            conn.rollback()
            return {'success': False, 'error': str(e)}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_existing_ticket(staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM liquidation_slip WHERE staff_id = %s AND status = 'PREPARING'", (staff_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def add_equipment_to_ticket(ticket_id, equipment_id, quantity=1, description=None, price=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                INSERT INTO detail_liquidation_slip (liquidation_slip_id, equipment_id, quantity, description, price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (ticket_id, equipment_id, quantity, description, price))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding equipment to ticket: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_my_liquidation_slip(staff_id=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM liquidation_slip WHERE staff_id = %s AND status = 'PENDING' OR status = 'PREPARING'", (staff_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def confirm_liquidation_slip(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("UPDATE liquidation_slip SET status = 'PENDING' WHERE id = %s", (request_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating repair ticket status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod 
    def get_all_processed_equipment():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT e_id FROM v_liquidation_full_details WHERE liquidation_status = 'PENDING' OR liquidation_status = 'PREPARING'")
            r = cursor.fetchall()
            return [x['e_id'] for x in r]
        finally:
            cursor.close()
            conn.close()