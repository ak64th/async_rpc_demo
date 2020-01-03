from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

metadata = MetaData()

engine = create_engine('sqlite:///db.sqlite3')
metadata.bind = engine
Session = scoped_session(sessionmaker(bind=engine))
