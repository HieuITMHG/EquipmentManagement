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
            cursor.execute("SELECT * FROM AccountInfo WHERE person_id = %s", (user_id,))
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
            cursor.execute("SELECT person_id FROM AccountInfo WHERE person_id = %s", (user_id,))
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
    def create_new_account(cccd, first_name, last_name, gender, email, phone, address, role_id, class_id, account_code, password):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Mã hóa password
            hashed_password = password
            # Gọi stored procedure
            cursor.callproc('CreateNewAccount', (
                cccd,
                first_name,
                last_name,
                gender,
                email,
                phone,
                address,
                role_id,
                class_id,
                account_code,
                hashed_password
            ))
            # Commit giao dịch
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_account(person_id, cccd, first_name, last_name, gender, email, phone, address, role_id, class_id, is_studing, is_working):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('UpdateAccount', (
                person_id, cccd, first_name, last_name, gender, email, phone, address, role_id, class_id,
                is_studing if is_studing is not None else False,
                is_working if is_working is not None else False
            ))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_account(person_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('DeleteAccount', (person_id,))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()
    
