from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config_map
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
import os

from flask import render_template

import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
load_dotenv()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name: str = os.environ.get("FLASK_CONFIG", "dev")) -> Flask:

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    print(f"Running in config: {config_name}")

    db.init_app(app)
    migrate.init_app(app, db)

    # --- START LOGGING CONFIGURATION ---
    if not os.path.exists('logs'):
        os.mkdir('logs')

        # Create a Rotating File Handler
        # 'logs/app.log' - file path
        # maxBytes=10240 - maximum size of the file (10KB)
        # backupCount=10 - number of backup files
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10, encoding='utf-8')

        # Set the formatter for the logs
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))

        # Set the logging level for the handler
        file_handler.setLevel(logging.INFO)

        # Add the handler to the application's logger
        app.logger.addHandler(file_handler)

        # Set the general logging level for the application
        app.logger.setLevel(logging.INFO)
        # app.logger.info('Flask app startup')
    # --- END LOGGING CONFIGURATION ---

    with app.app_context(): 
        # Register main/general blueprint
        from .views import main as main_blueprint
        app.register_blueprint(main_blueprint)
    
        # Import and register the 'users' Blueprint
        from .users import views as user_views
        app.register_blueprint(user_views.users_bp)

        # Import and register the 'posts' Blueprint
        from .posts import post_bp as posts_blueprint
        app.register_blueprint(posts_blueprint)

        from .posts import models

        # Print routes only when testing
        if config_name == "test":
            print("Registered routes:")
            for rule in app.url_map.iter_rules():
                print(rule)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
     
    return app

