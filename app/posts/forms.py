from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    SelectField,
    BooleanField,
    DateTimeLocalField  
)
from wtforms.validators import (
    DataRequired, 
    Length
)
from datetime import datetime
from .models import PostCategory  

class PostForm(FlaskForm):
    """
    Форма для створення/редагування поста.
    """
    
    # title - StringField, required, max 150 (відповідає моделі)
    title = StringField(
        "Заголовок", 
        validators=[DataRequired(), Length(max=150)]
    )
    
    # content - TextAreaField, required
    content = TextAreaField(
        "Вміст", 
        validators=[DataRequired()]
    )
    
    # is_active (boolean) - відповідає 'enabled' у вашому коментарі
    # та 'is_active' у вашій моделі
    is_active = BooleanField(
        "Активний (відображається на сайті)", 
        default='checked'
    )
    
    # posted (DateTimeLocalField) - відповідає 'publish_date' у вашому коментарі
    # та 'posted' у вашій моделі
    posted = DateTimeLocalField(
        "Дата публікації",
        format='%Y-%m-%dT%H:%M',  # Важливо для HTML5 <input type="datetime-local">
        default=datetime.utcnow,
        validators=[DataRequired()]
    )
    
    # category (SelectField) - 'choices' генеруються з вашого Enum 'PostCategory'
    category = SelectField(
        "Категорія",
        # Динамічно створюємо список (value, label) з Enum
        choices=[(cat.value, cat.name.capitalize()) for cat in PostCategory],
        validators=[DataRequired()]
    )
    
    # submit
    submit = SubmitField("Створити пост")