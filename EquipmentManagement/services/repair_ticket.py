import mysql.connector
from models.database import get_connection  

class RepairTicketService:
    @staticmethod
    def get_repair_ticket(staff_id=None, status=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if staff_id != None:
                cursor.execute("SELECT * FROM repair_ticket WHERE staff_id = %s AND status = %s", (staff_id, status))
            else:
                cursor.execute("SELECT * FROM repair_ticket WHERE status = %s", (status,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_my_repair_ticket(staff_id=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM repair_ticket WHERE staff_id = %s AND (status = 'PENDING' OR status = 'PREPARING')", (staff_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_pending_repair_ticket():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM repair_ticket WHERE status = 'PENDING'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_history_repair_ticket(start_date=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT * FROM repair_ticket 
                WHERE status IN ('COMPLETED', 'REJECTED', 'ACCEPTED')
            """
            params = []

            if start_date:
                query += " AND DATE(start_date) = %s"
                params.append(start_date)

            query += " ORDER BY start_date DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_total_cost(repair_ticket_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT SUM(price) AS total_cost FROM detail_repair_ticket WHERE repair_ticket_id = %s", (repair_ticket_id,))
            result = cursor.fetchone()  # Lấy hàng đầu tiên (chỉ có một hàng vì SUM)
            
            # Kiểm tra và trả về tổng dưới dạng số nguyên
            if result and result['total_cost'] is not None:
                return int(result['total_cost'])
            return 0  # Trả về 0 nếu không có dữ liệu hoặc tổng là NULL
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_repair_ticket(repair_ticket_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM repair_ticket WHERE id = %s", (repair_ticket_id,))
            
            if cursor.rowcount > 0:
                conn.commit() 
                return True
            else:
                conn.rollback() 
                return False
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL: {err}")
            conn.rollback() 
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_equipment_in_repair_ticket(repair_ticket_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM v_repair_ticket_details WHERE repair_ticket_id = %s", (repair_ticket_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    @staticmethod 
    def get_all_processed_equipment():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT e_id FROM v_repair_ticket_details WHERE repair_ticket_status = 'PENDING' OR repair_ticket_status = 'PREPARING'")
            r = cursor.fetchall()
            return [x['e_id'] for x in r]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_existing_ticket(staff_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM repair_ticket WHERE staff_id = %s AND status = 'PREPARING'", (staff_id,))
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
                INSERT INTO detail_repair_ticket (repair_ticket_id, equipment_id, quantity, description, price)
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
    def create_repair_ticket_with_equipment(staff_id, equipment_id, quantity=1, description=None, price=None, status='PREPARING'):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Step 1: Create a new repair ticket
            query_ticket = """
                INSERT INTO repair_ticket (staff_id, status)
                VALUES (%s, %s)
            """
            cursor.execute(query_ticket, (staff_id, status))
            
            # Get the ID of the newly created ticket
            ticket_id = cursor.lastrowid
            
            # Step 2: Add the equipment to the ticket
            query = """
                INSERT INTO detail_repair_ticket (repair_ticket_id, equipment_id, quantity, description, price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (ticket_id, equipment_id, quantity, description, price))
            
            # Commit the transaction
            conn.commit()
            return True
        
        except Exception as e:
            print(f"Error creating repair ticket: {e}")
            conn.rollback()
            return False
        
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remove_equipment_from_ticket(repair_ticket_id, equipment_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Step 1: Delete the equipment from detail_repair_ticket
            query_delete = """
                DELETE FROM detail_repair_ticket
                WHERE repair_ticket_id = %s AND equipment_id = %s
            """
            cursor.execute(query_delete, (repair_ticket_id, equipment_id))
            equipment_deleted = cursor.rowcount  # Number of rows deleted (0 or 1)

            # Step 2: Check if any equipment items remain in the ticket
            query_count = """
                SELECT COUNT(*) AS item_count
                FROM detail_repair_ticket
                WHERE repair_ticket_id = %s
            """
            cursor.execute(query_count, (repair_ticket_id,))
            item_count = cursor.fetchone()['item_count']

            # Step 3: If no items remain, delete the repair ticket
            ticket_deleted = False
            if item_count == 0:
                query_delete_ticket = """
                    DELETE FROM repair_ticket
                    WHERE id = %s
                """
                cursor.execute(query_delete_ticket, (repair_ticket_id,))
                ticket_deleted = cursor.rowcount > 0  # True if ticket was deleted

            # Commit the transaction
            conn.commit()
            return {
                'success': True,
                'equipment_deleted': equipment_deleted,
                'ticket_deleted': ticket_deleted,
                'error': None
            }

        except Exception as e:
            print(f"Error removing equipment from ticket: {e}")
            conn.rollback()
            return {
                'success': False,
                'equipment_deleted': 0,
                'ticket_deleted': False,
                'error': str(e)
            }
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def complete_repair_ticket(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                UPDATE repair_ticket
                SET status = 'COMPLETED', end_date = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (request_id,)
            )
            if cursor.rowcount == 0:
                return False
            cursor.execute(
                """
                SELECT drt.equipment_id, e.management_type
                FROM detail_repair_ticket drt
                JOIN equipment e ON drt.equipment_id = e.id
                WHERE drt.repair_ticket_id = %s
                """,
                (request_id,)
            )
            equipment_list = cursor.fetchall()

            for item in equipment_list:
                equipment_id = item['equipment_id']
                management_type = item['management_type']

                if management_type == 'INDIVIDUAL':
                    cursor.execute(
                        """
                        UPDATE equipment
                        SET status = 'AVAILABLE', broken_quantity = 0, under_repair_quantity = 0
                        WHERE id = %s
                        """,
                        (equipment_id,)
                    )
                elif management_type == 'QUANTITY':
                    cursor.execute(
                        """
                        UPDATE equipment
                        SET broken_quantity = 0, under_repair_quantity = 0
                        WHERE id = %s
                        """,
                        (equipment_id,)
                    )

                if cursor.rowcount == 0:
                    raise Exception(f"Failed to update equipment ID {equipment_id}")

            # Commit the transaction
            conn.commit()
            return True

        except Exception as e:
            print(f"Error completing repair ticket: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def confirm_repair_ticket(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("UPDATE repair_ticket SET status = 'PENDING' WHERE id = %s", (request_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating repair ticket status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def accept_repair_ticket(request_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Step 2: Update repair_ticket status to ACCEPTED
            cursor.execute(
                "UPDATE repair_ticket SET status = 'ACCEPTED' WHERE id = %s",
                (request_id,)
            )
            if cursor.rowcount == 0:
                return False

            # Step 3: Fetch all equipment associated with the ticket
            cursor.execute(
                """
                SELECT drt.equipment_id, drt.quantity, e.management_type
                FROM detail_repair_ticket drt
                JOIN equipment e ON drt.equipment_id = e.id
                WHERE drt.repair_ticket_id = %s
                """,
                (request_id,)
            )
            equipment_list = cursor.fetchall()

            # Step 4: Process each equipment based on management_type
            for item in equipment_list:
                equipment_id = item['equipment_id']
                quantity = item['quantity']
                management_type = item['management_type']

                if management_type == 'INDIVIDUAL':
                    # For INDIVIDUAL: Set status=UNDERREPAIR, broken_quantity=0, under_repair_quantity=1
                    cursor.execute(
                        """
                        UPDATE equipment
                        SET status = 'UNDERREPAIR', broken_quantity = 0, under_repair_quantity = 1
                        WHERE id = %s
                        """,
                        (equipment_id,)
                    )
                elif management_type == 'QUANTITY':
                    # For QUANTITY: Set broken_quantity=0, under_repair_quantity=quantity
                    cursor.execute(
                        """
                        UPDATE equipment
                        SET broken_quantity = 0, under_repair_quantity = %s
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
            print(f"Error confirming repair ticket: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
            
    @staticmethod
    def reject_repair_ticket(ticket_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE repair_ticket SET status = 'REJECTED' WHERE id = %s", (ticket_id,))
            conn.commit()
            return cursor.rowcount > 0  
        finally:
            cursor.close()
            conn.close()




