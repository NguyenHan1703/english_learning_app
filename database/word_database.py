from pymongo import MongoClient

class WordDatabase:
    def __init__(self):
        # Kết nối tới cơ sở dữ liệu MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['english_learning_app']  # Tên cơ sở dữ liệu
        self.collection = self.db['words']  # Tên collection cho từ vựng

    def add_word(self, username, english_word, vietnamese_meaning):
        """Thêm từ vựng cho người dùng."""
        self.collection.insert_one({
            'username': username,
            'english': english_word,
            'vietnamese': vietnamese_meaning
        })

    def get_all_words(self, username):
        """Lấy danh sách tất cả từ vựng của người dùng."""
        return list(self.collection.find({'username': username}))

    def delete_word(self, username, english_word):
        """Xóa từ vựng của người dùng."""
        result = self.collection.delete_one({
            'username': username,
            'english': english_word
        })
        return result.deleted_count > 0

    def update_word(self, username, english_word, new_vietnamese_meaning):
        """Cập nhật nghĩa của từ vựng."""
        result = self.collection.update_one(
            {'username': username, 'english': english_word},
            {'$set': {'vietnamese': new_vietnamese_meaning}}
        )
        return result.modified_count > 0

    def word_exists(self, username, english_word):
        """Kiểm tra xem từ vựng đã tồn tại hay chưa."""
        return self.collection.find_one({'username': username, 'english': english_word}) is not None