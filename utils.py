def load_form(right_frame, form_name):
    # Clear previous content
    for widget in right_frame.winfo_children():
        widget.destroy()

    try:
        if form_name == "TrangChu":
            from frm.frmTrangChu import TrangChuForm
            form = TrangChuForm(right_frame)
            form.pack(expand=True, fill="both", padx=10, pady=10)
        elif form_name == "QlySanPham":
            from frm.frmQlySanPham import FrmQlySanPham
            form = FrmQlySanPham(right_frame)
            form.pack(expand=True, fill="both", padx=10, pady=10)
        elif form_name == "QlyDonHang":
            from frm.frmQlyDonHang import FrmQlyDonHang
            form = FrmQlyDonHang(right_frame)
            form.pack(expand=True, fill="both", padx=10, pady=10)
        elif form_name == "QlyNguoiDung":
            from frm.frmQlyNguoiDung import FrmQlyNguoiDung
            form = FrmQlyNguoiDung(right_frame)
            form.pack(expand=True,fill="both", padx = 10,pady = 10)
        elif form_name == "QlyThongKe":
            from frm.frmQlyThongKe import FrmQlyThongKe
            form = FrmQlyThongKe(right_frame)
            form.pack(expand=True,fill="both",padx=10,pady=10)
        elif form_name == "QlyDanhMuc":
            from frm.frmQlyDanhMuc import FrmQlyDanhMuc
            form = FrmQlyDanhMuc(right_frame)
            form.pack(expand=True,fill="both",padx=10,pady=10)
        elif form_name == "QlyKhachHang":
            from frm.frmQlyKhachHang import FrmQlyKhachHang
            form = FrmQlyKhachHang(right_frame)
            form.pack(expand=True,fill="both",padx= 10,pady=10)
        # elif form_name == "QlySaoLuu":
        #     from frm.frmSaoLuu import FrmMainMenu
        #     form = FrmMainMenu(right_frame)
        #     form.pack(expand=True, fill="both", padx=10, pady=10)
        # Add other forms here
        # elif form_name == "QlySanPham":
        #     ...

    except Exception as e:
        print(f"Error loading form: {e}")