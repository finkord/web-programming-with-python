from flask import Blueprint

friends_bp = Blueprint(
    "friends", 
    __name__, 
    url_prefix="/friends",
    static_folder="static",
    static_url_path="/friends/static",
    template_folder="templates/friends"
)

from . import views