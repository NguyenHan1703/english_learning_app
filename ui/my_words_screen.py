import tkinter as tk
from database.word_database import WordDatabase
from tkinter import simpledialog, messagebox
from plyer import notification
import schedule
import time
import threading
import pyttsx3  # Nhập thư viện pyttsx3

class MyWordsScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.db = WordDatabase()
        self.engine = pyttsx3.init()  # Khởi tạo engine pyttsx3
        
        # Thay đổi giọng đọc
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Chọn giọng đọc thứ hai (thay đổi chỉ số tùy theo giọng bạn muốn)

        # Thay đổi tốc độ đọc
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate * 0.8)  # Giảm tốc độ đọc 10%

        self.frame = tk.Frame(self.root, bg="#f5f5f5")  # Màu nền nhẹ cho toàn bộ frame
        self.left_frame = tk.Frame(self.frame, bg="#e0f7fa")  # Màu nền nhẹ cho phần hiển thị từ
        self.right_frame = tk.Frame(self.frame, bg="#ffe0b2")  # Màu nền nhẹ cho phần nút

        self.listbox = tk.Listbox(self.left_frame, width=50, height=10, font=("Arial", 12), bg="#ffffff", fg="#000000")  # Màu nền và chữ cho listbox
        
        self.button_delete = tk.Button(self.right_frame, text="Xóa", command=self.delete_word, font=("Arial", 12), bg="#ffccbc", fg="#000000")
        self.button_notify = tk.Button(self.right_frame, text="Thông báo", command=self.set_notification, font=("Arial", 12), bg="#ffccbc", fg="#000000")
        self.button_read = tk.Button(self.right_frame, text="Đọc từ", command=self.read_word, font=("Arial", 12), bg="#ffccbc", fg="#000000")  # Nút đọc từ

        # Biến để lưu thời gian thông báo
        self.notification_time = None

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Hiển thị các phần của giao diện
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)  # Thêm khoảng cách
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)  # Thêm khoảng cách

        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.button_delete.pack(pady=10)
        self.button_notify.pack(pady=10)
        self.button_read.pack(pady=10)  # Thêm nút đọc từ
        self.display_words()

    def set_notification(self):
        # Nhập thời gian từ người dùng
        time_str = simpledialog.askstring("Đặt thời gian", "Nhập thời gian thông báo (HH:MM):")
        if time_str:
            self.notification_time = time_str
            # Lên lịch thông báo
            schedule.every().day.at(self.notification_time).do(self.send_notification)
            threading.Thread(target=self.run_schedule).start()  # Chạy lịch trình trong luồng riêng

    def send_notification(self):
        notification.notify(
            title="Thông báo",
            message="Đến lúc học tiếng Anh rồi!",
            app_name="English Learning App",
            timeout=10  # Thời gian hiển thị thông báo
        )

    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)  # Chờ 1 giây trước khi kiểm tra lại

    def delete_word(self):
        if not self.app.current_user:
            messagebox.showwarning("Cảnh báo", "Bạn cần đăng nhập để xóa từ!")
            return
        
        selected_word = self.listbox.get(tk.ACTIVE)
        if selected_word:
            english_word = selected_word.split(":")[0].strip()
            self.db.delete_word(self.app.current_user['username'], english_word)
            self.display_words()
            messagebox.showinfo("Xóa thành công", f"Đã xóa: {english_word}")


    def read_word(self):
        selected_word = self.listbox.get(tk.ACTIVE)
        if selected_word:
            english_word = selected_word.split(":")[0].strip()
            self.engine.say(english_word)  # Đọc từ tiếng Anh
            self.engine.runAndWait()  # Chờ cho đến khi việc đọc hoàn tất

    def display_words(self):
        words = self.db.get_all_words(self.app.current_user['username'])  # Lấy từ của người dùng hiện tại
        self.listbox.delete(0, tk.END)
        for word in words:
            self.listbox.insert(tk.END, f"{word['english']} : {word['vietnamese']}")