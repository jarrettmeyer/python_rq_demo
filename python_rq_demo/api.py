import logging

logger: logging.Logger = logging.getLogger('api')

from datetime import datetime
from flask import request
from flask_jsonpify import jsonify
from rq.job import Job, NoSuchJobError
from rq.registry import FailedJobRegistry
from . import app
from .config import SYNC_INTERVAL
from .tasks import (get_all_job_ids, get_job_duration, get_job_result_property,
                    redis_connection, rq_queue, send_message)


@app.route('/api/config')
def api_config():
    now = datetime.now()
    return {
        'now': str(now),
        'timestamp': now.timestamp(),
        'sync_interval': SYNC_INTERVAL
    }


@app.route('/api/delete_failed_jobs', methods=['POST'])
def api_delete_failed_jobs():
    connection = redis_connection()
    r = FailedJobRegistry('default', connection=connection)
    job_ids = r.get_job_ids()
    delete_count = 0
    for job_id in job_ids:
        job = Job.fetch(job_id, connection=connection)
        job.delete()
        delete_count += 1

    return jsonify({
        'count': delete_count
    })


@app.route('/api/jobs')
def api_get_jobs():
    """Get all jobs from Redis."""
    job_ids = get_all_job_ids()
    return jsonify({
        'job_ids': job_ids
    })


@app.route('/api/job_status/<id>')
def api_job_status(id):
    try:
        job: Job = Job.fetch(id, connection=redis_connection())
        return jsonify({
            'id': job.id,
            'created_at': job.created_at.timestamp(),
            'status': job.get_status(),
            'duration': get_job_duration(job),
            'title': get_job_result_property(job, 'title'),
            'message': get_job_result_property(job, 'message'),
        })
    except NoSuchJobError:
        return jsonify({
            'id': id,
            'created_at': -1,
            'status': 'no_such_job',
            'duration': -1
        })


@app.route('/api/messages', methods=['POST'])
def api_messages():
    """Creates a new send_message job on the job queue."""
    message = str(request.get_json().get('message') or '')
    sleep_duration = float(request.get_json().get('sleep_duration') or '0.0')
    logger.debug('message: %s, sleep duration: %f', message, sleep_duration)

    q = rq_queue()
    job: Job = q.enqueue(send_message, message=message, sleep_duration=sleep_duration)

    return jsonify({
        'id': job.id,
        'created_at': job.created_at.timestamp(),
        'status': job.get_status(),
    })
