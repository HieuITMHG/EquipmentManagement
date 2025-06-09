from models.database import get_connection

class AccountService:
    @staticmethod
    def get_all_account():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM AccountInfo")
            return cursor.fetchall()  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_account_by_person_id(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM AccountInfo WHERE tai_khoan_id = %s", (user_id,))
            account = cursor.fetchone()
            return account if account else None  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_user_info(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM tai_khoan WHERE id = %s", (user_id,))
            account = cursor.fetchone()

            if account['vai_tro_id'] == 3:
                cursor.execute("SELECT * FROM tai_khoan JOIN sinh_vien ON sinh_vien.id = tai_khoan.id WHERE tai_khoan.id = %s", (user_id,))
            else:
                cursor.execute("SELECT * FROM tai_khoan JOIN nhan_vien ON nhan_vien.id = tai_khoan.id WHERE tai_khoan.id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_account_by_email(email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM AccountInfo WHERE email = %s", (email,))
            account = cursor.fetchone()
            return account if account else None  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_account_by_cccd(cccd):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM AccountInfo WHERE cccd = %s", (cccd,))
            account = cursor.fetchone()
            return account if account else None  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_account_by_phone(phone):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM AccountInfo WHERE sdt = %s", (phone,))
            account = cursor.fetchone()
            return account if account else None  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_account_personal_id_by_person_id(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT person_id FROM AccountInfo WHERE tai_khoan_id = %s", (user_id,))
            account = cursor.fetchone()
            return account if account else None  
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_account_info_by_page(page_num=1):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            offset = (page_num - 1) * 10  
            cursor.execute("SELECT * FROM AccountInfo LIMIT 10 OFFSET %s", (offset,))
            accounts = cursor.fetchall()
            return accounts if accounts else []
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def delete_account(person_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM tai_khoan WHERE id = %s', (person_id,))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search_account_info(role_id=None, first_name=None, page_num=1):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM AccountInfo WHERE 1 = 1"

            # Base query for counting total records
            count_query = "SELECT COUNT(*) AS total FROM AccountInfo WHERE 1=1"
            params = []
            count_params = []

            # Apply filters for both queries
            if role_id:
                count_query += " AND vai_tro_id = %s"
                query += " AND vai_tro_id = %s"
                count_params.append(role_id)
                params.append(role_id)

            if first_name:
                count_query += " AND ten LIKE %s"
                query += " AND ten LIKE %s"
                count_params.append(f"%{first_name}%")
                params.append(f"%{first_name}%")

            # Execute count query
            cursor.execute(count_query, count_params)
            total_records = cursor.fetchone()['total']
            total_pages = (total_records + 10) // 10  

            # Add pagination to main query
            offset = (page_num - 1) * 10
            query += " LIMIT 10 OFFSET %s"
            params.append(offset)

            # Execute main query
            cursor.execute(query, params)
            accounts = cursor.fetchall()

            return accounts if accounts else [], total_pages
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_new_account(account_id, password, role_id, cccd, first_name, last_name, gender, email, phone, address, class_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Mã hóa password nếu cần, ở đây để nguyên
            hashed_password = password
            print(role_id)

            cursor.callproc('tao_tai_khoan_moi', (
                account_id,           # p_id
                hashed_password,      # p_mat_khau
                int(role_id),            # p_ten_vai_tro
                cccd,                 # p_cccd
                first_name,           # p_ho
                last_name,            # p_ten
                gender,               # p_gioi_tinh
                email,                # p_email
                phone,                # p_sdt
                address,              # p_dia_chi
                class_id              # p_lop_id
            ))

            # Đọc kết quả trả về (SELECT 1 AS success, ...)
            for result in cursor.stored_results():
                row = result.fetchone()
                print(row)
                return row[0] == 1  # success = 1 -> True
        except Exception as e:
            print("Error: " + str(e))
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_account(account_id, is_active, cccd, first_name, last_name, gender, email, phone, address, class_id, role_id):
        conn = get_connection()
        cursor = conn.cursor()
        print("Values sent to procedure:")
        print("account_id:", account_id)
        print("is_active:", int(is_active))
        print("role_id:", int(role_id))
        print("class_id:", class_id)

        try:
            cursor.callproc('cap_nhat_tai_khoan', (
                account_id,           # p_id
                is_active,            # p_dang_hoat_dong
                cccd,                 # p_cccd
                first_name,           # p_ho
                last_name,            # p_ten
                gender,               # p_gioi_tinh
                email,                # p_email
                phone,                # p_sdt
                address,              # p_dia_chi
                class_id,             # p_lop_id
                int(role_id)               # p_vai_tro_id
            ))

            for result in cursor.stored_results():
                row = result.fetchone()
                print(row)
                return row[0] == 1  # success = 1 -> True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

