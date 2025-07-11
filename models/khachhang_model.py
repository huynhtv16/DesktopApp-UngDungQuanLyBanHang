from models.database import Database

class KhachHangModel:
    def __init__(self):
        self.db = Database()
        self.connection = self.db.get_connection()

    def get_all_khachhang(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM khachhang")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách khách hàng: {e}")
            return []

    def add_khachhang(self, ten, sdt, diachi):
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO khachhang (tenKhachHang, sdt, diaChi) 
                     VALUES (%s, %s, %s)"""
            cursor.execute(query, (ten, sdt, diachi))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi thêm khách hàng: {e}")
            return False

    def update_khachhang(self, ma_kh, ten, sdt, diachi):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE khachhang SET 
                     tenKhachHang = %s,
                     sdt = %s,
                     diaChi = %s
                     WHERE maKhachHang = %s"""
            cursor.execute(query, (ten, sdt, diachi, ma_kh))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật khách hàng: {e}")
            return False

    def delete_khachhang(self, ma_kh):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM khachhang WHERE maKhachHang = %s", (ma_kh,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa khách hàng: {e}")
            return False

    def search_khachhang(self, keyword):
        try:
            cursor = self.connection.cursor()
            query = """SELECT * FROM khachhang 
                     WHERE tenKhachHang LIKE %s 
                     OR sdt LIKE %s"""
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi tìm kiếm khách hàng: {e}")
            return []