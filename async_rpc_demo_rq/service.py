import uuid

from rq.job import Job
from spyne import ComplexModel, Integer, Unicode, AnyDict, ImageUri
from spyne import rpc, ServiceBase

from .task_queue import task_queue
from .tasks import DETECTION_TASK_TYPE_MAPPING


class ApiResponse(ComplexModel):
    error = Integer
    message = Unicode
    data = AnyDict


class DetectionService(ServiceBase):

    @rpc(ImageUri, Integer(values=(1, 2)), _returns=ApiResponse)
    def analysis(self, image_url, task_type):
        job_id = uuid.uuid4().hex
        func = DETECTION_TASK_TYPE_MAPPING[task_type]
        job: Job = task_queue.enqueue(
            func,
            args=(image_url,),
            job_id=job_id,
            # Result will never expire, clean up result key manually
            result_ttl=-1,
        )
        return ApiResponse(
            error=0,
            message='Succeed',
            data={
                'job_id': job.id,
            },
        )

    @rpc(Unicode, _returns=ApiResponse)
    def query(self, job_id):
        job: Job = task_queue.fetch_job(job_id)
        if not job:
            return ApiResponse(
                error=1,
                message='No job found.'
            )
        return ApiResponse(
            error=0,
            message='Succeed',
            data={
                'job_id': job.id,
                'status': job.get_status(),
                'result': job.result,
            },
        )
