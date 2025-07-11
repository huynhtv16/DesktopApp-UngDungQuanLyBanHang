import tkinter as tk
from utils import load_form

def create_menu(left_frame, right_frame, user_info, logout_callback):
    # Cấu hình giao diện cho các nút menu
    menu_style = {
        "bg": "#34495e",
        "fg": "white",
        "activebackground": "#2c3e50",
        "activeforeground": "white",
        "font": ("Arial", 12),
        "relief": "flat",
        "borderwidth": 0,
        "anchor": "w"
    }

    menu_items = [
        ("🏠 Trang Chủ", "TrangChu"),
        ("📦 Quản Lý Sản Phẩm", "QlySanPham"),
        ("📦 Quản Lý Đơn Hàng", "QlyDonHang"),
        ("👥 Quản Lý Khách Hàng", "QlyKhachHang"),
        ("👔 Quản Lý Người Dùng", "QlyNguoiDung"),
        ("🗂 Quản Lý Danh Mục", "QlyDanhMuc"),
        ("📊 Thống Kê", "QlyThongKe")
        #("Sao Lưu","QlySaoLuu")
    ]

    # Tạo các nút menu dựa theo danh sách menu_items
    for text, form_name in menu_items:
        # Nếu không phải admin (maChucVu != 1) thì bỏ qua nút "Quản Lý Người Dùng"
        if form_name == "QlyNguoiDung" and user_info['maChucVu'] != 1:
            continue

        btn = tk.Button(
            left_frame,
            text=text,
            width=20,
            command=lambda name=form_name: load_form(right_frame, name),
            **menu_style
        )
        btn.pack(pady=5, padx=10, ipady=8)

    # Thêm nút đăng xuất ở phía dưới cùng của menu
    logout_btn = tk.Button(
        left_frame,
        text="🚪 Đăng Xuất",
        width=20,
        command=logout_callback,
        **menu_style
    )
    logout_btn.pack(side="bottom", pady=10, padx=10, ipady=8)
