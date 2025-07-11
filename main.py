import tkinter as tk
from utils import load_form
from frm.frmDangNhap import FrmDangNhap
from menu import create_menu

class MainApplication(tk.Tk):
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.title("Hệ Thống Quản Lý Đồ Ăn Nhanh")
        self.geometry("1280x620")
        self.configure(bg="#2c2f3f")
        self.create_layout()
        self.create_menu()
        self.show_default_form()



    def create_layout(self):
        # Tạo khung menu bên trái
        self.left_frame = tk.Frame(self, width=250, bg="#34495e")
        self.left_frame.pack(side="left", fill="y")
        # Tạo khung nội dung bên phải
        self.right_frame = tk.Frame(self, bg="#2c2f3f")
        self.right_frame.pack(side="right", fill="both", expand=True)

    def create_menu(self):
        # Gọi hàm tạo menu từ file menu.py, truyền thêm thông tin người dùng và callback đăng xuất
        create_menu(self.left_frame, self.right_frame, self.user_info, self.dang_xuat)

    def show_default_form(self):
        # Hiển thị form mặc định (ví dụ: Trang Chủ)
        load_form(self.right_frame, "TrangChu")

    def dang_xuat(self):
        self.destroy()
        FrmDangNhap().mainloop()


