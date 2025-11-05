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

class PostForm(FlaskForm):
    submit = SubmitField("Створити пост")