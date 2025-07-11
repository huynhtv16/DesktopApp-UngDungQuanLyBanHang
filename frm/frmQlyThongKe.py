import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.thongke_controller import ThongKeController
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class FrmQlyThongKe(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50")
        self.controller = ThongKeController()
        self.current_figure = None
        self.create_widgets()
        self.configure_style()

    def configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", background="#34495e", foreground="white")

    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Control Panel
        control_frame = tk.Frame(main_frame, bg="#2c3e50")
        control_frame.pack(fill="x", pady=10)

        # Date selection
        tk.Label(control_frame, text="Từ ngày:", bg="#2c3e50", fg="white").pack(side="left", padx=5)
        self.start_date = DateEntry(control_frame, date_pattern="yyyy-mm-dd")
        self.start_date.pack(side="left", padx=5)

        tk.Label(control_frame, text="Đến ngày:", bg="#2c3e50", fg="white").pack(side="left", padx=5)
        self.end_date = DateEntry(control_frame, date_pattern="yyyy-mm-dd")
        self.end_date.pack(side="left", padx=5)

        # Buttons
        ttk.Button(control_frame, text="Thống kê theo ngày", command=self.ve_bieudo_ngay).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Thống kê theo tháng", command=self.ve_bieudo_thang).pack(side="left", padx=5)
        ttk.Button(control_frame, text="SP bán chạy", command=self.ve_bieudo_sp).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Xuất Excel", command=self.xuat_excel).pack(side="left", padx=5)

        # Chart area
        self.chart_frame = tk.Frame(main_frame, bg="#2c3e50")
        self.chart_frame.pack(expand=True, fill="both")

    def clear_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def ve_bieudo_ngay(self):
        self.clear_chart()
        data = self.controller.get_data_thongke(
            self.start_date.get_date(),
            self.end_date.get_date()
        )

        dates = [item[0].strftime("%d-%m") for item in data]
        values = [item[1] for item in data]

        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(dates, values, color="#16a085")
        ax.set_title("Thống kê doanh thu theo ngày")
        ax.set_ylabel("Doanh thu (VNĐ)")

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def ve_bieudo_thang(self):
        self.clear_chart()
        current_year = pd.Timestamp.now().year
        data = self.controller.get_data_theo_thang(current_year)

        months = [f"Tháng {item[0]}" for item in data]
        values = [item[1] for item in data]

        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(months, values, marker="o", color="#e74c3c")
        ax.set_title("Thống kê doanh thu theo tháng")
        ax.set_ylabel("Doanh thu (VNĐ)")

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def ve_bieudo_sp(self):
        self.clear_chart()
        data = self.controller.get_top_sanpham()

        products = [item[0] for item in data]
        quantities = [item[1] for item in data]

        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(quantities, labels=products, autopct="%1.1f%%",
               colors=["#16a085", "#2980b9", "#8e44ad", "#f39c12", "#c0392b"])
        ax.set_title("Top sản phẩm bán chạy")

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def xuat_excel(self):
        data = self.controller.get_data_thongke(
            self.start_date.get_date(),
            self.end_date.get_date()
        )

        filename = "thongke.xlsx"
        if self.controller.xuat_excel(data, filename):
            messagebox.showinfo("Thành công", f"Đã xuất file {filename}")
        else:
            messagebox.showerror("Lỗi", "Xuất file thất bại")
