from flask import Blueprint

products_bp = Blueprint("products", 
                    __name__, 
                    url_prefix="/products",
                    static_folder="static",
                    static_url_path="/posts/static",
                    template_folder="templates/posts"
                    )

from . import views