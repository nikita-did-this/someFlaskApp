from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user

from webapp.user.forms import LoginForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route("/login")  # Авторизация пользователя и переадресация на заглавную страницу
def login():
    if current_user.is_authenticated:  # Проверка на авторизацию
        return redirect(url_for('news.index'))
    page_title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', title=page_title, form=login_form)

@blueprint.route("/process-user", methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():  # Валидация формы на предмет ошибок
        user = User.query.filter_by(name=form.username.data).first()
        if user and user.check_password(form.password.data):  # Проверка существования пользователя и верности введенного пароля,
            login_user(user,remember=form.remember_me.data)  # Логин пользователя, проверка функционала запоминнания в куках
            flash("Вы вошли на сайт")
            return redirect(url_for('news.index'))  # Переадресация на главную страницу

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('user.login'))  # Переадресация на повторную авторизацию в случае несовпадения данных с данными в бд

@blueprint.route('/logout')
def logout():  # Выход из учетной записи и переадресация на заглавную страницу
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('user.login'))