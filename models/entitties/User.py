from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password=None, cliente=None):
        self.id = id
        self.username = username
        self.password = password  # Será True/False para indicar si coincidió
        self.cliente = cliente  # Diccionario con datos del cliente
    @classmethod
    def create_password_hash(cls, password):
        return generate_password_hash(password)

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)