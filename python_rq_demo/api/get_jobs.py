from flask_jsonpify import jsonify
from redis import Redis
from rq import Queue
from rq.job import Job
from .. import app
from ..config import redis_connection, rq_queue


@app.route('/api/jobs')
def api_get_jobs():
    redis_conn: Redis = redis_connection()
    redis_keys = redis_conn.keys('rq:job:*')
    job_ids = list(map(lambda key: str(key)[9:-1], redis_keys))
    return jsonify({
        'job_ids': job_ids
    })
