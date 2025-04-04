from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, username, password=None):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def create_password_hash(cls, password):
        return generate_password_hash(password)

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)