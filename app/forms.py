from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    SelectField, 
    EmailField
)
from wtforms.validators import (
    DataRequired, 
    Length, 
    Email, 
    Regexp
)

class ContactForm(FlaskForm):
    """
    Форма зворотного зв'язку (контактна форма) 
    з повною валідацією полів.
    """
    
    # Поле "Ім'я"
    name = StringField(
        "Ім'я", 
        validators=[
            DataRequired(message="Це поле обов'язкове."), 
            Length(min=4, max=10, message="Ім'я повинно бути від 4 до 10 символів.")
        ]
    )
    
    # Поле "Email"
    email = EmailField(
        "Email", 
        validators=[
            DataRequired(message="Це поле обов'язкове."), 
            Email(message="Некоректний email-адрес.")
        ]
    )
    
    # Поле "Телефон"
    phone = StringField(
        "Телефон", 
        validators=[
            DataRequired(message="Це поле обов'язкове."), 
            Regexp(
                r'^\+380\d{9}$', 
                message="Телефон має бути у форматі +380xxxxxxxxx"
            )
        ]
    )
    
    # Поле "Тема" (випадаючий список)
    subject = SelectField(
        "Тема", 
        choices=[
            # (value, label)
            ('general', 'Загальне питання'),
            ('support', 'Технічна підтримка'),
            ('billing', 'Питання по оплаті')
        ],
        validators=[DataRequired(message="Будь ласка, оберіть тему.")]
    )
    
    # Поле "Повідомлення"
    message = TextAreaField(
        "Повідомлення", 
        render_kw={"rows": 5, "cols": 40}, 
        validators=[
            DataRequired(message="Це поле обов'язкове."), 
            Length(max=500, message="Повідомлення не може перевищувати 500 символів.")
        ]
    )
    
    # Кнопка відправки
    submit = SubmitField("Надіслати")