import tkinter as tk
from tkinter import messagebox
from ui.translation_screen import TranslationScreen
from ui.my_words_screen import MyWordsScreen
from ui.game_screen import GameScreen
from ui.user_login_screen import UserLoginScreen  # Giả sử bạn có một màn hình đăng nhập
from database.user_database import UserDatabase

class EnglishLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English Learning App")
        self.root.geometry("800x500")  # Tăng kích thước cửa sổ

        self.db = UserDatabase()  # Khởi tạo cơ sở dữ liệu người dùng
        self.current_user = None  # Biến lưu trữ người dùng hiện tại

        self.create_menu()
        self.show_login_screen()  # Hiển thị màn hình đăng nhập đầu tiên

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Tạo các menu riêng biệt
        menubar.add_command(label="Dịch", command=self.show_translation_screen)
        menubar.add_command(label="Từ của bạn", command=self.show_my_words_screen)
        menubar.add_command(label="Trò chơi", command=self.show_game_screen)

        # Thêm menu Tài khoản
        account_menu = tk.Menu(menubar, tearoff=0)
        account_menu.add_command(label="Đăng xuất", command=self.logout)
        menubar.add_cascade(label="Tài khoản", menu=account_menu)

    def show_login_screen(self):
        self.clear_frames()
        self.login_screen = UserLoginScreen(self.root, self)
        self.login_screen.show()  # Hiển thị màn hình đăng nhập

    def show_translation_screen(self):
        self.clear_frames()
        self.translation_screen = TranslationScreen(self.root, self)
        self.translation_screen.show()

    def show_my_words_screen(self):
        if not self.current_user:
            messagebox.showwarning("Cảnh báo", "Bạn cần đăng nhập để xem từ của mình!")
            self.show_login_screen()
            return
        self.clear_frames()
        self.my_words_screen = MyWordsScreen(self.root, self)
        self.my_words_screen.show()

    def show_game_screen(self):
        self.clear_frames()
        self.game_screen = GameScreen(self.root, self)
        self.game_screen.show()

    def clear_frames(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def logout(self):
        self.current_user = None  # Đặt người dùng hiện tại về None
        self.show_login_screen()  # Hiển thị lại màn hình đăng nhập

if __name__ == "__main__":
    root = tk.Tk()
    app = EnglishLearningApp(root)
    root.mainloop()