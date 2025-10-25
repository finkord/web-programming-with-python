from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,  # Required for password field
    BooleanField,  # Required for "Remember me" functionality
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length
)


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
