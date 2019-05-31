"""Defines the functions and classes to facilitate working Redis, RQ,
and tasks. Includes utilities for working with jobs, queues, and
registries."""

import logging

logger: logging.Logger = logging.getLogger('tasks')

import json
import pytz
import time
from datetime import datetime, timedelta
from redis import Redis
from rq import Connection, Queue, Worker
from rq.job import Job
from rq.registry import DeferredJobRegistry, FailedJobRegistry, FinishedJobRegistry, StartedJobRegistry
from typing import List
from . import db
from .config import REDIS_URI
from .models import Task
from .util import add_if_unique


QUEUE_NAME = 'default'


class CustomJob(Job):
    """This custom job adds database calls for persisting modifications
    to the job to the database."""

    def save(self, pipeline=None, include_meta=True):
        super().save(pipeline, include_meta)
        logger.debug('Job %s was saved.', self.id)
        save_task(self)

    def save_meta(self):
        super().save_meta()
        logger.debug('Job %s meta was saved.', self.id)
        save_task(self)

    def set_status(self, status, pipeline=None):
        super().set_status(status, pipeline)
        logger.debug('Job %s status was set to %s.', self.id, status)
        save_task(self, status)


class CustomQueue(Queue):
    """This custom queue adds a database call when enqueuing a new job."""
    job_class = CustomJob

    def enqueue(self, f, *args, **kwargs):
        result = super().enqueue(f, *args, **kwargs)
        if isinstance(result, Job):
            save_task(result)
        return result


class CustomWorker(Worker):
    """Our custom worker allows us to use our CustomQueue and
    CustomJob classes."""
    job_class = CustomJob
    queue_class = CustomQueue


class TaskResult:
    """Utility class for holding a job result."""
    body: dict = {}
    duration: float = None
    message: str = None
    title: str = None

    def get(self, key: str):
        return self.__dict__.get(key)

    def __init__(self, title=None, message=None, duration=None, **kwargs):
        self.title = title
        self.message = message
        self.duration = duration
        for key in kwargs:
            self.body[key] = kwargs.get(key, None)

    def __repr__(self):
        return '<TaskResult title: {0}>'.format(self.title)


def clean_dictionary(d: dict) -> dict:
    """Remove all callable keys from a dictionary. Callables (e.g. functions,
    methods, etc.) cannot be serialized."""
    for key in d:
        if hasattr(d[key], '__call__'):
            d.pop(key)
    return d


def get_all_job_ids() -> List[Job]:
    """Get all jobs IDs from the queue and various rq registries."""
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

    return job_ids


def get_job_duration(job: Job) -> float:
    """Get the job duration, as defined by the difference between
    the job create time and job end time. If the job does not have
    an end time, then `datetime.now()` is used instead."""
    if job.created_at is not None and job.ended_at is not None:
        created_at = job.created_at.replace(tzinfo=pytz.utc)
        ended_at = job.ended_at.replace(tzinfo=pytz.utc)
        return (ended_at - created_at).total_seconds()
    elif job.created_at is not None:
        created_at = job.created_at.replace(tzinfo=pytz.utc)
        now = datetime.now().replace(tzinfo=pytz.utc)
        return (now - created_at).total_seconds()
    else:
        return None


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


def job_result_to_string(job: Job) -> str:
    """Converts the job result to a string."""
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


def redis_connection() -> Redis:
    return Redis.from_url(REDIS_URI)


def rq_connection() -> Connection:
    return Connection(redis_connection())


def rq_failed_job_registry() -> FailedJobRegistry:
    return FailedJobRegistry(QUEUE_NAME, redis_connection())


def rq_finished_job_registry() -> FinishedJobRegistry:
    return FinishedJobRegistry(QUEUE_NAME, redis_connection())


def rq_queue() -> Queue:
    return CustomQueue(QUEUE_NAME, connection=redis_connection())


def rq_worker() -> Worker:
    return CustomWorker(QUEUE_NAME)


def save_task(job: Job, status: str=None) -> Task:
    """Update a task, using the job as the spec for the
    task properties. Fetches a task with the given job ID.
    If no task can be found, a new one is created."""
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
    task.result = job_result_to_string(job)
    task.result_ttl = job.result_ttl
    task.started_at = job.started_at
    task.status = status or job.get_status()
    task.timeout = job.timeout
    task.ttl = job.ttl
    task.title = get_job_result_property(job, 'title')
    task.message = get_job_result_property(job, 'message')
    task.meta = json.dumps(job.meta)

    # Persist any changes to the DB.
    db.session.commit()
    return task


def send_message(message: str, sleep_duration: float):
    """Task to send a message."""
    start_time = time.time()
    logger.debug('message length: %d, duration: %f', len(message), sleep_duration)
    time.sleep(sleep_duration)
    end_time = time.time()
    duration = end_time - start_time
    logger.debug('Done, duration: %f', duration)
    return TaskResult(
        title='Sent Message',
        message=message,
        duration=duration,
        start_time=start_time,
        end_time=end_time,
        message_length=len(message)
    )
