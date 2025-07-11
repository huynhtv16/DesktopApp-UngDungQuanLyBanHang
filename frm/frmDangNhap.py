import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controllers.nguoidung_controller import NguoiDungController


class FrmDangNhap(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controller = NguoiDungController()
        self.title("Đăng nhập hệ thống")
        self.configure(bg="#ffffff")
        self.setup_ui()

    def setup_ui(self):
        # Đặt kích thước cố định và căn giữa cửa sổ
        width = 400
        height = 250
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.center_window(width, height)

        # Cấu hình style với ttk
        style = ttk.Style(self)
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12), padding=5)

        # Khung chính với padding
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True, fill="both")

        # Tiêu đề
        lbl_title = ttk.Label(main_frame, text="ĐĂNG NHẬP", font=("Helvetica", 16, "bold"), foreground="#333333")
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Nhãn và ô nhập tài khoản
        lbl_username = ttk.Label(main_frame, text="Tài khoản:")
        lbl_username.grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)
        self.entry_username = ttk.Entry(main_frame, width=30)
        self.entry_username.grid(row=1, column=1, pady=5, sticky="w")

        # Nhãn và ô nhập mật khẩu
        lbl_password = ttk.Label(main_frame, text="Mật khẩu:")
        lbl_password.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=5)
        self.entry_password = ttk.Entry(main_frame, width=30, show="*")
        self.entry_password.grid(row=2, column=1, pady=5, sticky="w")

        # Nút đăng nhập
        btn_login = ttk.Button(main_frame, text="Đăng nhập", command=self.dang_nhap)
        btn_login.grid(row=3, column=0, columnspan=2, pady=(20, 0))

    def center_window(self, width, height):
        # Tính vị trí để căn giữa cửa sổ trên màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def dang_nhap(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Kiểm tra thông tin đăng nhập thông qua controller
        user = self.controller.kiem_tra_dang_nhap(username, password)
        if user:
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            self.current_user = user
            self.mo_ung_dung()
        else:
            messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu không đúng!")

    def mo_ung_dung(self):
        from main import MainApplication  # Import sau để tránh circular import
        self.destroy()
        app = MainApplication(self.current_user)
        app.mainloop()


if __name__ == "__main__":
    login_window = FrmDangNhap()
    login_window.mainloop()
