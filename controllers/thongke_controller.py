from models.thongke_model import ThongKeModel
import pandas as pd

class ThongKeController:
    def __init__(self):
        self.model = ThongKeModel()

    def get_data_thongke(self, start_date, end_date):
        return self.model.thongke_theo_thoigian(start_date, end_date)

    def get_top_sanpham(self):
        return self.model.thongke_sanpham_banchay()

    def get_data_theo_thang(self, year):
        return self.model.thongke_theo_thang(year)

    def xuat_excel(self, data, filename):
        try:
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)
            return True
        except Exception as e:
            print(f"Lỗi xuất Excel: {e}")
            return False

    def get_data_trangchu(self):
        return self.model.get_thongke_ngay()

    def get_sanpham_ban_ngay(self):
        return self.model.get_sanpham_ban_trong_ngay()