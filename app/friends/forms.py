from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired, Length, Email, Optional
from .models import FriendGroup

class FriendForm(FlaskForm):
    first_name = StringField("Ім'я", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Прізвище", validators=[DataRequired(), Length(max=50)])
    phone = StringField("Телефон", validators=[Optional(), Length(max=20)])
    email = EmailField("Email", validators=[Optional(), Email(), Length(max=120)])
    
    # Вибір групи (Select)
    group_id = SelectField("Група", coerce=int, validators=[DataRequired()])
    
    submit = SubmitField("Зберегти")

class SearchForm(FlaskForm):
    query = StringField("Пошук за прізвищем", validators=[Optional()])
    submit = SubmitField("Шукати")

class GroupForm(FlaskForm):
    name = StringField("Назва групи", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Створити групу")

    def validate_name(self, name):
        # Перевірка на унікальність
        group = FriendGroup.query.filter_by(name=name.data).first()
        if group:
            raise ValidationError('Така група вже існує. Оберіть іншу назву.')