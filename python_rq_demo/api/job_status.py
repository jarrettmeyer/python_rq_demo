import pytz
from datetime import datetime, timedelta
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
            'created_at': job.created_at.timestamp(),
            'status': job.get_status(),
            'duration': _get_job_duration(job),
            'title': _get_result(job, 'title'),
            'message': _get_result(job, 'message'),
        })
    except NoSuchJobError:
        return jsonify({
            'id': id,
            'created_at': -1,
            'status': 'no_such_job',
            'duration': -1
        })


def _get_job_duration(job: Job) -> float:
    if job.result is not None and job.result.duration is not None:
        return job.result.duration
    else:
        duration: timedelta = datetime.now().replace(tzinfo=pytz.utc) - job.started_at.replace(tzinfo=pytz.utc)
        return duration.total_seconds()


def _get_result(job: Job, key: str) -> str:
    try:
        return job.result.get(key)
    except AttributeError:
        logger.warning('Job %s result does not have a %s attribute.', job.id, key)
        return None
