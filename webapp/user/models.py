from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from webapp.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50), unique=True)

    def set_password(self, user_password):
        self.password = generate_password_hash(user_password)

    def check_password(self, hash_password):
        return check_password_hash(self.password, hash_password)

    @property  # Декоратор позволяет вызывать метод как атрибут (без скобочек)
    def is_admin(self):  # Класс сообщает, является ли пользователь администратором
        return self.role == 'admin'

    def __repr__(self):
        return f"USERNAME - {self.name}, ROLE - {self.role}"
