from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class GetPictureForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    city_from = StringField("Город проживания", validators=[DataRequired()])
    country_from = SelectField("Страна проживания", validators=[DataRequired()], choices=[],validate_choice=False)
    picture = FileField('Изменить фотографию профиля',
                        validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Сохранить')
