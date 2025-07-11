from models.database import Database

class NguoiDungModel:
    def __init__(self):
        self.db = Database()
        self.connection = self.db.get_connection()

    def get_all_users(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT n.maNguoiDung, n.taiKhoan,n.matKhau, n.hoTen, c.tenChucVu
                FROM nguoidung n
                JOIN chucvu c ON n.maChucVu = c.maChucVu
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách người dùng: {e}")
            return []

    def add_user(self, taikhoan, matkhau, hofen, maChucVu):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO nguoidung (taiKhoan, matKhau, hoTen, maChucVu)
                VALUES (%s, %s, %s, %s)
            """, (taikhoan, matkhau, hofen, maChucVu))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi thêm người dùng: {e}")
            return False

    def update_user(self, maNguoiDung, taikhoan, hofen, maChucVu):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE nguoidung 
                SET taiKhoan = %s, hoTen = %s, maChucVu = %s 
                WHERE maNguoiDung = %s
            """, (taikhoan, hofen, maChucVu, maNguoiDung))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật người dùng: {e}")
            return False

    def delete_user(self, maNguoiDung):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM nguoidung WHERE maNguoiDung = %s", (maNguoiDung,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa người dùng: {e}")
            return False

    def search_users(self, keyword):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT n.maNguoiDung, n.taiKhoan,n.matKhau, n.hoTen, c.tenChucVu 
                FROM nguoidung n
                JOIN chucvu c ON n.maChucVu = c.maChucVu
                WHERE n.taiKhoan LIKE %s OR n.hoTen LIKE %s
            """
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi tìm kiếm người dùng: {e}")
            return []
    def kiem_tra_dang_nhap(self, username, password):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT n.maNguoiDung, n.taikhoan, c.maChucVu 
                FROM nguoidung n
                JOIN chucvu c ON n.maChucVu = c.maChucVu
                WHERE n.taikhoan = %s AND n.matkhau = %s
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            self.connection.commit()
            if result:
                return {
                    'maNguoiDung': result[0],
                    'taikhoan': result[1],
                    'maChucVu': result[2]
                }
            return None
        except Exception as e:
            print(f"Lỗi kiểm tra đăng nhập: {e}")
            return None