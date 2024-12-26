import tkinter as tk
from tkinter import messagebox
from logic.translation_logic import translate_word
from database.word_database import WordDatabase
import pyttsx3  # Nhập thư viện pyttsx3

class TranslationScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.db = WordDatabase()
        self.engine = pyttsx3.init()  # Khởi tạo engine pyttsx3
        
        # Lấy danh sách các giọng nói có sẵn
        voices = self.engine.getProperty('voices')
        
        # Chọn giọng nói bạn muốn sử dụng (thay đổi chỉ số theo ý muốn)
        self.engine.setProperty('voice', voices[1].id)  # Chọn giọng đọc đầu tiên (thay đổi chỉ số tùy theo giọng bạn muốn)

        # Thay đổi tốc độ đọc
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate * 0.8)  # Giảm tốc độ đọc 10%

        self.frame = tk.Frame(self.root, bg="#f5f5f5")  # Màu nền nhẹ cho toàn bộ frame

        # Chia đôi màn hình với màu nền nhẹ
        self.left_frame = tk.Frame(self.frame, bg="#e0f7fa")  # Màu nền nhẹ cho phần bên trái
        self.right_frame = tk.Frame(self.frame, bg="#ffe0b2")  # Màu nền nhẹ cho phần bên phải

        # Các widget cho phần bên trái (Nhập từ tiếng Anh)
        self.label_english = tk.Label(self.left_frame, text="English", font=("Arial", 14), bg="#e0f7fa", fg="#004d40")  # Màu chữ nhẹ nhàng
        self.entry_english = tk.Text(self.left_frame, font=("Arial", 16), width=30, height=5)

        # Nút đọc từ
        self.button_read = tk.Button(self.left_frame, text="Đọc từ", font=("Arial", 12), command=self.read_word, bg="#b2ebf2", fg="#004d40")

        self.button_translate = tk.Button(self.right_frame, text="Dịch", font=("Arial", 12), command=self.translate, bg="#ffccbc", fg="#004d40")
        self.button_save = tk.Button(self.right_frame, text="Lưu từ", font=("Arial", 12), command=self.save_word, bg="#ffccbc", fg="#004d40")

        # Các widget cho phần bên phải (Hiển thị nghĩa tiếng Việt)
        self.label_vietnamese = tk.Label(self.right_frame, text="Tiếng Việt", font=("Arial", 14), bg="#ffe0b2", fg="#bf360c")  # Màu chữ nhẹ nhàng
        self.entry_vietnamese = tk.Text(self.right_frame, font=("Arial", 16), width=30, height=5)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Hiển thị các phần của giao diện
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)  # Thêm khoảng cách
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)  # Thêm khoảng cách

        # Bên trái
        self.label_english.pack(pady=10)
        self.entry_english.pack(pady=10)
        self.button_read.pack(pady=10)  # Thêm nút đọc từ

        # Bên phải
        self.label_vietnamese.pack(pady=10)
        self.entry_vietnamese.pack(pady=10)
        self.button_translate.pack(padx=5, pady=10)
        self.button_save.pack(padx=5, pady=10)

    def translate(self):
        word = self.entry_english.get("1.0", tk.END).strip()  # Lấy nội dung từ Text widget
        translated_word = translate_word(word)
        self.entry_vietnamese.delete("1.0", tk.END)  # Xóa nội dung Text widget
        self.entry_vietnamese.insert("1.0 ", translated_word)  # Chèn từ đã dịch vào Text widget

    def read_word(self):
        word = self.entry_english.get("1.0", tk.END).strip()  # Lấy từ cần đọc
        if word:
            self.engine.say(word)  # Đọc từ
            self.engine.runAndWait()  # Chờ cho đến khi hoàn thành

    def save_word(self):
        english_word = self.entry_english.get("1.0", tk.END).strip()  # Lấy nội dung từ Text widget
        vietnamese_meaning = self.entry_vietnamese.get("1.0", tk.END).strip()  # Lấy nội dung từ Text widget
        if english_word and vietnamese_meaning:
            self.db.add_word(self.app.current_user['username'], english_word, vietnamese_meaning)  # Thêm username
            tk.messagebox.showinfo("Lưu thành công", f"Đã lưu: {english_word} - {vietnamese_meaning}")
        else:
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ vào")
