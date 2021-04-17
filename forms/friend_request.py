from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class FriendRequestForm(FlaskForm):
    name = StringField('Имя Фамилия', validators=[DataRequired()])
    submit = SubmitField('Поиск')
