import logging
from flask_jsonpify import jsonify
from rq.job import Job, NoSuchJobError
from .. import app
from ..config import redis_connection
from ..models import Task
from . import logger


@app.route('/api/job_status/<id>')
def api_job_status(id):
    try:
        job: Job = Job.fetch(id, connection=redis_connection())
        Task.update(job)
        return jsonify({
            'id': job.id,
            'status': job.get_status(),
            'duration': float(_get_result(job, 'duration') or 0),
            'title': _get_result(job, 'title'),
            'message': _get_result(job, 'message'),
        })
    except NoSuchJobError:
        return jsonify({
            'id': id,
            'status': 'no_such_job'
        })


def _get_result(job: Job, key: str) -> str:
    try:
        return job.result.get(key)
    except AttributeError:
        logger.warning('Job %s result does not have a %s attribute.', job.id, key)
        return None
