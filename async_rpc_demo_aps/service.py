import json
import uuid

from spyne import ComplexModel, Integer, Unicode, AnyDict
from spyne import rpc, ServiceBase
from sqlalchemy.orm.exc import NoResultFound

from .db import Session
from .models import JobResult
from .scheduler import scheduler
from .tasks import detect_type_1, detect_type_2


class ApiResponse(ComplexModel):
    error = Integer
    message = Unicode
    data = AnyDict


DETECTION_TASK_TYPE_MAPPING = {
    1: detect_type_1,
    2: detect_type_2,
}


class DetectionService(ServiceBase):

    @rpc(Unicode, Unicode, Integer(values=(1, 2)), _returns=ApiResponse)
    def analysis(self, infrared_image, visible_image, task_type):
        job_id = uuid.uuid4().hex
        func = DETECTION_TASK_TYPE_MAPPING[task_type]
        job = scheduler.add_job(
            func=func,
            args=(infrared_image, visible_image),
            id=job_id,
        )
        return ApiResponse(
            error=0,
            message='Succeed',
            data={
                'job_id': job.id
            },
        )

    @rpc(Unicode, _returns=ApiResponse)
    def query(self, job_id):
        db_session = Session()
        try:
            job_result = db_session.query(JobResult).filter(
                JobResult.job_id == job_id
            ).one()
        except NoResultFound:
            return ApiResponse(
                error=1,
                message='No job found.'
            )
        finally:
            Session.remove()
        return ApiResponse(
            error=0,
            message='Succeed',
            data={
                'job_id': job_result.job_id,
                'status': job_result.status,
                'result': json.loads(job_result.result)
            },
        )
