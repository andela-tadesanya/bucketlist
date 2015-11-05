import bucketlist
import unittest
from bucketlist import create_app
from bucketlist.database import init_db, db_session, drop_db
import json


class BucketListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app = create_app('test_config.py')
        init_db()
        self.client = bucketlist.app.test_client()

    @classmethod
    def tearDownClass(self):
        db_session.close()
        db_session.remove()
        drop_db()

    def get_token(self):
        '''generates a token'''
        rv = self.client.post('/api/v1.0/auth/login',
                              data={
                                'username': 'testuser',
                                'password': 'password',
                              })
        resp = json.loads(rv.data)
        return resp['token']

    def test_01_create_user(self):
        '''test if user can be created'''
        rv = self.client.post('/api/v1.0/users', data={
            'username': 'testuser',
            'password': 'password'
            })
        resp = json.loads(rv.data)
        assert rv.status_code == 200
        assert 'username' in resp
        assert 'id' in resp
        assert 'app_bucket_listing' in resp

    def test_02_create_token(self):
        '''test token creation'''
        rv = self.client.post('/api/v1.0/auth/login',
                              data={
                                'username': 'testuser',
                                'password': 'password',
                              })
        resp = json.loads(rv.data)
        assert 'token' in resp
        assert len(resp['token']) == 122

    def test_03_invalid_token(self):
        '''test when an invalid token is sent'''
        rv = self.client.get('/api/v1.0/users',
                             headers={
                                'token': 'uguguiguiguigugugiguiig'
                             })
        assert rv.status_code == 403

    def test_04_no_token(self):
        '''test when token is not provided'''
        rv = self.client.get('/api/v1.0/users')
        assert rv.status_code == 401

    def test_05_valid_token(self):
        '''test if user can use token'''
        token = self.get_token()
        rv = self.client.get('/api/v1.0/users',
                             headers={
                                'token': token
                             })
        assert rv.status_code == 200

    def test_06_create_bucketlist(self):
        '''test creating a bucketlist'''
        token = self.get_token()
        rv = self.client.post('/api/v1.0/bucketlists',
                              data={
                                'name': 'list1'
                              },
                              headers={
                                'token': token
                              })
        resp = json.loads(rv.data)
        assert 'app_bucketlist_items' in resp
        assert 'created_by' in resp
        assert 'date_created' in resp
        assert 'date_modified' in resp
        assert 'id' in resp
        assert 'name' in resp

    def test_07_get_bucketlists(self):
        '''test fetching a bucketlist'''
        token = self.get_token()
        rv = self.client.get('/api/v1.0/bucketlists',
                             headers={
                                'token': token
                             })
        resp = json.loads(rv.data)
        assert 'bucketlists' in resp
        assert 'current_page' in resp
        assert 'has_next_page' in resp
        assert 'has_previous_page' in resp
        assert 'total_objects' in resp
        assert 'total_pages' in resp

        assert len(resp['bucketlists']) > 0

    def test_08_get_bucketlists_pagination(self):
        '''test fetching a bucketlist with pagination'''
        token = self.get_token()
        rv = self.client.get('/api/v1.0/bucketlists?limit=1&page=1',
                             headers={
                                'token': token
                             })
        resp = json.loads(rv.data)
        assert 'bucketlists' in resp
        assert 'current_page' in resp
        assert 'has_next_page' in resp
        assert 'has_previous_page' in resp
        assert 'total_objects' in resp
        assert 'total_pages' in resp
        assert len(resp['bucketlists']) == 1

    def test_09_get_bucketlists_with_query(self):
        '''test fetching a bucketlist by query'''
        token = self.get_token()
        rv = self.client.get('/api/v1.0/bucketlists?q=list1',
                             headers={
                                'token': token
                             })
        resp = json.loads(rv.data)
        assert 'bucketlists' in resp
        assert 'current_page' in resp
        assert 'has_next_page' in resp
        assert 'has_previous_page' in resp
        assert 'total_objects' in resp
        assert 'total_pages' in resp
        assert len(resp['bucketlists']) == 1
        assert resp['bucketlists'][0]['name'] == 'list1'

    def test_10_get_bucketlist_item(self):
        '''test getting a bucketlist item'''
        token = self.get_token()
        rv = self.client.get('/api/v1.0/bucketlists/1',
                             headers={
                                'token': token
                             })
        resp = json.loads(rv.data)
        assert 'app_bucketlist_items' in resp
        assert 'created_by' in resp
        assert 'date_created' in resp
        assert 'date_modified' in resp
        assert 'id' in resp
        assert 'name' in resp
        assert resp['id'] == 1
        assert resp['created_by'] == 1

    def test_11_update_bucketlist(self):
        '''test update of a bucketlist'''
        token = self.get_token()
        rv = self.client.put('/api/v1.0/bucketlists/1',
                             headers={
                               'token': token
                             },
                             data={
                               'name': 'list2'
                             })
        resp = json.loads(rv.data)
        assert 'app_bucketlist_items' in resp
        assert 'created_by' in resp
        assert 'date_created' in resp
        assert 'date_modified' in resp
        assert 'id' in resp
        assert 'name' in resp
        assert resp['name'] == 'list2'
        assert resp['id'] == 1
        assert resp['created_by'] == 1
        assert resp['date_created'] != resp['date_modified']

    def test_12_create_bucketlist_item(self):
        '''test creation of a bucketlist item'''
        token = self.get_token()
        rv = self.client.post('/api/v1.0/bucketlists/1/items',
                              headers={
                                'token': token
                              },
                              data={
                                'name': 'listitem1'
                              })
        resp = json.loads(rv.data)
        assert 'name' in resp
        assert 'done' in resp
        assert 'date_created' in resp
        assert 'date_modified' in resp
        assert 'id' in resp
        assert resp['name'] == 'listitem1'

    def test_13_update_bucketlist_item(self):
        '''test if bucketlist item can be updated'''
        token = self.get_token()
        rv = self.client.put('/api/v1.0/bucketlists/1/items/1',
                             headers={
                                'token': token
                             },
                             data={
                                'name': 'listitem2',
                                'done': 'true'
                             })
        resp = json.loads(rv.data)
        assert 'name' in resp
        assert 'done' in resp
        assert 'date_created' in resp
        assert 'date_modified' in resp
        assert 'id' in resp
        assert resp['date_created'] != resp['date_modified']
        assert resp['name'] == 'listitem2'
        assert resp['done'] is True

    def test_14_delete_bucketlist_item(self):
        '''delete bucketlist item'''
        token = self.get_token()
        rv = self.client.delete('/api/v1.0/bucketlists/1/items/1',
                                headers={
                                  'token': token
                                },
                                data={
                                    'name': 'listitem2',
                                    'done': 'true'
                                })
        resp = json.loads(rv.data)
        assert 'message' in resp
        assert resp['message'] == 'bucketlist item deleted'
        assert rv.status_code == 200

    def test_15_delete_bucketlist(self):
        '''test deleting a bucketlist'''
        token = self.get_token()
        rv = self.client.delete('/api/v1.0/bucketlists/1',
                                headers={
                                    'token': token
                                })
        resp = json.loads(rv.data)
        assert 'message' in resp
        assert resp['message'] == 'bucketlist deleted'

        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()
