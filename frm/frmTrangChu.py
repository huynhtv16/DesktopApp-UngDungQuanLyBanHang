import tkinter as tk
from tkinter import font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controllers.thongke_controller import ThongKeController


class TrangChuForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c2f3f")
        self.controller = ThongKeController()
        self.parent = parent
        self.title_font = font.Font(family="Arial", size=20, weight="bold")
        self.card_title_font = font.Font(family="Arial", size=12, weight="bold")
        self.card_value_font = font.Font(family="Arial", size=16, weight="bold")
        self.chart_font = font.Font(family="Arial", size=14)

        self.create_widgets()
        self.update_data()

    def create_widgets(self):
        # Main content frame
        main_frame = tk.Frame(self, bg="#2c2f3f")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        lbl_title = tk.Label(main_frame,
                             text="TRANG CHỦ",
                             font=self.title_font,
                             fg="white",
                             bg="#2c2f3f")
        lbl_title.pack(pady=(0, 20))

        # Stats cards
        self.cards_frame = tk.Frame(main_frame, bg="#2c2f3f")
        self.cards_frame.pack(fill="x", pady=10)

        self.card_donhang = self.create_stat_card(self.cards_frame,
                                                  "Số đơn bán ra trong ngày:",
                                                  "0", "#8E44AD")
        self.card_donhang.grid(row=0, column=0, padx=10)

        self.card_doanhthu = self.create_stat_card(self.cards_frame,
                                                   "Doanh thu ngày:",
                                                   "0 VNĐ", "#F39C12")
        self.card_doanhthu.grid(row=0, column=1, padx=10)

        self.card_sanpham = self.create_stat_card(self.cards_frame,
                                                  "Số sản phẩm bán trong ngày:",
                                                  "0", "#16A085")
        self.card_sanpham.grid(row=0, column=2, padx=10)

        # Chart section
        self.chart_frame = tk.Frame(main_frame, bg="#2c2f3f")
        self.chart_frame.pack(expand=True, fill="both", padx=20, pady=10)

    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent,
                        bg=color,
                        width=220,
                        height=100,
                        bd=0,
                        highlightthickness=0)

        # Rounded corners
        canvas = tk.Canvas(card,
                           bg=color,
                           highlightthickness=0,
                           width=220,
                           height=100)
        canvas.create_rounded_rectangle(0, 0, 220, 100, radius=10, fill=color)
        canvas.place(x=0, y=0)

        # Content
        lbl_title = tk.Label(card,
                             text=title,
                             font=self.card_title_font,
                             fg="white",
                             bg=color,
                             wraplength=200,
                             anchor="w")
        lbl_title.place(x=15, y=10)

        lbl_value = tk.Label(card,
                             text=value,
                             font=self.card_value_font,
                             fg="white",
                             bg=color,
                             anchor="w")
        lbl_value.place(x=15, y=50)

        return card

    def update_data(self):
        # Cập nhật số liệu thống kê
        data = self.controller.get_data_trangchu()
        if data:
            self.card_donhang.children["!label2"].config(text=str(data['so_don']))
            self.card_doanhthu.children["!label2"].config(text=f"{data['doanh_thu']:,.0f} VNĐ")
            self.card_sanpham.children["!label2"].config(text=str(data['so_sanpham']))

        # Vẽ biểu đồ
        self.draw_chart()

    def draw_chart(self):
        # Xóa biểu đồ cũ
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Lấy dữ liệu từ CSDL
        data = self.controller.get_sanpham_ban_ngay()

        if not data:
            lbl = tk.Label(self.chart_frame,
                           text="Không có dữ liệu bán hàng hôm nay",
                           bg="#2c2f3f",
                           fg="white",
                           font=self.chart_font)
            lbl.pack(pady=50)
            return

        # Chuẩn bị dữ liệu cho biểu đồ
        products = [item[0] for item in data]
        quantities = [item[1] for item in data]

        # Tạo biểu đồ cột
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Vẽ biểu đồ
        bars = ax.bar(products, quantities, color="#16a085")

        # Cấu hình style
        ax.set_title("Sản phẩm bán chạy trong ngày", color="white", pad=20)
        ax.set_ylabel("Số lượng bán", color="white")
        ax.set_xlabel("Tên sản phẩm", color="white")
        ax.tick_params(axis='x', rotation=45, colors="white")
        ax.tick_params(axis='y', colors="white")
        ax.set_facecolor("#2c2f3f")
        fig.patch.set_facecolor("#2c2f3f")

        # Thêm số liệu lên từng cột
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}',
                    ha='center', va='bottom',
                    color="white")

        # Nhúng vào GUI
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)

# Add rounded rectangle method to Canvas
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return self.create_polygon(points, **kwargs, smooth=True)


tk.Canvas.create_rounded_rectangle = create_rounded_rectangle