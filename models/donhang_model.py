
from models.database import Database

class DonHangModel:
    def __init__(self):
        self.db = Database()
        self.connection = self.db.get_connection()

    def create_donhang(self, ma_khachhang, ngay_dat_hang, tong_tien):
        try:
            cursor = self.connection.cursor()
            # Câu truy vấn phải có đủ 3 placeholder tương ứng với 3 tham số truyền vào.
            query = "INSERT INTO donhang (maKhachHang, ngayDatHang, tongTien) VALUES (%s, %s, %s)"
            cursor.execute(query, (ma_khachhang, ngay_dat_hang, tong_tien))
            self.connection.commit()
            return cursor.lastrowid  # Trả về mã đơn hàng vừa tạo
        except Exception as e:
            print(f"Lỗi khi tạo đơn hàng: {e}")
            return None

    def create_chitiet_donhang(self, ma_donhang, ma_sanpham, so_luong, gia):
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO chitietdonhang 
                     (maDonHang, maSanPham, soLuong, gia)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (ma_donhang, ma_sanpham, so_luong, gia))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi thêm chi tiết đơn hàng: {e}")
            return False

    def get_all_donhang(self):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT d.maDonHang, d.maKhachHang, k.tenKhachHang, d.ngayDatHang, d.tongTien
                FROM donhang d
                JOIN khachhang k ON d.maKhachHang = k.maKhachHang
                ORDER BY d.ngayDatHang DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Lỗi khi lấy danh sách đơn hàng: {e}")
            return []

    def search_donhang(self, search_term):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT d.maDonHang, d.maKhachHang, k.tenKhachHang, d.ngayDatHang, d.tongTien
                FROM donhang d
                JOIN khachhang k ON d.maKhachHang = k.maKhachHang
                WHERE d.maDonHang LIKE %s
                   OR d.maKhachHang LIKE %s
                   OR k.tenKhachHang LIKE %s
                   OR DATE_FORMAT(d.ngayDatHang, '%d/%m/%Y') LIKE %s
                   OR d.tongTien LIKE %s
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi tìm kiếm đơn hàng:", e)
            return []

    def get_chitiet_donhang(self, ma_donhang):
        try:
            cursor = self.connection.cursor()
            query = """SELECT sp.maSanPham, sp.tenSanPham, ctdh.soLuong, ctdh.gia 
                     FROM chitietdonhang ctdh
                     JOIN sanpham sp ON ctdh.maSanPham = sp.maSanPham
                     WHERE ctdh.maDonHang = %s"""
            cursor.execute(query, (ma_donhang,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy chi tiết đơn hàng: {e}")
            return []

    def get_donhang_by_id(self, maDonHang):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT d.maDonHang, d.maKhachHang, k.tenKhachHang, d.ngayDatHang, d.tongTien
                FROM donhang d
                JOIN khachhang k ON d.maKhachHang = k.maKhachHang
                WHERE d.maDonHang = %s
            """
            cursor.execute(query, (maDonHang,))
            return cursor.fetchone()  # Lấy một đơn hàng duy nhất
        except Exception as e:
            print("Lỗi khi truy vấn đơn hàng:", e)
            return None

    def xoa_donhang(self, maDonHang):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM donhang WHERE maDonHang = %s"
            cursor.execute(query, (maDonHang,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Lỗi khi xóa đơn hàng:", e)
            return False


