from getpass import getpass
import sys

from webapp import create_app
from webapp.model import db, User

app = create_app()

with app.app_context():
    username = input("Введите имя пользователя: ")

    if User.query.filter(User.name == username).count():
        print("Такой пользователь уже есть")
        sys.exit(0)

    password = getpass("Введите пароль:")
    password_confirmation = getpass("Повторите пароль для подтверждения: ")

    if password != password_confirmation:
        print("Пароли не совпадают")
        sys.exit(0)

    new_admin = User(name=username, role="admin")
    new_admin.set_password(password)

    db.session.add(new_admin)
    db.session.commit()
    print(f"Идентификатор нового администратора - #{new_admin.id}")