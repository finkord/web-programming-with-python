from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    EmailField,
    StringField,
    PasswordField,  
    BooleanField,  
    SubmitField,
    ValidationError,
    TextAreaField
)
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    Email
)

from app.users.models import User
from flask_login import current_user

import os

class RegistrationForm(FlaskForm):
    username = StringField(
        "Ім'я користувача", # Username
        validators=[DataRequired(), Length(min=4, max=14)]
    )
    
    email = EmailField(
        "Електронна пошта", # Email
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    
    password = PasswordField(
        "Пароль", # Password
        validators=[DataRequired(), Length(min=6)]
    )
    
    confirm_password = PasswordField(
        "Підтвердження паролю", # Confirm Password
        validators=[DataRequired(), EqualTo('password', message="Паролі мають співпадати")]
    )
    
    submit = SubmitField("Зареєструватися")

    def validate_username(self, username):
        """Перевіряє, чи не існує вже користувач з таким іменем."""
        # Query the database to find a user with the entered username
        user = User.query.filter_by(username=username.data).first()
        if user:
            # If a user is found, raise a validation error
            raise ValidationError('Це ім\'я користувача вже зайняте. Виберіть інше.')
            
    def validate_email(self, email):
        """Перевіряє, чи не існує вже користувач з такою електронною поштою."""
        # Query the database to find a user with the entered email
        user = User.query.filter_by(email=email.data).first()
        if user:
            # If a user is found, raise a validation error
            raise ValidationError('Ця електронна пошта вже зареєстрована.')

class LoginForm(FlaskForm):
    """
    Form for user login (authentication).
    """

    # username/email - Required field
    # Using StringField as it can handle either email or username input
    username = StringField(
        "Ім'я користувача",
        validators=[
            DataRequired(message="Будь ла ласка, введіть логін або email.")
        ]
    )

    # password - Required, min=4, max=10 characters
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Будь ласка, введіть пароль."),
            Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів.")
        ]
    )

    # remember - BooleanField for persistence
    remember = BooleanField("Запам'ятати мене")

    submit = SubmitField("Увійти")

class UpdateAccountForm(FlaskForm):
    """Форма оновлення даних користувача"""
    username = StringField(
        "Ім'я користувача",
        validators=[DataRequired(), Length(min=4, max=14)]
    )
    
    email = EmailField(
        "Електронна пошта",
        validators=[DataRequired(), Email(), Length(max=120)]
    )

    picture = FileField(
        'Оновити фото профілю', 
        validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Тільки зображення!')]
    )

    about_me = TextAreaField(
        "Про мене", 
        validators=[Length(min=0, max=140)]
    )
    
    submit = SubmitField("Оновити")

    def validate_username(self, username):
        """Перевірка унікальності імені (ігноруючи поточне ім'я користувача)"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Це ім\'я користувача вже зайняте.')

    def validate_email(self, email):
        """Перевірка унікальності пошти (ігноруючи поточну пошту користувача)"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ця електронна пошта вже використовується.')

    def validate_picture(self, picture):
            """Перевірка розміру файлу (не більше 5 МБ)"""
            if picture.data:
                picture.data.seek(0, os.SEEK_END)
                file_size = picture.data.tell()
                picture.data.seek(0)
                
                if file_size > 5 * 1024 * 1024: # 5 МБ в байтах
                    raise ValidationError('Файл занадто великий. Максимальний розмір - 5MB.')