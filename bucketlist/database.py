from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bucket.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(
                                        autocommit=False,
                                        autoflush=False,
                                        bind=engine
                                        ))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all models and create the database tables
    import bucketlist.models
    Base.metadata.create_all(bind=engine)