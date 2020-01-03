from redis import Redis
from rq import Queue

task_queue = Queue(connection=Redis())
