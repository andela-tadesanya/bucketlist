from sqlalchemy import Column, Integer, String, DateTime,\
                       ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from bucketlist.database import Base
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer as
                          Serializer, BadSignature, SignatureExpired)
from bucketlist import app
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    pwdhash = Column(String(100))

    # declare relationships
    app_bucket_listing = relationship(
                              "BucketList",
                              order_by="BucketList.id",
                              backref="user",
                              cascade="all, delete, delete-orphan")

    def __init__(self, username=None, password=None):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        '''hash the password and sets it'''
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        '''hashes password and compares with password in database'''
        return check_password_hash(self.pwdhash, password)

    def generate_auth_token(self, expiration=1200):
        '''creates a token'''
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            # valid token, but expired
            return None
        except BadSignature:
            # invalid token
            return None

        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % (self.username)


class BucketList(Base):
    __tablename__ = 'bucketlists'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    date_created = Column(DateTime, default=datetime.now)
    date_modified = Column(DateTime,
                           default=datetime.now,
                           onupdate=datetime.now)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=True)

    # declare relationships
    app_user = relationship('User',
                            backref=backref('bucketlists', order_by=id))
    app_bucketlist_items = relationship(
                         'BucketListItem',
                         order_by='BucketListItem.id',
                         backref='bucketlists',
                         cascade='all, delete, delete-orphan')

    def __init__(self, name=None, created_by=None):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '<BucketList %d:%r>' % (self.id, self.name)


class BucketListItem(Base):
    __tablename__ = 'bucketlist_item'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    done = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.now)
    date_modified = Column(DateTime,
                           default=datetime.now,
                           onupdate=datetime.now)
    bucket_list = Column(Integer, ForeignKey('bucketlists.id'))

    # declare relationships
    app_bucketlist = relationship('BucketList',
                                  backref=backref('bucketlist_item',
                                                  order_by=id))

    def __init__(self, name=None, bucket_list=None):
        self.name = name
        self.start()
        self.bucket_list = bucket_list

    def end(self):
        '''sets done to true'''
        self.done = True

    def start(self):
        '''sets done to false'''
        self.done = False

    def __repr__(self):
        return '<BucketListItem %d:%r>' % (self.id, self.name)


# generate marshmallow schemas
class BucketListItemSchema(ModelSchema):
    class Meta:
        fields = ('id', 'name', 'date_created', 'date_modified', 'done')
        model = BucketListItem


class BucketListSchema(ModelSchema):
    class Meta:
        fields = ('id', 'name', 'date_created',
                  'date_modified', 'app_bucketlist_items', 'created_by')
        model = BucketList
    app_bucketlist_items = fields.Nested(BucketListItemSchema, many=True)


class UserSchema(ModelSchema):
    class Meta:
        fields = ('id', 'username', 'app_bucket_listing')
        model = User
    app_bucket_listing = fields.Nested(BucketListSchema, many=True)
