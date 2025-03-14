from models.database import get_connection

class UserService:
    @staticmethod
    def get_all_users():
        """Lấy danh sách tất cả users từ DB"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, name, email FROM users")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_user(name, email):
        """Tạo user mới"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Kiểm tra email đã tồn tại chưa
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return {"error": "Email already exists"}, 400

            # Chèn dữ liệu mới vào bảng users
            query = "INSERT INTO users (name, email) VALUES (%s, %s)"
            cursor.execute(query, (name, email))
            conn.commit()
            return {"message": "User created", "user_id": cursor.lastrowid}, 201
        finally:
            cursor.close()
            conn.close()
