import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from .db import engine, metadata

Base = declarative_base(bind=engine, metadata=metadata)


class JobResult(Base):
    class Status(object):
        PENDING = 'PENDING'
        FAILED = 'FAILED'
        DONE = 'DONE'

    __tablename__ = 'job_results'

    id = sa.Column(sa.Integer, primary_key=True)
    job_id = sa.Column(sa.String(50), index=True, nullable=False)
    result = sa.Column(sa.Text, server_default='{}')
    status = sa.Column(sa.String(20), server_default=Status.PENDING)
    error = sa.Column(sa.Integer, server_default='0')
