from models.khachhang_model import KhachHangModel

class KhachHangController:
    def __init__(self):
        self.model = KhachHangModel()

    def get_all_khachhang(self):
        return self.model.get_all_khachhang()

    def add_khachhang(self, ten, sdt, diachi):
        return self.model.add_khachhang(ten, sdt, diachi)

    def update_khachhang(self, ma_kh,ten,sdt,diachi):
        return self.model.update_khachhang(ma_kh,ten,sdt,diachi)


    def delete_khachhang(self, ma_kh):
        return self.model.delete_khachhang(ma_kh)

    def search_khachhang(self, keyword):
        return self.model.search_khachhang(keyword)