from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password=None, cliente=None, cuenta=None):
        self.id = id
        self.username = username
        self.password = password  # Será True/False para indicar si coincidió
        self.cliente = cliente  # Diccionario con datos del cliente
        self.cuenta = cuenta
        
    @property
    def cuenta_principal(self):
        """Returns the first account or None if no accounts exist"""
        return self.cuenta[0] if self.cuenta else None
    
    @classmethod
    def create_password_hash(cls, password):
        return generate_password_hash(password)

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)