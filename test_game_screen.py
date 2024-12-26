import unittest
import time
import tkinter as tk
from main import EnglishLearningApp  # Giả sử bạn đã định nghĩa lớp này trong main.py
from database.word_database import WordDatabase  # Thêm import cho WordDatabase
from pymongo import MongoClient
import random

class TestEnglishLearningApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Kết nối MongoDB
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['english_learning_app']
        
        # Tạo ứng dụng Tkinter
        cls.root = tk.Tk()
        cls.app = EnglishLearningApp(cls.root)
        cls.root.update()  # Cập nhật giao diện

        # Khởi tạo WordDatabase
        cls.word_db = WordDatabase()  # Khởi tạo cơ sở dữ liệu từ vựng

        # Đặt tên người dùng test_user
        cls.test_user = "test_user"

    def setUp(self):
        # In ra tên testcase đang chạy
        print(f"\nRunning test: {self._testMethodName}")

    def test_login_and_navigate_to_game(self):
        """Kiểm tra đăng nhập và chuyển đến màn hình trò chơi."""
        username = self.test_user
        password = "123456789"  # Mật khẩu đã biết

        entry_username = self.app.login_screen.entry_username
        entry_password = self.app.login_screen.entry_password
        button_login = self.app.login_screen.button_login

        entry_username.insert(0, username)
        entry_password.insert(0, password)

        button_login.invoke()  # Gọi hàm đăng nhập

        time.sleep(1)
        self.root.update()  # Cập nhật giao diện

        self.assertIsNotNone(self.app.current_user, "User  should be logged in after successful login.")

        # Chuyển đến màn hình trò chơi
        self.app.show_game_screen()  
        time.sleep(1)
        self.root.update()  # Cập nhật giao diện

        self.assertTrue(self.app.game_screen.frame.winfo_exists(), "Game screen frame should exist after navigating.")
        print("Test 'test_login_and_navigate_to_game' passed.")

    def test_correct_answer(self):
        """Kiểm tra trường hợp trả lời đúng."""
        # Đăng nhập trước khi bắt đầu trò chơi
        self.test_login_and_navigate_to_game()

        self.app.game_screen.start_game()  # Bắt đầu trò chơi

        # Lấy từ vựng đầu tiên từ cơ sở dữ liệu
        words = self.word_db.get_all_words(self.test_user)
        if words:
            random_word = random.choice(words)  # Chọn ngẫu nhiên một từ
            self.app.game_screen.current_word = random_word['english']
            self.app.game_screen.current_meaning = random_word['vietnamese']

            self.app.game_screen.entry_answer.insert(0, random_word['vietnamese'])  # Nhập câu trả lời đúng
            self.app.game_screen.check_answer()  # Kiểm tra câu trả lời

            # Kiểm tra xem thông báo kết quả có đúng không
            result_text = self.app.game_screen.label_result.cget("text")
            self.assertIn("Chúc mừng! Bạn đã trả lời đúng.", result_text)
            time.sleep(5)
            print("Test 'test_correct_answer' passed.")

    def test_incorrect_answer(self):
        """Kiểm tra trường hợp trả lời sai với 3 đáp án sai."""
        # Đăng nhập trước khi bắt đầu trò chơi
        self.test_login_and_navigate_to_game()
        self.app.game_screen.start_game()  # Bắt đầu trò chơi

        # Lấy từ vựng đầu tiên từ cơ sở dữ liệu
        words = self.word_db.get_all_words(self.test_user)
        if words:
            random_word = random.choice(words)  # Chọn ngẫu nhiên một từ
            self.app.game_screen.current_word = random_word['english']
            self.app.game_screen.current_meaning = random_word['vietnamese']

            # Tạo 3 đáp án sai
            wrong_answers = [word['vietnamese'] for word in words if word['vietnamese'] != random_word['vietnamese']]
            wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))  # Chọn 3 đáp án sai ngẫu nhiên

            # Nhập một đáp án sai
            self.app.game_screen.entry_answer.insert(0, wrong_answers[0])  # Nhập câu trả lời sai
            self.app.game_screen.check_answer()  # Kiểm tra câu trả lời

            # Kiểm tra xem thông báo kết quả có đúng không
            result_text = self.app.game_screen.label_result.cget("text")
            self.assertIn("Sai rồi!", result_text)
            time.sleep(5)
            print("Test 'test_incorrect_answer' passed.")

    def test_get_all_words(self):
        """Kiểm tra việc lấy tất cả từ vựng của người dùng."""
        # Đăng nhập trước khi kiểm tra từ vựng
        self.test_login_and_navigate_to_game()

        # Lấy tất cả từ vựng của test_user
        words = self.word_db.get_all_words(self.test_user)

        # Kiểm tra xem danh sách từ vựng có tồn tại và không rỗng
        self.assertIsNotNone(words, "Danh sách từ vựng không được None.")
        self.assertGreater(len(words), 0, "Danh sách từ vựng không được rỗng.")

        # In ra tất cả từ vựng
        print("Từ vựng của test_user:")
        for word in words:
            print(f"{word['english']} : {word['vietnamese']}")
        print("Test 'test_get_all_words' passed.")

if __name__ == "__main__":
    unittest.main()