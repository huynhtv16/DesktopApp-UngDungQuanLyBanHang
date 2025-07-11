import tkinter as tk
from tkinter import ttk, messagebox
from controllers.product_controller import ProductController


class FrmQlySanPham(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50")
        self.controller = ProductController()
        self.selected_product = None
        self.create_widgets()
        self.configure_style()
        self.load_data()

    def configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Cấu hình style cho Treeview
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

        self.style.map("TButton",
                       background=[("active", "#3498db"), ("!disabled", "#2980b9")],
                       foreground=[("!disabled", "white")])

        self.style.configure("Search.TEntry",
                             fieldbackground="#34495e",
                             foreground="white")

    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Phần tìm kiếm
        search_frame = tk.Frame(main_frame, bg="#2c3e50")
        search_frame.pack(fill="x", pady=5)

        self.search_var = tk.StringVar()
        self.entry_search = ttk.Entry(search_frame,
                                      textvariable=self.search_var,
                                      width=30,
                                      style="Search.TEntry")
        self.entry_search.pack(side="left", padx=5)
        self.entry_search.insert(0, "Nhập tên sản phẩm...")
        self.entry_search.bind("<FocusIn>", lambda e: self.entry_search.delete(0, "end"))
        self.entry_search.bind("<Return>", lambda e: self.search_product())

        ttk.Button(search_frame,
                   text="🔍 Tìm kiếm",
                   command=self.search_product).pack(side="left", padx=5)

        ttk.Button(search_frame,
                   text="❌ Xóa tìm",
                   command=self.clear_search).pack(side="left", padx=5)

        # Bảng dữ liệu
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame,
                                 columns=("ID", "Tên", "Giá", "SL", "Mô tả", "Mã DM"),
                                 show="headings")
        columns = [
            ("ID", "Mã SP"),
            ("Tên", "Tên SP"),
            ("Giá", "Giá"),
            ("SL", "Số lượng"),
            ("Mô tả", "Mô tả"),
            ("Mã DM", "Mã DM")
        ]
        for col_id, col_text in columns:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, minwidth=50, anchor="center", stretch=True)

        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Ràng buộc sự kiện thay đổi kích thước để cập nhật lại chiều rộng các cột
        self.tree.bind("<Configure>", self.update_column_widths)

        # Nút chức năng
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=10)

        buttons = [
            ("➕ Thêm", self.show_add_dialog),
            ("✏️ Sửa", self.show_edit_dialog),
            ("🗑️ Xóa", self.delete_product),
            ("🔄 Làm Mới", self.load_data)
        ]

        for text, command in buttons:
            ttk.Button(btn_frame,
                       text=text,
                       command=command).pack(side="left", padx=5, ipadx=10)

    def update_column_widths(self, event):
        # Lấy chiều rộng hiện tại của Treeview
        tree_width = self.tree.winfo_width()
        # Đặt tỷ lệ cho mỗi cột: (tùy chỉnh theo ý muốn)
        relative_widths = [0.1, 0.3, 0.15, 0.15, 0.2, 0.1]  # Tổng = 1.0
        for i, col in enumerate(self.tree["columns"]):
            new_width = int(tree_width * relative_widths[i])
            self.tree.column(col, width=new_width)

    def load_data(self, search_term=None):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Nếu có từ khóa tìm kiếm thì gọi phương thức tìm kiếm, nếu không thì lấy tất cả sản phẩm
        if search_term:
            products = self.controller.search_products(search_term)
        else:
            products = self.controller.get_all_products()

        # Load dữ liệu vào Treeview
        for product in products:
            self.tree.insert('', 'end', values=product)

    def search_product(self):
        search_term = self.search_var.get()
        self.load_data(search_term)

    def clear_search(self):
        self.search_var.set("")
        self.load_data()

    def show_add_dialog(self):
        self._show_dialog("Thêm sản phẩm")

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm!")
            return
        self.selected_product = self.tree.item(selected[0])['values']
        self._show_dialog("Sửa sản phẩm", self.selected_product)

    def _show_dialog(self, title, data=None):
        dialog = tk.Toplevel()
        dialog.title(title)

        entries = {}
        labels = ["Tên SP", "Giá", "Số lượng", "Mô tả", "Mã DM"]
        for i, label in enumerate(labels):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(dialog)
            entry.grid(row=i, column=1, padx=5, pady=5)
            if data:
                entry.insert(0, data[i + 1])
            entries[label] = entry

        def save():
            data = {
                'ten': entries["Tên SP"].get(),
                'gia': entries["Giá"].get(),
                'soluong': entries["Số lượng"].get(),
                'mota': entries["Mô tả"].get(),
                'madanhmuc': entries["Mã DM"].get()
            }
            if title == "Thêm sản phẩm":
                success = self.controller.add_product(data)
            else:
                success = self.controller.update_product(self.selected_product[0], data)

            if success:
                self.load_data()
                dialog.destroy()

        ttk.Button(dialog, text="Lưu", command=save).grid(row=5, columnspan=2, pady=10)

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm!")
            return
        product_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa?"):
            if self.controller.delete_product(product_id):
                self.load_data()
