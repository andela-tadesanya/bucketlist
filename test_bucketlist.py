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

    def get_token(self):
        '''generates a token'''
        rv = self.app.post('/api/v1.0/auth/login',
                           data={
                                'username': 'testuser',
                                'password': 'password',
                            })
        return rv.data['token']

    def test_create_user(self):
        '''test if user can be created'''
        rv = self.app.post('/api/v1.0/users', data={
            'username': 'testuser',
            'password': 'password'
            })
        assert 'username' in rv.data
        assert 'id' in rv.data
        assert 'app_bucket_listing' in rv.data

    def test_create_token(self):
        '''test token creation'''
        rv = self.app.post('/api/v1.0/auth/login',
                           data={
                            'username': 'testuser',
                            'password': 'password',
                           })
        assert 'token' in rv.data
        assert len(rv.data['token']) == 122

    def test_invalid_token(self):
        '''test when an invalid token is sent'''
        rv = self.app.get('/api/v1.0/users',
                          header={
                            'token': 'uguguiguiguigugugiguiig'
                          })
        assert rv.status_code == 403

    def test_no_token(self):
        '''test when token is not provided'''
        rv = self.app.get('/api/v1.0/users')
        assert rv.status_code == 401

    def test_valid_token(self):
        '''test if user can use token'''
        token = self.get_token()
        rv = self.app.get('/api/v1.0/users',
                          header={
                            'token': token
                          })
        assert rv.status_code == 200

    def test_create_bucketlist(self):
        '''test creating a bucketlist'''
        token = self.get_token()
        rv = self.app.post('/api/v1.0/bucketlists',
                           data={
                                'name': 'list1'
                           },
                           header={
                                'token': token
                           })
        assert 'app_bucketlist_items' in rv.data
        assert 'created_by' in rv.data
        assert 'date_created' in rv.data
        assert 'date_modified' in rv.data
        assert 'id' in rv.data
        assert 'name' in rv.data
        assert rv.data['date_created'] != rv.data['date_modified']

    def test_get_bucketlists(self):
        '''test fetching a bucketlist'''
        token = self.get_token()
        rv = self.app.get('/api/v1.0/bucketlists',
                          header={
                                'token': token
                          })
        assert 'bucketlists' in rv.data
        assert 'current_page' in rv.data
        assert 'has_next_page' in rv.data
        assert 'has_previous_page' in rv.data
        assert 'total_objects' in rv.data
        assert 'total_pages' in rv.data
        assert len(rv.data['bucketlists']) > 0

    def test_get_bucketlists_pagination(self):
        '''test fetching a bucketlist with pagination'''
        token = self.get_token()
        rv = self.app.get('/api/v1.0/bucketlists?limit=1&page=1',
                          header={
                                'token': token
                          })
        assert 'bucketlists' in rv.data
        assert 'current_page' in rv.data
        assert 'has_next_page' in rv.data
        assert 'has_previous_page' in rv.data
        assert 'total_objects' in rv.data
        assert 'total_pages' in rv.data
        assert len(rv.data['bucketlists']) == 1

    def test_get_bucketlists_with_query(self):
        '''test fetching a bucketlist by query'''
        token = self.get_token()
        rv = self.app.get('/api/v1.0/bucketlists?q=list1',
                          header={
                                'token': token
                          })
        assert 'bucketlists' in rv.data
        assert 'current_page' in rv.data
        assert 'has_next_page' in rv.data
        assert 'has_previous_page' in rv.data
        assert 'total_objects' in rv.data
        assert 'total_pages' in rv.data
        assert len(rv.data['bucketlists']) == 1
        assert rv.data['bucketlists']['name'] == 'list1'

    def test_get_bucketlist_item(self):
        '''test getting a bucketlist item'''
        token = self.get_token()
        rv = self.app.get('/api/v1.0/bucketlists/1',
                          header={
                                'token': token
                          })
        assert 'app_bucketlist_items' in rv.data
        assert 'created_by' in rv.data
        assert 'date_created' in rv.data
        assert 'date_modified' in rv.data
        assert 'id' in rv.data
        assert 'name' in rv.data
        assert rv.data['id'] == 1
        assert rv.data['created_by'] == 1

    def test_update_bucketlist(self):
        '''test update of a bucketlist'''
        token = self.get_token()
        rv = self.app.put('/api/v1.0/bucketlists/1',
                          header={
                            'token': token
                          },
                          data={
                            'name': 'list2'
                          })
        assert 'app_bucketlist_items' in rv.data
        assert 'created_by' in rv.data
        assert 'date_created' in rv.data
        assert 'date_modified' in rv.data
        assert 'id' in rv.data
        assert 'name' in rv.data
        assert rv.data['name'] == 'list2'
        assert rv.data['id'] == 1
        assert rv.data['created_by'] == 1
        assert rv.data['date_created'] != rv.data['date_modified']

    def test_create_bucketlist_item(self):
        '''test creation of a bucketlist item'''
        token = self.get_token()
        rv = self.app.post('/api/v1.0/bucketlists/1/items',
                           header={
                            'token': token
                           },
                           data={
                            'name': 'listitem1'
                           })
        assert 'name' in rv.data
        assert 'done' in rv.data
        assert 'date_created' in rv.data
        assert 'date_modified' in rv.data
        assert 'id' in rv.data
        assert rv.data['date_created'] == rv.data['date_modified']
        assert rv.data['name'] == 'listitem1'

    def test_update_bucketlist_item(self):
        '''test if bucketlist item can be updated'''
        token = self.get_token()
        rv = self.app.put('/api/v1.0/bucketlists/1/items/1',
                          header={
                            'token': token
                           },
                          data={
                            'name': 'listitem2',
                            'done': 'true'
                           })
        assert 'name' in rv.data
        assert 'done' in rv.data
        assert 'date_created' in rv.data
        assert 'date_modified' in rv.data
        assert 'id' in rv.data
        assert rv.data['date_created'] != rv.data['date_modified']
        assert rv.data['name'] == 'listitem2'
        assert rv.data['done'] == 'true'

    def test_delete_bucketlist_item(self):
        '''delete bucketlist item'''
        token = self.get_token()
        rv = self.app.delete('/api/v1.0/bucketlists/1/items/1',
                             header={
                                'token': token
                               },
                             data={
                                'name': 'listitem2',
                                'done': 'true'
                               })
        assert 'message' in rv.data
        assert rv.data['message'] == 'bucketlist item deleted'
        assert rv.status_code == 200

    def test_delete_bucketlist(self):
        '''test deleting a bucketlist'''
        token = self.get_token()
        rv = self.app.delete('/api/v1.0/bucketlists/1',
                             header={
                                'token': token
                             })
        assert 'message' in rv.data
        assert rv.data['message'] == 'bucketlist deleted'
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()
