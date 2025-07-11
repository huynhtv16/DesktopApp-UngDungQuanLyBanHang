from models.danhmuc_model import DanhMucModel

class DanhMucController:
    def __init__(self):
        self.model = DanhMucModel()

    def get_all_danhmuc(self):
        return self.model.get_all_danhmuc()

    def add_danhmuc(self, ten_danhmuc):
        return self.model.add_danhmuc(ten_danhmuc)

    def update_danhmuc(self, ma_danhmuc, ten_danhmuc):
        return self.model.update_danhmuc(ma_danhmuc, ten_danhmuc)

    def delete_danhmuc(self, ma_danhmuc):
        return self.model.delete_danhmuc(ma_danhmuc)

    def search_danhmuc(self, keyword):
        return self.model.search_danhmuc(keyword)