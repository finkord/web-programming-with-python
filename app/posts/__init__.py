from flask import Blueprint

post_bp = Blueprint("posts", 
                    __name__, 
                    url_prefix="/post",
                    static_folder="static",
                    static_url_path="/posts/static",
                    template_folder="templates/posts"
                    )

from . import views