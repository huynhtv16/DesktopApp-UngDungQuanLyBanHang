from models.database import Database
from datetime import datetime, timedelta


class ThongKeModel:
    def __init__(self):
        self.db = Database()
        self.connection = self.db.get_connection()

    def thongke_theo_thoigian(self, start_date, end_date):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT DATE(dh.ngayDatHang) as ngay, 
                       SUM(ctdh.soLuong * ctdh.gia) as doanhthu
                FROM donhang dh
                JOIN chitietdonhang ctdh ON dh.maDonHang = ctdh.maDonHang
                WHERE dh.ngayDatHang BETWEEN %s AND %s
                GROUP BY DATE(dh.ngayDatHang)
            """
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi thống kê theo thời gian: {e}")
            return []

    def thongke_sanpham_banchay(self, limit=5):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT sp.tenSanPham, SUM(ctdh.soLuong) as tongsl
                FROM chitietdonhang ctdh
                JOIN sanpham sp ON ctdh.maSanPham = sp.maSanPham
                GROUP BY sp.maSanPham
                ORDER BY tongsl DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi thống kê sản phẩm bán chạy: {e}")
            return []

    def thongke_theo_thang(self, year):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT MONTH(dh.ngayDatHang) as thang, 
                       SUM(ctdh.soLuong * ctdh.gia) as doanhthu
                FROM donhang dh
                JOIN chitietdonhang ctdh ON dh.maDonHang = ctdh.maDonHang
                WHERE YEAR(dh.ngayDatHang) = %s
                GROUP BY MONTH(dh.ngayDatHang)
            """
            cursor.execute(query, (year,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi thống kê theo tháng: {e}")
            return []

    def get_thongke_ngay(self):
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        try:
            cursor = self.connection.cursor()

            # Số đơn trong ngày
            cursor.execute("SELECT COUNT(*) FROM donhang WHERE ngayDatHang >= %s AND ngayDatHang < %s",
                           (today, tomorrow))
            so_don = cursor.fetchone()[0]

            # Doanh thu ngày
            cursor.execute("""
                SELECT SUM(tongTien) 
                FROM donhang 
                WHERE ngayDatHang >= %s AND ngayDatHang < %s
            """, (today, tomorrow))
            doanh_thu = cursor.fetchone()[0] or 0

            # Số sản phẩm bán
            cursor.execute("""
                SELECT SUM(ctdh.soLuong)
                FROM chitietdonhang ctdh
                JOIN donhang dh ON ctdh.maDonHang = dh.maDonHang
                WHERE dh.ngayDatHang >= %s AND dh.ngayDatHang < %s
            """, (today, tomorrow))
            so_sanpham = cursor.fetchone()[0] or 0

            return {
                'so_don': so_don,
                'doanh_thu': doanh_thu,
                'so_sanpham': so_sanpham
            }

        except Exception as e:
            print(f"Lỗi thống kê ngày: {e}")
            return None

    def get_sanpham_ban_trong_ngay(self):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT sp.tenSanPham, SUM(ctdh.soLuong) as tong_ban
                FROM chitietdonhang ctdh
                JOIN donhang dh ON ctdh.maDonHang = dh.maDonHang
                JOIN sanpham sp ON ctdh.maSanPham = sp.maSanPham
                WHERE DATE(dh.ngayDatHang) = CURDATE()
                GROUP BY sp.maSanPham
                ORDER BY tong_ban DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy dữ liệu sản phẩm bán trong ngày: {e}")
            return []