import os
import bucketlist
import unittest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import bucketlist.models


class BucketListTestCase(unittest.TestCase):

    def setUp(self):
        self.db_file, self.db_name = tempfile.mkstemp()
        db = 'sqlite:///%s' % (self.db_name)
        engine = create_engine(db, convert_unicode=True)
        db_session = scoped_session(sessionmaker(
                                                autocommit=False,
                                                autoflush=False,
                                                bind=engine
                                                ))
        Base = declarative_base()
        Base.query = db_session.query_property()
        Base.metadata.create_all(bind=engine)
        self.app = bucketlist.app.test_client()

    def tearDown(self):
        os.close(self.db_file)
        os.unlink(self.db_name)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Hello World!' in rv.data

if __name__ == '__main__':
    unittest.main()
