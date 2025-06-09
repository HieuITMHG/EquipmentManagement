from models.database import get_connection

class RoleService:
    @staticmethod
    def get_all_role():
        """Lấy danh sách tất cả thiết bị từ DB"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM vai_tro")
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()

