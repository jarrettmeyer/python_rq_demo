from flask import Flask
from .config import (DEBUG, SQLALCHEMY_DATABASE_URI,
                     SQLALCHEMY_TRACK_MODIFICATIONS,
                     SECRET_KEY, SESSION_COOKIE_NAME)


def create_app() -> Flask:
    """Create a new Flask application instance."""
    app = Flask(__name__)
    app.debug = DEBUG
    app.secret_key = SECRET_KEY
    app.session_cookie_name = SESSION_COOKIE_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    return app
