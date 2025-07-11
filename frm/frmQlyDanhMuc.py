import tkinter as tk
from tkinter import ttk, messagebox
from controllers.danhmuc_controller import DanhMucController


class FrmQlyDanhMuc(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50")
        self.controller = DanhMucController()
        self.selected_danhmuc = None
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
        self.style.map("TButton",
                       background=[("active", "#3498db"), ("!disabled", "#2980b9")],
                       foreground=[("!disabled", "white")])
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
                                      style="Search.TEntry"
                                      )
        self.entry_search.pack(side="left", padx=5)
        self.entry_search.insert(0, "Nhập từ khóa...")
        self.entry_search.bind("<FocusIn>", lambda e: self.entry_search.delete(0, "end"))
        self.entry_search.bind("<Return>", lambda e: self.search_danhmuc())

        ttk.Button(search_frame,
                   text="🔍 Tìm kiếm",
                   command=self.search_danhmuc).pack(side="left", padx=5)

        ttk.Button(search_frame,
                   text="❌ Xóa tìm",
                   command=self.clear_search).pack(side="left", padx=5)

        # Bảng danh mục
        self.tree = ttk.Treeview(main_frame,
                                 columns=("MaDM", "TenDM"),
                                 show="headings")

        self.tree.heading("MaDM", text="Mã DM")
        self.tree.heading("TenDM", text="Tên Danh Mục")

        self.tree.column("MaDM", width=100, anchor="center")
        self.tree.column("TenDM", width=300)

        self.tree.pack(expand=True, fill="both", pady=10)

        # Nút chức năng
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=10)

        buttons = [
            ("➕ Thêm", self.show_add_dialog),
            ("✏️ Sửa", self.show_edit_dialog),
            ("🗑️ Xóa", self.delete_danhmuc),
            ("🔄 Làm mới", self.load_data)
        ]

        for text, cmd in buttons:
            ttk.Button(btn_frame,
                       text=text,
                       command=cmd,
                       style="TButton").pack(side="left", padx=5)

    def load_data(self, search_term=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if search_term:
            data = self.controller.search_danhmuc(search_term)
        else:
            data = self.controller.get_all_danhmuc()

        for dm in data:
            self.tree.insert("", "end", values=dm)

    def search_danhmuc(self):
        search_term = self.search_var.get()
        self.load_data(search_term)

    def clear_search(self):
        self.search_var.set("")
        self.load_data()

    def show_add_dialog(self):
        self._show_dialog("Thêm Danh Mục")

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn danh mục!")
            return
        self.selected_danhmuc = self.tree.item(selected[0])['values']
        self._show_dialog("Sửa Danh Mục", self.selected_danhmuc)

    def _show_dialog(self, title, data=None):
        dialog = tk.Toplevel()
        dialog.title(title)

        tk.Label(dialog, text="Tên Danh Mục:").grid(row=0, column=0, padx=5, pady=5)
        entry_ten = ttk.Entry(dialog, width=30)
        entry_ten.grid(row=0, column=1, padx=5, pady=5)

        if data:
            entry_ten.insert(0, data[1])

        def save():
            ten_dm = entry_ten.get()
            if not ten_dm:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên danh mục")
                return

            if title == "Thêm Danh Mục":
                if self.controller.add_danhmuc(ten_dm):
                    self.load_data()
                    dialog.destroy()
            else:
                if self.controller.update_danhmuc(self.selected_danhmuc[0], ten_dm):
                    self.load_data()
                    dialog.destroy()

        ttk.Button(dialog, text="Lưu", command=save).grid(row=1, columnspan=2, pady=10)

    def delete_danhmuc(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn danh mục!")
            return

        ma_dm = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa?"):
            if self.controller.delete_danhmuc(ma_dm):
                self.load_data()