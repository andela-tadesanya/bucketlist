from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session
from sqlalchemy.ext.declarative import declarative_base


# create an engine and session that can be initialized dynamically
engine = None
db_session = scoped_session(lambda: create_session(bind=engine,
                                                   autocommit=False,
                                                   autoflush=False,
                                                   expire_on_commit=False))
Base = declarative_base()
Base.query = db_session.query_property()


def init_engine(uri, **kwargs):
    '''sets up a database engine'''
    global engine
    engine = create_engine(uri, **kwargs)
    return engine


def init_db():
    '''import all models and create the database tables'''
    import bucketlist.models
    Base.metadata.create_all(bind=engine)


def drop_db():
    '''drop all tables'''
    import bucketlist.models
    Base.metadata.drop_all(bind=engine, checkfirst=True)
