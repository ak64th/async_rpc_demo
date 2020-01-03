import multiprocessing as mp

from redis import Redis
from rq import Worker
from waitress import serve

from .task_queue import task_queue


def start_worker():
    worker = Worker(
        [task_queue],
        connection=Redis(),
        default_result_ttl=-1,
    )
    worker.work()


if __name__ == '__main__':
    from .wsgi import wsgi_application

    worker_process = mp.Process(target=start_worker)
    worker_process.start()
    serve(wsgi_application, host='0.0.0.0', port=8000)
    worker_process.terminate()
