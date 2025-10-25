from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
# Load configuration from a separate file
app.config.from_pyfile("../config.py")

# --- START LOGGING CONFIGURATION ---
# Configure logging unless running in debug mode (currently forced 'True')
# if not app.debug:
if True:
    # Create the 'logs' directory if it doesn't exist
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

# Import and register general views
from . import views

# Import and register the 'users' Blueprint
from .users import views
app.register_blueprint(views.users_bp)

# Import and register the 'posts' Blueprint
from .posts import post_bp
app.register_blueprint(post_bp)