from flask import Flask, flash, render_template, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from webapp.forms import LoginForm
from webapp.model import db, News, User
from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        page_title = "Новости Python"
        weather_data = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', title=page_title, weather=weather_data, news=news_list)

    @app.route("/login")  # Авторизация пользователя и переадресация на заглавную страницу
    def login():
        if current_user.is_authenticated:  # Проверка на авторизацию
            return redirect(url_for('index'))
        page_title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', title=page_title, form=login_form)

    @app.route("/process-login", methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():  # Валидация формы на предмет ошибок
            user = User.query.filter_by(name=form.username.data).first()
            if user and user.check_password(form.password.data): # Проверка существования пользователя и верности введенного пароля
                login_user(user)  # Логин пользователя
                flash("Вы вошли на сайт")
                return redirect(url_for('index'))  # Переадресация на главную страницу

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))  # Переадресация на повторную авторизацию в случае несовпадения данных с данными в бд

    @app.route('/admin')
    @login_required
    def admin_index():  # Страница с доступом только для зарегестрированных (пока что есть только роль админа)
        if current_user.is_admin:
            return 'Привет Админ'
        else:
            return 'Ты не Админ!'

    @app.route('/logout')
    def logout():  # Выход из учетной записи и переадресация на заглавную страницу
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    return app
