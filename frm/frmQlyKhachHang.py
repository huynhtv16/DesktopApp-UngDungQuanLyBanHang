import tkinter as tk
from tkinter import ttk, messagebox
from controllers.khachhang_controller import KhachHangController


class FrmQlyKhachHang(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50")
        self.controller = KhachHangController()
        self.selected_kh = None
        self.create_widgets()
        self.configure_style()
        self.load_data()

    def configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Treeview",
                             background="#34495e",
                             foreground="white",
                             fieldbackground="#34495e",
                             rowheight=25)

        self.style.configure("Treeview.Heading",
                             background="#16a085",
                             foreground="white",
                             font=("Arial", 12, "bold"))
        # Style cho nút
        self.style.map("TButton",
                       background=[("active", "#3498db"), ("!disabled", "#2980b9")],
                       foreground=[("!disabled", "white")])
        # thanh tim kiem
        self.style.configure("Search.TEntry",
                             fieldbackground="#34495e",
                             foreground="white")

    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Thanh tìm kiếm
        search_frame = tk.Frame(main_frame, bg="#2c3e50")
        search_frame.pack(fill="x", pady=5)

        self.search_var = tk.StringVar()
        self.entry_search = ttk.Entry(search_frame,
                                      textvariable=self.search_var,
                                      width=40,
                                      style="Search.TEntry")
        self.entry_search.pack(side="left", padx=5)
        self.entry_search.insert(0, "Nhập từ khóa...")
        self.entry_search.bind("<FocusIn>", lambda e: self.entry_search.delete(0, "end"))
        self.entry_search.bind("<Return>", lambda e: self.search_khachhang())

        ttk.Button(search_frame,
                   text="🔍 Tìm kiếm",
                   command=self.search_khachhang).pack(side="left", padx=5)

        ttk.Button(search_frame,
                   text="❌ Xóa tìm",
                   command=self.clear_search).pack(side="left", padx=5)

        # Bảng khách hàng
        self.tree = ttk.Treeview(main_frame,
                                 columns=("MaKH", "TenKH", "SDT", "DiaChi"),
                                 show="headings",
                                 height=15)

        # Cấu hình cột
        columns = [
            ("MaKH", "Mã KH", 100),
            ("TenKH", "Tên Khách Hàng", 200),
            ("SDT", "Số Điện Thoại", 150),
            ("DiaChi", "Địa Chỉ", 300)
        ]

        for col_id, col_text, width in columns:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=width, anchor="w")

        self.tree.pack(expand=True, fill="both", pady=10)

        # Nút chức năng
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=10)

        buttons = [
            ("➕ Thêm", self.show_add_dialog),
            ("✏️ Sửa", self.show_edit_dialog),
            ("🗑️ Xóa", self.delete_khachhang),
            ("🔄 Làm mới", self.load_data)
        ]

        for text, cmd in buttons:
            ttk.Button(btn_frame,
                       text=text,
                       command=cmd).pack(side="left", padx=5)

    def load_data(self, search_term=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if search_term:
            data = self.controller.search_khachhang(search_term)
        else:
            data = self.controller.get_all_khachhang()

        for kh in data:
            self.tree.insert("", "end", values=kh)

    def search_khachhang(self):
        search_term = self.search_var.get()
        self.load_data(search_term)

    def clear_search(self):
        self.search_var.set("")
        self.load_data()

    def show_add_dialog(self):
        self._show_dialog("Thêm Khách Hàng")

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng!")
            return
        self.selected_kh = self.tree.item(selected[0])['values']
        self._show_dialog("Sửa Khách Hàng", self.selected_kh)

    def _show_dialog(self, title, data=None):
        dialog = tk.Toplevel()
        dialog.title(title)

        # Tạo các ô nhập liệu
        labels = ["Tên Khách Hàng:", "Số Điện Thoại:", "Địa Chỉ:"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            if data:
                entry.insert(0, data[i + 1])
            entries[label] = entry

        def save():
            ten = entries["Tên Khách Hàng:"].get()
            sdt = entries["Số Điện Thoại:"].get()
            diachi = entries["Địa Chỉ:"].get()

            if not ten or not sdt:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin bắt buộc!")
                return

            if title == "Thêm Khách Hàng":
                success = self.controller.add_khachhang(ten, sdt, diachi)
            else:
                success = self.controller.update_khachhang(self.selected_kh[0], ten, sdt, diachi)

            if success:
                self.load_data()
                dialog.destroy()

        ttk.Button(dialog, text="Lưu", command=save).grid(row=3, columnspan=2, pady=10)

    def delete_khachhang(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng!")
            return

        ma_kh = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa?"):
            if self.controller.delete_khachhang(ma_kh):
                self.load_data()