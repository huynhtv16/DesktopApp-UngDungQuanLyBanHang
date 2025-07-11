# 🛒 Ứng dụng Quản lý Bán Hàng - Python Desktop App

Dự án này là một ứng dụng quản lý bán hàng nhỏ lẻ được xây dựng bằng ngôn ngữ Python theo mô hình MVC. Ứng dụng có giao diện thân thiện, hỗ trợ quản lý sản phẩm, đơn hàng, tạo mã QR và thống kê hiệu quả bán hàng theo ngày/tháng.

## ✅ Tính năng chính

- 📦 **Quản lý sản phẩm**
  - Thêm, sửa, xóa sản phẩm
  - Thêm sản phẩm qua **quét mã QR**
  - Tạo và hiển thị QR code cho từng sản phẩm

- 🛍️ **Tạo đơn hàng**
  - Thêm sản phẩm vào giỏ hàng
  - In hóa đơn (hỗ trợ xuất đơn hàng có QR code)

- 📊 **Thống kê**
  - Thống kê doanh thu theo ngày, tháng
  - Xem loại sản phẩm bán chạy nhất

- 🖼️ **Giao diện đồ họa**
  - Xây dựng bằng **Tkinter**
  - Sử dụng thư viện **Matplotlib** để hiển thị biểu đồ
## 📸 Hình ảnh minh họa
<img width="794" height="543" alt="image" src="https://github.com/user-attachments/assets/51a881dd-9f99-4824-b760-ab681b360438" />
<img width="789" height="495" alt="image" src="https://github.com/user-attachments/assets/febb81c2-4542-4009-a9bc-4dda046b3770" />
<img width="794" height="524" alt="image" src="https://github.com/user-attachments/assets/321c3366-57aa-448d-87dc-3c6f9c57b329" />
<img width="805" height="503" alt="image" src="https://github.com/user-attachments/assets/dabd7161-cf3b-42ee-b386-b4d813b0f822" />
<img width="788" height="533" alt="image" src="https://github.com/user-attachments/assets/9e4416f2-84f3-4da2-b796-960f62a191d1" />
<img width="782" height="469" alt="image" src="https://github.com/user-attachments/assets/f217e5a6-3933-4643-90a5-f12ed12de43f" />
<img width="797" height="495" alt="image" src="https://github.com/user-attachments/assets/afc275c9-fb7f-4e84-a340-04156f82d294" />
## 🧱 Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.x
- **Giao diện:** Tkinter
- **Thư viện phụ trợ:** `qrcode`, `Pillow`, `matplotlib`, `mysql-connector-python`
- **Cơ sở dữ liệu:** MySQL (hoặc SQLite nếu chuyển đổi)
- **Kiến trúc:** MVC (Model – View – Controller)

## 📂 Cấu trúc thư mục
```
📦 QuảnLýBánHàng
│
├── controllers/ # Xử lý logic, giao tiếp giữa view và model
│
├── frm/ # Các form giao diện người dùng (UI)
│ ├── form_sanpham.py
│ ├── form_donhang.py
│ └── ...
│
├── icons/ # Icon giao diện (nút, biểu tượng, trạng thái...)
│
├── img/ # Ảnh sản phẩm hoặc ảnh QR code sinh ra
│
├── models/ # Xử lý truy vấn cơ sở dữ liệu
│ ├── sanpham_model.py
│ ├── donhang_model.py
│ └── ...
│
├── main.py # File khởi chạy chương trình
├── menu.py # Menu điều hướng chính
├── utils.py # Các hàm tiện ích như sinh QR, xử lý thời gian, format
```
📌 Ghi chú
Dự án phù hợp để áp dụng cho cửa hàng nhỏ, cá nhân bán hàng

Có thể dễ dàng mở rộng thêm: quản lý khách hàng, phân quyền người dùng, in hóa đơn thực tế

Có thể tích hợp thêm OpenCV để quét mã QR từ camera
