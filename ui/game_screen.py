import tkinter as tk
from database.word_database import WordDatabase
import random
from tkinter import messagebox
import re

class GameScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.db = WordDatabase()
        self.frame = tk.Frame(self.root, bg="#e0f7fa")  # Màu nền nhẹ cho toàn bộ frame

        # Tạo các widget
        self.label_question = tk.Label(self.frame, text="Bắt đầu ôn tập từ vựng!", font=("Arial", 16), bg="#f5f5f5", fg="#000000")
        self.entry_answer = tk.Entry(self.frame, font=("Arial", 14), width=30, bg="#ffffff", fg="#000000")
        self.button_check = tk.Button(self.frame, text="Kiểm tra", command=self.check_answer, font=("Arial", 12), bg="#b2ebf2", fg="#000000")
        self.button_start = tk.Button(self.frame, text="Bắt đầu ôn tập", command=self.start_game, font=("Arial", 12), bg="#ffccbc", fg="#000000")
        self.label_result = tk.Label(self.frame, text="", font=("Arial", 14), bg="#f5f5f5", fg="#000000")

        # Biến lưu trữ từ vựng hiện tại
        self.current_word = None
        self.current_meaning = None

        self.words = []  # Danh sách các từ đã random
        self.current_index = 0  # Chỉ số của từ hiện tại

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Sắp xếp các widget
        self.label_question.grid(row=0, column=0, padx=10, pady=10)
        self.entry_answer.grid(row=1, column=0, padx=10, pady=10)
        self.button_check.grid(row=2, column=0, padx=10, pady=10)
        self.button_start.grid(row=3, column=0, padx=10, pady=10)
        self.label_result.grid(row=4, column=0, padx=10, pady=10)

    def start_game(self):
        if not self.app.current_user:
            messagebox.showwarning("Cảnh báo", "Bạn cần đăng nhập để chơi trò chơi!")
            return

        self.words = self.db.get_all_words(self.app.current_user['username'])  # Lấy tất cả các từ của người dùng
        if self.words:
            random.shuffle(self.words)  # Random danh sách từ
            self.current_index = 0  # Đặt lại chỉ số về 0
            self.ask_question()  # Gọi hàm để hỏi câu hỏi đầu tiên
        else:
            self.label_question.config(text="Chưa có từ nào trong cơ sở dữ liệu!")

    def ask_question(self):
        if self.current_index < len(self.words):
            random_word = self.words[self.current_index]
            self.current_word = random_word['english']
            self.current_meaning = random_word['vietnamese']
            self.label_question.config(text=f"Nghĩa của từ '{self.current_word}' là gì?")
        else:
            self.label_question.config(text="Bạn đã trả lời tất cả các từ!")

    def check_answer(self):
        user_answer = self.entry_answer.get().strip().lower()
        
        meanings = re.split(r'[;,]', self.current_meaning.lower())  # Phân tách bằng dấu ',' hoặc ';'
        meanings = [meaning.strip() for meaning in meanings]  # Xóa khoảng trắng ở đầu và cuối mỗi nghĩa

        if user_answer in meanings:
            self.label_result.config(text="Chúc mừng! Bạn đã trả lời đúng.", fg='green')
            self.current_index += 1  # Tăng chỉ số lên để hỏi từ tiếp theo
            self.entry_answer.delete(0, tk.END)  # Xóa câu trả lời
            self.ask_question()  # Hỏi câu hỏi tiếp theo
        else:
            self.label_result.config(
                text=f"Sai rồi! Nghĩa đúng của '{self.current_word}' là '{self.current_meaning}'.", fg='red')

        # Xóa câu trả lời
        self.entry_answer.delete(0, tk.END)