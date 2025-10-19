from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config.py")

from . import views

from .users import views
app.register_blueprint(views.users_bp)

from .posts import post_bp
app.register_blueprint(post_bp)