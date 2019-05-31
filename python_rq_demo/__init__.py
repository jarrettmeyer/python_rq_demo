"""Initialize the python_rq_demo module."""

import logging

# Define the logger before continuing with the rest of the module.
logging.basicConfig(level=logging.DEBUG)
logger: logging.Logger = logging.getLogger('python_rq_demo')

import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import (DEBUG, SECRET_KEY, SESSION_COOKIE_NAME,
                     SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS)
from .util import mask


def create_app() -> Flask:
    """Create a new Flask application instance."""
    app = Flask(__name__)
    app.debug = DEBUG
    app.secret_key = SECRET_KEY
    app.session_cookie_name = SESSION_COOKIE_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    CORS(app)
    return app


# Create the app, db, and migration instances.
app = create_app()
db: SQLAlchemy = SQLAlchemy(app)
migrate: Migrate = Migrate(app, db)


ENV_BLACKLIST = [
    'GPG_KEY',
    'HTTP_PROXY',
    'HTTPS_PROXY',
    'LANG',
    'PATH',
    'POSTGRES_PASSWORD',
    'SQLALCHEMY_DATABASE_URI',
    'http_proxy',
    'https_proxy'
]


def print_environment_variables():
    logger.debug('---------- env ----------')
    for var in os.environ:
        if var not in ENV_BLACKLIST:
            logger.debug('%s: %s', var, os.environ.get(var))
        else:
            logger.debug('%s: %s', var, mask(os.environ.get(var)))


# These need to be imported *AFTER* the app has been initialized.
from . import api, models, routes
