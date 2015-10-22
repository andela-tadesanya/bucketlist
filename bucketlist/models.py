from sqlalchemy import Column, Integer, String, DateTime, Sequence, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from bucketlist.database import Base
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    pwdhash = Column(String(100))

    # declare relationships
    bucketlist = relationship("BucketList", backref=backref('users', order_by=id))

    def __init__(self, username=None, email=None, password=None):
        self.username = username.lower()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        '''hash the password and sets it'''
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        '''hashes password and compares with password in database'''
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return '<User %r>' % (self.username)


class BucketList(Base):
    __tablename__ = 'bucketlists'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    date_created = Column(DateTime, default=datetime.now)
    date_modified = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'))

    # declare relationships
    user = relationship('User', backref=backref('bucketlists', order_by=id))
    item = relationship("Items", backref=backref('bucketlists', order_by=id))

    def __init__(self, name=None, created_by=None):
        self.name = name.lower()
        self.created_by = created_by
        self.set_creation_date()
        self.set_modify_date()

    def set_creation_date(self):
        '''sets date object was created'''
        self.date_created = datetime.now()

    def set_modify_date(self):
        '''sets date object is last modified'''
        self.date_modified = datetime.now()

    def __repr__(self):
        return '<BucketList %r>' % (self.name)

class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    date_created = Column(DateTime, default=datetime.now)
    date_modified = Column(DateTime)
    bucket_list = Column(Integer, ForeignKey('bucketlists.id'))
    done = Column(Boolean, unique=False, default=True)

    # declare relationships
    #bucketlist = relationship('BucketList', backref=backref('items', order_by=id))

    def __init__(self, name=None, done=False, bucket_list=None):
        self.name = name.lower()
        self.done = done
        self.bucket_list = bucket_list
        self.set_creation_date()
        self.set_modify_date()

    def set_creation_date(self):
        '''sets date object was created'''
        self.date_created = datetime.now()

    def set_modify_date(self):
        '''sets date object is last modified'''
        self.date_modified = datetime.now()

    def end(self):
        '''sets done to true'''
        self.done = True

    def start(self):
        '''sets done to false'''
        self.done = False

    def __repr__(self):
        return '<Items %r done: %r>' % (self.name, self.done)