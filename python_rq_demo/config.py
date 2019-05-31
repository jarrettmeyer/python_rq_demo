"""Configure the application. Most values are pulled from system
environment variables, with sane defaults."""

import os

# Default values.
_DEFAULT_COOKIE_NAME = 'python_rq_demo'
_DEFAULT_DB_URI = 'postgresql://postgres:postgres@localhost:5432/python_rq_demo'
_DEFAULT_REDIS_URI = 'redis://localhost:6379'
_DEFAULT_SECRET_KEY = 'yuk5CIDchKtV5sk38Dygb11083hx2wtofbIpyJFIgMpJ5Z2O3K2ToTL79veNgyfr'

# Configuration values set from environment variables.
DEBUG: bool = (os.environ.get('DEBUG') or '1') == '1'
REDIS_URI: str = os.environ.get('REDIS_URI') or _DEFAULT_REDIS_URI
SQLALCHEMY_DATABASE_URI: str = os.environ.get('SQLALCHEMY_DATABASE_URI') or _DEFAULT_DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS: bool = (os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or '1') == '1'
SECRET_KEY: str = os.environ.get('SECRET_KEY') or _DEFAULT_SECRET_KEY
SESSION_COOKIE_NAME: str = os.environ.get('SESSION_COOKIE_NAME') or _DEFAULT_COOKIE_NAME
SYNC_INTERVAL: int = int(os.environ.get('SYNC_INTERVAL') or '15000')
