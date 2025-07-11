from models.product_model import ProductModel

class ProductController:
    def __init__(self):
        self.connection = None
        self.model = ProductModel()

    def get_all_products(self):
        return self.model.get_all_products()

    def add_product(self, data):
        return self.model.add_product(
            data['ten'],
            data['gia'],
            data['soluong'],
            data['mota'],
            data['madanhmuc']
        )

    def update_product(self, ma, data):
        return self.model.update_product(
            ma,
            data['ten'],
            data['gia'],
            data['soluong'],
            data['mota'],
            data['madanhmuc']
        )

    def delete_product(self, ma):
        return self.model.delete_product(ma)

    def search_products(self, keyword):
        return self.model.search_products(keyword)

    # Trong ProductController
    def get_product_by_id(self, ma_sp):
        try:
            cursor = self.model.connection.cursor()
            cursor.execute("SELECT * FROM sanpham WHERE maSanPham = %s", (ma_sp,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Lỗi khi lấy sản phẩm: {e}")
            return None