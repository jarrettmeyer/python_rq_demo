import json
from rq.job import Job
from sqlalchemy import Column, DateTime, Numeric, String
from .. import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = Column(String(256), nullable=False, primary_key=True)
    started_at = Column(DateTime(timezone=True), nullable=False)
    func_name = Column(String(256), nullable=False)
    status = Column(String(256), nullable=False)
    enqueued_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    result = Column(String(1024))
    duration = Column(Numeric(18, 6))

    @staticmethod
    def create(job: Job):
        task = Task(
            id=job.id,
            started_at=job.started_at,
            func_name=job.func_name,
            status=job.get_status()
        )
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update(job: Job):
        task = Task.query.get(job.id)
        if task is None:
            task = Task.create(job)
        elif task.status not in ['failed', 'finished']:
            task.status = job.get_status()
            task.enqueued_at = job.enqueued_at
            task.ended_at = job.ended_at
            if job.result is not None:
                task.result = json.dumps( job.result.toDict() )
                task.duration = job.result.duration

        # Commit any changes that were made during
        # this method.
        db.session.commit()
        return task

