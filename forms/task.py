import datetime

import tzlocal
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField,widgets, SubmitField, IntegerField, DateTimeField, SelectField,BooleanField,RadioField, SelectMultipleField
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def pre_validate(self, form):
        """per_validation is disabled"""

class TaskForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание')
    type = SelectField("Тип мероприятия", validators=[DataRequired()],choices=[],validate_choice=False)
    country = SelectField("Страна проведения", validators=[DataRequired()], choices=[],validate_choice=False)
    friend_invited = MultiCheckboxField('Друзья/Участники:',choices=[], validate_choice=False)
    address = StringField('Адрес мероприятия', validators=[DataRequired()])
    date = DateTimeField(f"Дата проведения(МСК)", validators=[DataRequired()],format='%Y-%m-%dT%H:%M')
    is_private = BooleanField("Приватное мероприятие?")
    is_address_displayed = BooleanField("Добавить отображение адреса на карте?")
    submit = SubmitField('Сохранить')