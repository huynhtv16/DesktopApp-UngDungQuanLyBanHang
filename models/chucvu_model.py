from models.database import Database

class ChucVuModel:
    def __init__(self):
        self.db = Database()
        self.connection = self.db.get_connection()

    def get_all_chucvu(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM chucvu"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy các chức vụ: {e}")
            return []