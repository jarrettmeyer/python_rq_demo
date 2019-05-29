"""Initialize the python_rq_demo module."""

import logging

# Define the logger before continuing with the rest of the module.
logging.basicConfig(level=logging.DEBUG)
logger: logging.Logger = logging.getLogger('python_rq_demo')

from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .app_factory import create_app
from .print_environment_variables import print_environment_variables


app = create_app()
CORS(app)
db: SQLAlchemy = SQLAlchemy(app)
migrate: Migrate = Migrate(app, db)

# These need to be imported *AFTER* the app has been initialized.
from . import api, models, routes
