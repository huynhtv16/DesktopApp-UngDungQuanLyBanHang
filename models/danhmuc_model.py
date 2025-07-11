from models.database import Database

class DanhMucModel:
    def __init__(self):
        self.db = Database()
        self.connection = self.db.get_connection()

    def get_all_danhmuc(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM danhmuc")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách danh mục: {e}")
            return []

    def add_danhmuc(self, ten_danhmuc):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO danhmuc (tenDanhMuc) VALUES (%s)", (ten_danhmuc,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi thêm danh mục: {e}")
            return False

    def update_danhmuc(self, ma_danhmuc, ten_danhmuc):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE danhmuc SET tenDanhMuc = %s WHERE maDanhMuc = %s",
                         (ten_danhmuc, ma_danhmuc))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật danh mục: {e}")
            return False

    def delete_danhmuc(self, ma_danhmuc):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM danhmuc WHERE maDanhMuc = %s", (ma_danhmuc,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa danh mục: {e}")
            return False

    def search_danhmuc(self, keyword):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM danhmuc WHERE tenDanhMuc LIKE %s", (f"%{keyword}%",))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi tìm kiếm danh mục: {e}")
            return []