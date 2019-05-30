from flask_jsonpify import jsonify
from redis import Redis
from rq import Queue
from rq.job import Job
from rq.registry import DeferredJobRegistry, FailedJobRegistry, FinishedJobRegistry, StartedJobRegistry
from typing import List
from .. import app
from ..tasks import redis_connection, rq_queue


@app.route('/api/jobs')
def api_get_jobs():
    connection = redis_connection()

    job_ids = []
    queue_job_ids: List[str] = rq_queue().get_job_ids()
    deferred_job_ids = DeferredJobRegistry('default', connection=connection).get_job_ids()
    failed_job_ids = FailedJobRegistry('default', connection=connection).get_job_ids()
    finished_job_ids = FinishedJobRegistry('default', connection=connection).get_job_ids()
    started_job_ids = StartedJobRegistry('default', connection=connection).get_job_ids()

    add_if_unique(job_ids, queue_job_ids)
    add_if_unique(job_ids, deferred_job_ids)
    add_if_unique(job_ids, failed_job_ids)
    add_if_unique(job_ids, finished_job_ids)
    add_if_unique(job_ids, started_job_ids)

    return jsonify({
        'job_ids': job_ids
    })


def add_if_unique(target, source):
    for item in source:
        if item not in target:
            target.append(item)
    return target
