import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="P@ssword123",
                database="qlycuahang",
                port=3308
            )
            print("Kết nối database thành công!")
        except Error as e:
            print(f"Lỗi kết nối database: {e}")

    def get_connection(self):
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()