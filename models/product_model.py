
from models.database import Database

class ProductModel:
    def __init__(self):
        self.db = Database()
        self.connection = self.db.get_connection()

    def get_all_products(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM sanpham")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu: {e}")
            return []

    def add_product(self, ten, gia, soluong, mota, madanhmuc):
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO sanpham 
                     (tenSanPham, gia, soLuong, moTa, maDanhMuc)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (ten, gia, soluong, mota, madanhmuc))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi thêm sản phẩm: {e}")
            return False

    def update_product(self, ma, ten, gia, soluong, mota, madanhmuc):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE sanpham SET 
                     tenSanPham = %s,
                     gia = %s,
                     soLuong = %s,
                     moTa = %s,
                     maDanhMuc = %s
                     WHERE maSanPham = %s"""
            cursor.execute(query, (ten, gia, soluong, mota, madanhmuc, ma))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật sản phẩm: {e}")
            return False

    def delete_product(self, ma):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM sanpham WHERE maSanPham = %s", (ma,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa sản phẩm: {e}")
            return False

    #phuong thuc tim kiem
    def search_products(self, keyword):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM sanpham WHERE tenSanPham LIKE %s"
            cursor.execute(query, (f"%{keyword}%",))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi tìm kiếm: {e}")
            return []

