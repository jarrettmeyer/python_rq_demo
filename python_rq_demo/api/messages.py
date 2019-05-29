import logging
from flask import request
from flask_jsonpify import jsonify
from rq.job import Job
from .. import app
from ..config import rq_queue
from ..tasks import send_message


logger: logging.Logger = logging.getLogger('api_messages')


@app.route('/api/messages', methods=['POST'])
def api_messages():

    message = str(request.get_json().get('message') or '')
    sleep_duration = float(request.get_json().get('sleep_duration') or '0.0')
    logger.debug('message: %s, sleep duration: %f', message, sleep_duration)

    q = rq_queue()
    job: Job = q.enqueue(send_message, message=message, sleep_duration=sleep_duration)

    return jsonify({
        'id': job.id,
        'status': job.get_status()
    })


