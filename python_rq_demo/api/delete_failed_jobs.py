from flask_jsonpify import jsonify
from rq.job import Job
from .. import app
from ..tasks import redis_connection, rq_failed_job_registry


@app.route('/api/delete_failed_jobs', methods=['POST'])
def api_delete_failed_jobs():
    r = rq_failed_job_registry()
    job_ids = r.get_job_ids()
    connection = redis_connection()
    delete_count = 0
    for job_id in job_ids:
        job = Job.fetch(job_id, connection=connection)
        job.delete()
        delete_count += 1

    return jsonify({
        'count': delete_count
    })


