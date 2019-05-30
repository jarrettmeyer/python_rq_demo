import logging

logger: logging.Logger = logging.getLogger('tasks')

import json
import pytz
from datetime import datetime, timedelta
from redis import Redis
from rq import Connection, Queue, Worker
from rq.job import Job
from rq.registry import FailedJobRegistry, FinishedJobRegistry
from .. import db
from ..config import REDIS_URI
from ..models import Task
from .send_message import send_message
from .task_result import TaskResult


class CustomJob(Job):

    def set_status(self, status, pipeline=None):
        super().set_status(status, pipeline)
        logger.debug('Job %s status was set to %s.', self.id, status)
        update_task(self, status)


class CustomQueue(Queue):
    job_class = CustomJob

    def enqueue(self, f, *args, **kwargs):
        result = super().enqueue(f, *args, **kwargs)
        if isinstance(result, Job):
            update_task(result)
        return result


class CustomWorker(Worker):
    job_class = CustomJob
    queue_class = CustomQueue


def clean_dictionary(d: dict) -> dict:
    for key in d:
        if hasattr(d[key], '__call__'):
            d.pop(key)
    return d


def get_job_duration(job: Job) -> float:
    if job.created_at is not None and job.ended_at is not None:
        created_at = job.created_at.replace(tzinfo=pytz.utc)
        ended_at = job.ended_at.replace(tzinfo=pytz.utc)
        return (ended_at - created_at).total_seconds()
    else:
        return None


def get_job_result(job: Job) -> str:
    if job.result is None:
        return None
    elif isinstance(job.result, dict):
        d = clean_dictionary(job.result)
        return json.dumps(d)
    elif isinstance(job.result, str):
        return job.result
    else:
        try:
            d = clean_dictionary(job.result.__dict__)
            return json.dumps(d)
        except AttributeError:
            return str(job.result)


def get_job_result_property(job: Job, prop: str, default: str=None) -> str:
    if job.result is None:
        return default
    if isinstance(job.result, dict):
        return job.result.get(prop) or default
    else:
        try:
            result_as_dict = job.result.__dict__
            return result_as_dict.get(prop) or default
        except AttributeError:
            return default


def redis_connection() -> Redis:
    return Redis.from_url(REDIS_URI)


def rq_connection() -> Connection:
    return Connection(redis_connection())


def rq_failed_job_registry() -> FailedJobRegistry:
    return FailedJobRegistry('default', redis_connection())


def rq_finished_job_registry() -> FinishedJobRegistry:
    return FinishedJobRegistry('default', redis_connection())


def rq_queue() -> Queue:
    return CustomQueue('default', connection=redis_connection())


def rq_worker() -> Worker:
    return CustomWorker('default')


def update_task(job: Job, status: str=None) -> Task:
    task: Task = Task.query.get(job.id)
    if task is None:
        task = Task()
        task.id = job.id
        db.session.add(task)

    # Update the task properties.
    task.created_at = job.created_at
    task.duration = get_job_duration(job)
    task.ended_at = job.ended_at
    task.enqueued_at = job.enqueued_at
    task.failure_ttl = job.failure_ttl
    task.func_name = job.func_name
    task.result = get_job_result(job)
    task.result_ttl = job.result_ttl
    task.started_at = job.started_at
    task.status = status or job.get_status()
    task.timeout = job.timeout
    task.ttl = job.ttl
    task.title = get_job_result_property(job, 'title')
    task.message = get_job_result_property(job, 'message')

    # Persist any changes to the DB.
    db.session.commit()
    return task
