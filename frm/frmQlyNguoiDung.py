import tkinter as tk
from tkinter import ttk, messagebox
from controllers.nguoidung_controller import NguoiDungController


class FrmQlyNguoiDung(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50")
        self.controller = NguoiDungController()
        self.selected_user = None
        self.create_widgets()
        self.configure_style()
        self.load_data()

    def configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Cấu hình style Treeview
        self.style.configure("Treeview",
                             background="#34495e",
                             foreground="white",
                             fieldbackground="#34495e",
                             rowheight=25,
                             bordercolor="#16a085")

        self.style.configure("Treeview.Heading",
                             background="#16a085",
                             foreground="white",
                             font=("Arial", 12, "bold"))

        # Style cho nút
        self.style.map("TButton",
                       background=[("active", "#3498db"), ("!disabled", "#2980b9")],
                       foreground=[("!disabled", "white")])
        #thanh tim kiem
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
        self.entry_search.bind("<Return>", lambda e: self.search_user())

        ttk.Button(search_frame,
                   text="🔍 Tìm kiếm",
                   command=self.search_user).pack(side="left", padx=5)

        ttk.Button(search_frame,
                   text="❌ Xóa tìm",
                   command=self.clear_search).pack(side="left", padx=5)

        # Bảng dữ liệu
        self.tree = ttk.Treeview(main_frame,
                                 columns=("ID", "Tài khoản", "Mật khẩu", "Họ tên", "Chức vụ"),
                                 show="headings")
        # Cấu hình cột
        columns = [
            ("ID", "Mã ND", 80),
            ("Tài khoản", "Tài khoản", 150),
            ("Mật khẩu", "Mật khẩu", 150),  # Thêm cột mật khẩu
            ("Họ tên", "Họ tên", 200),
            ("Chức vụ", "Chức vụ", 150)
        ]

        for col_id, col_text, width in columns:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=width, anchor="center")

        self.tree.pack(expand=True, fill="both", pady=10)

        # Nút chức năng
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=10)

        buttons = [
            ("➕ Thêm", self.show_add_dialog),
            ("✏️ Sửa", self.show_edit_dialog),
            ("🗑️ Xóa", self.delete_user),
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

        users = self.controller.search_users(search_term) if search_term else self.controller.get_all_users()

        for user in users:
            # Hiển thị mật khẩu (đã mã hóa trong CSDL)
            self.tree.insert("", "end", values=user)

    def search_user(self):
        search_term = self.search_var.get()
        self.load_data(search_term)

    def clear_search(self):
        self.search_var.set("")
        self.load_data()

    def show_add_dialog(self):
        self._show_dialog("Thêm người dùng")

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng!")
            return
        self.selected_user = self.tree.item(selected[0])['values']
        self._show_dialog("Sửa người dùng", self.selected_user)

    def _show_dialog(self, title, data=None):
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.grab_set()

        # Combobox chức vụ
        chucvu_list = self.controller.get_chucvu_list()
        chucvu_dict = {cv[1]: cv[0] for cv in chucvu_list}

        entries = {}
        labels = ["Tài khoản", "Mật khẩu", "Họ tên", "Chức vụ"]
        for i, label in enumerate(labels):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            if label == "Chức vụ":
                combo = ttk.Combobox(dialog, values=[cv[1] for cv in chucvu_list])
                if data:
                    combo.set(data[3])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries[label] = combo
            else:
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                if data and label != "Mật khẩu":
                    entry.insert(0, data[labels.index(label) + 1])
                entries[label] = entry

        def save():
            data = {
                'taikhoan': entries["Tài khoản"].get(),
                'matkhau': entries["Mật khẩu"].get() if title == "Thêm người dùng" else "",
                'hofen': entries["Họ tên"].get(),
                'maChucVu': chucvu_dict[entries["Chức vụ"].get()]
            }

            if title == "Thêm người dùng":
                if self.controller.add_user(data):
                    self.load_data()
                    dialog.destroy()
            else:
                if self.controller.update_user(self.selected_user[0], data):
                    self.load_data()
                    dialog.destroy()

        ttk.Button(dialog, text="Lưu", command=save).grid(row=4, columnspan=2, pady=10)

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng!")
            return

        user_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa?"):
            if self.controller.delete_user(user_id):
                self.load_data()