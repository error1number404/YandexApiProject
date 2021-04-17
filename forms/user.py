from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField, DateField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    country_from = SelectField("Страна проживания", validators=[DataRequired()], choices=[])
    city_from = StringField("Город проживания", validators=[DataRequired()])
    date_of_birth = DateField("Дата рождения", validators=[DataRequired()],format='%Y-%m-%d')
    submit = SubmitField('Зарегистрироваться')