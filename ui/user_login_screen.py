import tkinter as tk
from tkinter import messagebox
from database.user_database import UserDatabase
import re

class UserLoginScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.db = UserDatabase()  # Khởi tạo cơ sở dữ liệu người dùng

        self.frame = tk.Frame(self.root, bg="#f5f5f5")  # Màu nền nhẹ cho toàn bộ frame

        # Các widget cho màn hình đăng nhập
        self.label_username = tk.Label(self.frame, text="Tên đăng nhập:", font=("Arial", 14), bg="#f5f5f5", fg="#004d40")
        self.entry_username = tk.Entry(self.frame, font=("Arial", 14), width=30, bg="#ffffff", fg="#000000")
        self.label_password = tk.Label(self.frame, text="Mật khẩu:", font=("Arial", 14), bg="#f5f5f5", fg="#004d40")
        self.entry_password = tk.Entry(self.frame, show='*', font=("Arial", 14), width=30, bg="#ffffff", fg="#000000")
        
        self.button_login = tk.Button(self.frame, text="Đăng nhập", command=self.login, font=("Arial", 12), bg="#b2ebf2", fg="#004d40")
        self.button_register = tk.Button(self.frame, text="Đăng ký", command=self.register, font=("Arial", 12), bg="#ffccbc", fg="#004d40")

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Sắp xếp các widget
        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_login.pack(pady=10)
        self.button_register.pack(pady=10)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        user = self.db.get_user(username)
        if user and user['password'] == password:
            self.app.current_user = user  # Lưu thông tin người dùng hiện tại
            messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {username}!")
            self.app.show_translation_screen()  # Chuyển đến màn hình dịch
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

    def register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

    # Kiểm tra tên tài khoản không có ký tự đặc biệt
        if not re.match("^[A-Za-z0-9_]*$", username):
            messagebox.showerror("Lỗi", "Tên đăng nhập không được chứa ký tự đặc biệt!")
            return

        # Kiểm tra mật khẩu dài hơn 6 ký tự
        if len(password) <= 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải dài hơn 6 ký tự!")
            return

        if self.db.add_user(username, password):
            messagebox.showinfo("Đăng ký thành công", f"Bạn đã đăng ký thành công với tên đăng nhập: {username}")
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")