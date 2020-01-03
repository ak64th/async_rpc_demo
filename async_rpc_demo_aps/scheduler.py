import json
import logging

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_ADDED
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm.exc import NoResultFound

from .db import engine, metadata, Session
from .models import JobResult

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', engine=engine, metadata=metadata)
scheduler.add_executor('processpool')


def on_submit(event):
    logger.debug(u'Job [%s] submitted', event.job_id)
    db_session = Session()
    job_result = JobResult(
        job_id=event.job_id,
        result=None,
        error=0,
        status=JobResult.Status.PENDING,
    )
    db_session.add(job_result)
    db_session.commit()
    Session.remove()


def on_finish(event):
    db_session = Session()
    try:
        job_result = db_session.query(JobResult).filter(
            JobResult.job_id == event.job_id
        ).one()
    except NoResultFound:
        job_result = JobResult(
            job_id=event.job_id,
            result=None,
            error=0,
        )
        db_session.add(job_result)
    if not event.exception:
        logger.debug(u'Job [%s] returns `%s`', event.job_id, event.retval)
        job_result.result = json.dumps(event.retval)
        job_result.status = JobResult.Status.DONE
    else:
        logger.error(u'Job [%s] failed', event.job_id)
        job_result.error = 1
        job_result.status = JobResult.Status.FAILED
    db_session.commit()
    Session.remove()


scheduler.add_listener(on_submit, EVENT_JOB_ADDED)
scheduler.add_listener(on_finish, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
