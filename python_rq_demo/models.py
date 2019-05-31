import json
from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text
from . import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = Column(String(256), nullable=False, primary_key=True)
    started_at = Column(DateTime(timezone=True))
    func_name = Column(String(256))
    status = Column(String(256))
    enqueued_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    result = Column(String(1024))
    duration = Column(Numeric(18, 6))
    created_at = Column(DateTime(timezone=True))
    ttl = Column(Integer())
    result_ttl = Column(Integer())
    failure_ttl = Column(Integer())
    timeout = Column(Integer())
    title = Column(String(256))
    message = Column(Text())
    meta = Column(String(1024))

    def __repr___(self):
        return '<Task {0}, status: {1}>'.format(self.id, self.status)

