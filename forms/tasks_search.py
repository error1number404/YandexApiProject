from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class TasksSearchForm(FlaskForm):
    search_line = StringField('Search...')
    search_item = SelectField("Искать в", validators=[DataRequired()], choices=[(0,'Адрес'),(1,'Название'),(2,'Описание')], validate_choice=False)
    country = SelectField("Страна проведения", validators=[DataRequired()], choices=[(0,"Любая")],validate_choice=False)
    type = SelectField("Тип мероприятия", validators=[DataRequired()], choices=[(0,"Любое")], validate_choice=False)
    submit = SubmitField('Поиск')
