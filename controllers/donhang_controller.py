from models.donhang_model import DonHangModel
from models.product_model import ProductModel
from datetime import datetime
from models.khachhang_model import KhachHangModel



class DonHangController:
    def __init__(self):
        self.donhang_model = DonHangModel()
        self.product_model = ProductModel()
        self.khachhang_model = KhachHangModel()

    def tao_donhang(self,maKhachHang, danh_sach_sanpham):
        # Tính tổng tiền
        tong_tien = sum(item['gia'] * item['so_luong'] for item in danh_sach_sanpham)

        # Tạo đơn hàng
        ma_donhang = self.donhang_model.create_donhang(maKhachHang,datetime.now(), tong_tien)

        if ma_donhang:
            # Thêm chi tiết đơn hàng
            for item in danh_sach_sanpham:
                success = self.donhang_model.create_chitiet_donhang(
                    ma_donhang,
                    item['ma_sanpham'],
                    item['so_luong'],
                    item['gia']
                )
                if not success:
                    return False
            return True
        return False
    def get_all_donhang(self):
        return self.donhang_model.get_all_donhang()

    def search_donhang(self, keyword):
        return self.donhang_model.search_donhang(keyword)

    def get_chitiet_donhang(self, ma_donhang):
        return self.donhang_model.get_chitiet_donhang(ma_donhang)

    def get_donhang_by_id(self, ma_donhang):
        return self.donhang_model.get_donhang_by_id(ma_donhang)

    def get_khachhang_list(self):
        return self.khachhang_model.get_all_khachhang()

    def xoa_donhang(self, ma_donhang):
        return self.donhang_model.xoa_donhang(ma_donhang)