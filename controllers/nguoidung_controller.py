from models.nguoidung_model import NguoiDungModel
from models.chucvu_model import ChucVuModel

class NguoiDungController:
    def __init__(self):
        self.model = NguoiDungModel()
        self.chucvu_model = ChucVuModel()

    def get_all_users(self):
        return self.model.get_all_users()

    def get_chucvu_list(self):
        return self.chucvu_model.get_all_chucvu()

    def add_user(self, data):
        return self.model.add_user(data['taikhoan'], data['matkhau'], data['hofen'], data['maChucVu'])

    def update_user(self, maNguoiDung, data):
        return self.model.update_user(maNguoiDung, data['taikhoan'], data['hofen'], data['maChucVu'])

    def delete_user(self, maNguoiDung):
        return self.model.delete_user(maNguoiDung)

    def search_users(self, keyword):
        return self.model.search_users(keyword)

    def kiem_tra_dang_nhap(self, username, password):
        return  self.model.kiem_tra_dang_nhap(username,password)