from pymongo import MongoClient

class UserDatabase:
    def __init__(self):
        # Kết nối tới cơ sở dữ liệu MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['english_learning_app']  # Tên cơ sở dữ liệu
        self.collection = self.db['users']  # Tên collection cho người dùng

    def add_user(self, username, password):
        """Thêm người dùng mới vào cơ sở dữ liệu."""
        if not self.collection.find_one({'username': username}):
            self.collection.insert_one({'username': username, 'password': password})
            return True
        return False

    def get_user(self, username):
        """Lấy thông tin người dùng từ cơ sở dữ liệu."""
        return self.collection.find_one({'username': username})

    def delete_user(self, username):
        """Xóa người dùng khỏi cơ sở dữ liệu."""
        result = self.collection.delete_one({'username': username})
        return result.deleted_count > 0

    def update_user_password(self, username, new_password):
        """Cập nhật mật khẩu của người dùng."""
        result = self.collection.update_one(
            {'username': username},
            {'$set': {'password': new_password}}
        )
        return result.modified_count > 0

    def user_exists(self, username):
        """Kiểm tra xem người dùng đã tồn tại hay chưa."""
        return self.collection.find_one({'username': username}) is not None

    def get_all_users(self):
        """Lấy danh sách tất cả người dùng."""
        return list(self.collection.find())
        
    def __del__(self):
        self.client.close()