from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя Пользователя', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
    remember_me = BooleanField("Запомнить меня", default=True,
                               render_kw={"class": "form-check-input"})

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Введите пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password_confirmation = PasswordField('Повторите пароль',
                             validators=[DataRequired(), EqualTo('password')],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary"})

    def validate_username (self, username):
        users_count = User.query.filter_by(name=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')

    def validate_email (self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегестрирован')
