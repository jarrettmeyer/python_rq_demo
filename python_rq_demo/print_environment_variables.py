import logging
import os
import re
from . import logger
from .util import mask

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
