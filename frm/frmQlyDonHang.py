import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from fpdf import FPDF

from controllers.donhang_controller import DonHangController
from controllers.product_controller import ProductController
from controllers.khachhang_controller import KhachHangController

class FrmQlyDonHang(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50")
        self.donhang_controller = DonHangController()
        self.product_controller = ProductController()
        self.khachhang_controller = KhachHangController()
        self.danh_sach_sanpham = []  # Lưu tạm sản phẩm được chọn
        self.configure_style()
        self.create_widgets()
        self.load_data()
        # Gắn sự kiện click vào Treeview
        self.tree.bind("<Double-1>", self.show_detail_donhang)

    def show_detail_donhang(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Lấy mã đơn hàng từ hàng được chọn
        ma_donhang = self.tree.item(selected_item)['values'][0]

        # Lấy thông tin chi tiết đơn hàng
        donhang_info = self.donhang_controller.get_donhang_by_id(ma_donhang)
        chitiet_donhang = self.donhang_controller.get_chitiet_donhang(ma_donhang)

        # Tạo pop-up hiển thị thông tin
        self.create_detail_popup(donhang_info, chitiet_donhang)

    def create_detail_popup(self, donhang_info, chitiet_donhang):
        # Giả sử donhang_info = (ma_dh, ma_kh, ten_kh, ngay_dat, tong_tien)
        popup = tk.Toplevel()
        popup.title(f"Chi tiết đơn hàng #{donhang_info[0]}")
        popup.geometry("800x500")

        # Chuyển đổi ngày đặt nếu cần (giả sử donhang_info[3] là timestamp Unix)
        ngay_dat = donhang_info[3]
        if isinstance(ngay_dat, int):
            ngay_dat = datetime.fromtimestamp(ngay_dat)

        # Thông tin cơ bản
        info_frame = tk.Frame(popup)
        info_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(info_frame, text=f"Mã đơn hàng: {donhang_info[0]}", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        tk.Label(info_frame, text=f"Mã khách hàng: {donhang_info[1]}", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        tk.Label(info_frame, text=f"Tên khách hàng: {donhang_info[2]}", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        tk.Label(info_frame, text=f"Ngày đặt: {ngay_dat.strftime('%d/%m/%Y')}", font=("Arial", 12)).grid(row=3, column=0, sticky="w")
        tk.Label(info_frame, text=f"Tổng tiền: {donhang_info[4]:,.0f} VNĐ", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w")

        # Bảng chi tiết sản phẩm
        tree_frame = tk.Frame(popup)
        tree_frame.pack(fill="both", expand=True, padx=10)

        columns = ("Mã SP", "Tên SP", "Số lượng", "Đơn giá", "Thành tiền")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100 if col == "Mã SP" else 150)
        for item in chitiet_donhang:
            # Giả sử mỗi chi tiết đơn hàng là tuple: (ma_sp, ten_sp, so_luong, gia)
            ma_sp, ten_sp, so_luong, gia = item
            thanh_tien = so_luong * gia
            tree.insert("", "end", values=(ma_sp, ten_sp, so_luong, f"{gia:,.0f}", f"{thanh_tien:,.0f}"))
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Nút xuất PDF
        btn_export = ttk.Button(popup, text="📄 Xuất PDF", command=lambda: self.export_to_pdf(donhang_info, chitiet_donhang))
        btn_export.pack(pady=10)

    def export_to_pdf(self, donhang_info, chitiet_donhang):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', r'D:\DH\K2_N3\LTUDPY\File project\BTL\frm\dejavu-fonts-ttf-2.37\dejavu-fonts-ttf-2.37\ttf\DejaVuSans.ttf', uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, txt=f"HÓA ĐƠN #{donhang_info[0]}", ln=1, align="C")
        pdf.cell(200, 10, txt=f"Ngày đặt: {donhang_info[3].strftime('%d/%m/%Y')}", ln=1)
        pdf.cell(200, 10, txt=f"Tổng tiền: {donhang_info[4]:,.0f} VNĐ", ln=1)
        pdf.cell(40, 10, "Mã SP", border=1)
        pdf.cell(60, 10, "Tên SP", border=1)
        pdf.cell(30, 10, "Số lượng", border=1)
        pdf.cell(40, 10, "Đơn giá", border=1)
        pdf.cell(40, 10, "Thành tiền", border=1)
        pdf.ln()
        for item in chitiet_donhang:
            ma_sp, ten_sp, so_luong, gia = item
            thanh_tien = so_luong * gia
            pdf.cell(40, 10, str(ma_sp), border=1)
            pdf.cell(60, 10, ten_sp.encode('utf-8').decode('utf-8'), border=1)
            pdf.cell(30, 10, str(so_luong), border=1)
            pdf.cell(40, 10, f"{gia:,.0f}", border=1)
            pdf.cell(40, 10, f"{thanh_tien:,.0f}", border=1)
            pdf.ln()
        file_path = asksaveasfilename(
            title="Chọn nơi lưu file PDF",
            initialfile=f"donhang_{donhang_info[0]}.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            pdf.output(file_path, "F")
            messagebox.showinfo("Thành công", f"Đã xuất PDF thành công: {file_path}")

    def configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#34495e", foreground="white",
                             fieldbackground="#34495e", rowheight=25, bordercolor="#16a085")
        self.style.configure("Treeview.Heading", background="#16a085", foreground="white",
                             font=("Arial", 12, "bold"))
        self.style.map("TButton", background=[("active", "#3498db"), ("!disabled", "#2980b9")],
                       foreground=[("!disabled", "white")])

    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # === Thanh tìm kiếm ===
        search_frame = tk.Frame(main_frame, bg="#2c3e50")
        search_frame.pack(fill="x", pady=5)
        self.search_var = tk.StringVar()
        self.entry_search = ttk.Entry(search_frame, textvariable=self.search_var, width=40, style="Search.TEntry")
        self.entry_search.pack(side="left", padx=5)
        self.entry_search.insert(0, "Nhập mã đơn, mã KH, tên KH, ngày đặt hoặc tổng tiền...")
        self.entry_search.bind("<FocusIn>", lambda e: self.entry_search.delete(0, "end"))
        btn_search = ttk.Button(search_frame, text="🔍 Tìm kiếm", command=self.search_donhang)
        btn_search.pack(side="left", padx=5)
        btn_clear = ttk.Button(search_frame, text="❌ Xóa tìm", command=self.clear_search)
        btn_clear.pack(side="left", padx=5)

        # === Bảng đơn hàng với cột: Mã ĐH, Mã KH, Tên KH, Ngày đặt, Tổng tiền ===
        self.tree = ttk.Treeview(main_frame,
                                 columns=("Mã ĐH", "Mã KH", "Tên KH", "Ngày đặt", "Tổng tiền"),
                                 show="headings",
                                 style="Custom.Treeview")
        self.tree.heading("Mã ĐH", text="Mã ĐH", anchor="center")
        self.tree.heading("Mã KH", text="Mã KH", anchor="center")
        self.tree.heading("Tên KH", text="Tên KH", anchor="center")
        self.tree.heading("Ngày đặt", text="Ngày đặt")
        self.tree.heading("Tổng tiền", text="Tổng tiền (VNĐ)", anchor="e")
        self.tree.column("Mã ĐH", width=100)
        self.tree.column("Mã KH", width=100)
        self.tree.column("Tên KH", width=150)
        self.tree.column("Ngày đặt", width=150)
        self.tree.column("Tổng tiền", width=150)
        self.tree.pack(fill="both", expand=True, pady=10)

        # Nút chức năng
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=10)

        buttons = [
            ("➕ Tạo đơn hàng", self.show_taodon_dialog),
            ("🗑️ Xóa", self.xoa_donhang),
            ("🔄 Làm mới", self.load_data)
        ]

        for text, cmd in buttons:
            ttk.Button(btn_frame,
                       text=text,
                       command=cmd,
                       style="TButton").pack(side="left", padx=5)

    def show_taodon_dialog(self):
        dialog = tk.Toplevel()
        dialog.title("Tạo đơn hàng mới")
        dialog.geometry("800x500")

        # Frame chọn khách hàng
        frame_kh = tk.Frame(dialog)
        frame_kh.pack(fill="x", padx=10, pady=10)
        tk.Label(frame_kh, text="Chọn khách hàng:", font=("Arial", 12)).pack(side="left", padx=5)
        self.combo_kh = ttk.Combobox(frame_kh, state="readonly", font=("Arial", 12), width=30)
        self.combo_kh.pack(side="left", padx=5)
        self.load_combo_khachhang()

        # Frame chọn sản phẩm
        frame_chon_sp = tk.Frame(dialog)
        frame_chon_sp.pack(fill="x", padx=10, pady=10)
        self.combo_sp = ttk.Combobox(frame_chon_sp)
        self.combo_sp.pack(side="left", padx=5)
        self.load_combo_sanpham()
        self.entry_sl = ttk.Entry(frame_chon_sp, width=10)
        self.entry_sl.pack(side="left", padx=5)
        self.entry_sl.insert(0, "1")
        btn_them_sp = ttk.Button(frame_chon_sp, text="Thêm vào đơn", command=self.them_sanpham)
        btn_them_sp.pack(side="left", padx=5)

        # Bảng sản phẩm đã chọn
        self.tree_sp = ttk.Treeview(dialog,
                                    columns=("Mã SP", "Tên SP", "Số lượng", "Đơn giá", "Thành tiền"),
                                    show="headings")
        self.tree_sp.heading("Mã SP", text="Mã SP")
        self.tree_sp.heading("Tên SP", text="Tên SP")
        self.tree_sp.heading("Số lượng", text="Số lượng")
        self.tree_sp.heading("Đơn giá", text="Đơn giá (VNĐ)")
        self.tree_sp.heading("Thành tiền", text="Thành tiền (VNĐ)")
        self.tree_sp.column("Mã SP", width=80)
        self.tree_sp.column("Tên SP", width=200)
        self.tree_sp.column("Số lượng", width=100)
        self.tree_sp.column("Đơn giá", width=120)
        self.tree_sp.column("Thành tiền", width=150)
        self.tree_sp.pack(fill="both", expand=True, padx=10, pady=10)
        self.lbl_tongtien = tk.Label(dialog, text="Tổng tiền: 0 VNĐ", font=("Arial", 12, "bold"))
        self.lbl_tongtien.pack(pady=10)
        btn_luu = ttk.Button(dialog, text="Lưu đơn hàng", command=lambda: self.luu_donhang(dialog))
        btn_luu.pack(pady=10)

    def load_combo_sanpham(self):
        products = self.product_controller.get_all_products()
        self.combo_sp['values'] = [f"{sp[0]} - {sp[1]}" for sp in products]

    def load_combo_khachhang(self):
        customers = self.khachhang_controller.get_all_khachhang()
        self.combo_kh['values'] = [f"{kh[0]} - {kh[1]}" for kh in customers]

    def them_sanpham(self):
        selected = self.combo_sp.get()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm!")
            return
        ma_sp = selected.split(" - ")[0]
        sanpham = self.product_controller.get_product_by_id(ma_sp)
        if sanpham:
            try:
                so_luong = int(self.entry_sl.get())
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Số lượng phải là số!")
                return
            thanh_tien = sanpham[2] * so_luong
            self.danh_sach_sanpham.append({
                'ma_sanpham': ma_sp,
                'ten': sanpham[1],
                'gia': sanpham[2],
                'so_luong': so_luong,
                'thanh_tien': thanh_tien
            })
            self.tree_sp.insert("", "end", values=(
                ma_sp,
                sanpham[1],
                so_luong,
                f"{sanpham[2]:,}",
                f"{thanh_tien:,}"
            ))
            self.capnhat_tongtien()

    def capnhat_tongtien(self):
        tong = sum(item['thanh_tien'] for item in self.danh_sach_sanpham)  # Sử dụng danh sách đã được khai báo
        self.lbl_tongtien.config(text=f"Tổng tiền: {tong:,} VNĐ")

    def luu_donhang(self, dialog):
        if len(self.danh_sach_sanpham) == 0:
            messagebox.showwarning("Cảnh báo", "Vui lòng thêm sản phẩm vào đơn hàng!")
            return
        selected_kh = self.combo_kh.get() if hasattr(self, 'combo_khachhang') else self.combo_kh.get()
        if not selected_kh:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng!")
            return
        ma_khachhang = selected_kh.split(" - ")[0]
        if self.donhang_controller.tao_donhang(ma_khachhang, self.danh_sach_sanpham):
            messagebox.showinfo("Thành công", "Lưu đơn hàng thành công!")
            self.load_data()
            dialog.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu đơn hàng!")

    def load_data(self, search_term=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if search_term:
            donhangs = self.donhang_controller.search_donhang(search_term)
        else:
            donhangs = self.donhang_controller.get_all_donhang()
        # Giả sử mỗi đơn hàng trả về là: (ma_dh, ma_kh, ten_kh, ngay_dat, tong_tien)
        for dh in donhangs:
            ma_dh, ma_kh, ten_kh, ngay_dat, tong_tien = dh
            self.tree.insert("", "end", values=(
                ma_dh,
                ma_kh,
                ten_kh,
                ngay_dat.strftime("%d/%m/%Y"),
                f"{tong_tien:,.0f} VNĐ"
            ))

    def search_donhang(self):
        search_term = self.search_var.get()
        self.load_data(search_term)

    def clear_search(self):
        self.search_var.set("")
        self.load_data()

    def xoa_donhang(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đơn hàng cần xóa!")
            return
        ma_donhang = self.tree.item(selected)['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa đơn hàng #{ma_donhang}?"):
            if self.donhang_controller.xoa_donhang(ma_donhang):
                messagebox.showinfo("Thành công", "Đơn hàng đã được xóa thành công!")
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa đơn hàng!")


