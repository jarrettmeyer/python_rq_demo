from datetime import datetime
from flask_jsonpify import jsonify
from .. import app
from ..config import SYNC_INTERVAL


def api_config():
    now = datetime.now()
    return {
        'now': str(now),
        'timestamp': now.timestamp(),
        'sync_interval': SYNC_INTERVAL
    }
