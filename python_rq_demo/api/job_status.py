import pytz
from datetime import datetime, timedelta
from flask_jsonpify import jsonify
from rq.job import Job, NoSuchJobError
from .. import app
from ..models import Task
from ..tasks import get_job_duration, get_job_result_property, redis_connection
from . import logger


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
