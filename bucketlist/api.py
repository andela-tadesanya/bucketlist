from bucketlist import app
from flask_restful import Resource, Api, abort
from bucketlist.models import User, BucketList, BucketListItem, UserSchema,\
                              BucketListSchema, BucketListItemSchema
from bucketlist.database import db_session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import request, g
from functools import wraps
from sqlalchemy_paginator import Paginator


api = Api(app)


# create a custom login decorator to handle token authentication
def login_required(f):
    '''custom decorator to verify token'''
    @wraps(f)
    def verify_token(*args, **kwargs):
        # check if token in request headers
        if 'token' in request.headers:
            token = request.headers['token']

            # authenticate token
            user = User.verify_auth_token(token)
            if not user:
                abort(403, message='authentication failed')
            else:
                # set user in g
                g.user = user
                return f(*args, **kwargs)
        else:
            abort(401, message='token missing from header')
    return verify_token


def get_bucketlist(user, bucketlist_id):
    '''function to get a bucketlist'''
    query = db_session.query(BucketList).\
            filter_by(created_by=user.id).\
            filter_by(id=bucketlist_id)
    try:
        bl = query.one()
    except NoResultFound:
        abort(404, message='no object with this id found')
    except MultipleResultsFound:
        abort(409, message='multiply bucketlists with this id found')
    return bl


def get_bucketlist_item(bucketlist, bucketlistitem_id):
    '''function to get a bucketlist item'''
    query = db_session.query(BucketListItem).\
            filter_by(bucket_list=bucketlist.id).\
            filter_by(id=bucketlistitem_id)
    try:
        bl_item = query.one()
    except NoResultFound:
        abort(404, message='no object with this id found')
    except MultipleResultsFound:
        abort(409, message='multiply bucketlists with this id found')
    return bl_item


class AppUsers(Resource):

    def post(self):
        '''creates a user'''
        self.username = request.form['username']
        self.password = request.form['password']

        # check that arguments are not empty
        if self.username is None or self.password is None:
            abort(400, message='username/password missing')

        # check if user already exists
        if User.query.filter(User.username == self.username).first() is not None:
            abort(400, message='username unavailable')

        # create a user and commit to database
        u = User(self.username, self.password)
        db_session.add(u)
        db_session.commit()

        schema = UserSchema()
        return schema.dump(u).data, 200

    @login_required
    def get(self):
        '''returns a user'''
        usr = g.user
        schema = UserSchema()
        return schema.dump(usr).data, 200


class Login(Resource):

    def post(self):
        '''verify a user and return a token'''
        self.username = request.form['username']
        self.password = request.form['password']

        # check that arguments are not empty
        if self.username is None or self.password is None:
            abort(400, message='username/password missing')

        # check if user exists
        usr = User.query.filter(User.username == self.username).first()
        if usr is None:
            abort(400, message='username does not exist')

        # authenticate and create token
        if usr.check_password(self.password):
            token = usr.generate_auth_token()
            return {'token': token.decode('ascii')}, 200
        else:
            abort(401, message='authentication failed')


class BucketLists(Resource):

    @login_required
    def post(self):
        '''create a bucketlist'''
        self.name = request.form['name']

        # check if bucketlist already exists
        bl = BucketList.query.filter(BucketList.name == self.name).first()

        if bl is not None:
            abort(409, message='a bucketlist with this name already exists')
        else:
            usr = g.user
            # create new bucketlist and add it to the user
            bl = BucketList(self.name, usr)
            usr.app_bucket_listing.append(bl)

            # add to session
            db_session.add(usr)
            db_session.commit()

            # return a json representation of the object
            schema = BucketListSchema()
            return schema.dump(bl).data, 200

    @login_required
    def get(self):
        '''returns all the bucketlists of the user'''
        usr_id = g.user.id

        # set limit for pagination
        if 'limit' in request.args:
            limit = int(request.args['limit'])
        else:
            limit = 20

        # set page of pagination
        if 'page' in request.args:
            page = int(request.args['page'])
        else:
            page = 1

        # get the bucketlists and implement search if required
        if 'q' in request.args:
            query = db_session.query(BucketList).\
                    filter_by(created_by=usr_id).\
                    filter(BucketList.name.like('%'+request.args['q']+'%'))
            paginator = Paginator(query, limit)
            current_page = paginator.page(page)
            bucketlists = current_page.object_list
        else:
            # get all bucketlists for this user and implement pagination
            query = db_session.query(BucketList).filter_by(created_by=usr_id)
            paginator = Paginator(query, limit)
            current_page = paginator.page(page)
            bucketlists = current_page.object_list

        if bucketlists is None:
            rv = {'bucketlists': 'none'}
        else:
            ls = []
            schema = BucketListSchema()

            for bucketlist in bucketlists:
                ls.append(schema.dump(bucketlist).data)
            rv = {
                    'total_objects': current_page.paginator.count,
                    'total_pages': current_page.paginator.total_pages,
                    'current_page': current_page.number,
                    'has_next_page': current_page.has_next(),
                    'has_previous_page': current_page.has_previous(),
                    'bucketlists': ls
                 }

        return rv, 200


class BucketListSingle(Resource):

    @login_required
    def get(self, id):
        '''return single bucketlist'''
        usr = g.user
        bl = get_bucketlist(usr, id)

        schema = BucketListSchema()
        return schema.dump(bl).data, 200

    @login_required
    def put(self, id):
        '''update a bucketlist of the user'''
        usr = g.user

        # get the bucketlist
        bl = get_bucketlist(usr, id)

        # update name of bucketlist
        if request.form['name']:
            bl.name = request.form['name']

        # commit changes to database
        db_session.add(bl)
        db_session.commit()

        schema = BucketListSchema()
        return schema.dump(bl).data, 200

    @login_required
    def delete(self, id):
        '''delete a bucketlist'''
        usr = g.user

        # get the bucketlist
        bl = get_bucketlist(usr, id)

        # delete the bucketlist
        db_session.delete(bl)
        db_session.commit()

        return {'message': 'bucketlist deleted'}, 200


class BucketListItemResource(Resource):

    @login_required
    def post(self, id):
        '''creates a new item in a bucketlist'''
        usr = g.user
        bl = get_bucketlist(usr, id)
        self.name = request.form['name']

        # create new bucketlist item and append to bucketlist
        item = BucketListItem(self.name, bl)
        item.start()
        bl.app_bucketlist_items.append(item)

        # commit to database
        db_session.add(bl)
        db_session.commit()

        schema = BucketListItemSchema()
        return schema.dump(item).data, 200

    @login_required
    def put(self, id, item_id):
        '''update a bucket list item'''
        usr = g.user
        bl = get_bucketlist(usr, id)

        # get the bucketlist item
        bl_item = get_bucketlist_item(bl, item_id)

        # update name
        if 'name' in request.form:
            bl_item.name = request.form['name']

        # set if done
        if 'done' in request.form:
            if request.form['done'].lower() == 'true':
                bl_item.end()
            elif request.form['done'].lower() == 'false':
                bl_item.start()
            else:
                abort(406, message='unsupported value for done')

        # commit to database
        db_session.add(bl_item)
        db_session.commit()

        schema = BucketListItemSchema()
        return schema.dump(bl_item).data, 200

    @login_required
    def delete(self, id, item_id):
        '''delete a bucket list item'''
        usr = g.user
        bl = get_bucketlist(usr, id)

        # get the bucketlist item
        bl_item = get_bucketlist_item(bl, item_id)

        # delete the bucketlist item
        db_session.delete(bl_item)
        db_session.commit()

        return {'message': 'bucketlist item deleted'}, 200


# create resource mappings
api.add_resource(AppUsers,
                 '/api/v1.0/users',
                 endpoint='api_users')
api.add_resource(Login,
                 '/api/v1.0/auth/login',
                 endpoint='api_login')
api.add_resource(BucketLists,
                 '/api/v1.0/bucketlists',
                 endpoint='api_bucketlists')
api.add_resource(BucketListSingle,
                 '/api/v1.0/bucketlists/<int:id>',
                 endpoint='api_bucketlist')
api.add_resource(BucketListItemResource,
                 '/api/v1.0/bucketlists/<int:id>/items',
                 '/api/v1.0/bucketlists/<int:id>/items/<int:item_id>',
                 endpoint='api_bucketlist_item')
