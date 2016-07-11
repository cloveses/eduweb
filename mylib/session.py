#!/usr/bin/env python
import os
import time
import functools
import datetime
from hashlib import sha1
from db.model import Sessions
from settings import session_settings
from tornado import ioloop


class SessionIvaild(Exception):
    pass

class SessionManagerBase:
    def generate_session_id(self, salt):
        rand = os.urandom(16)
        now = time.time()
        return sha1(("%s%s%s" % (rand, now, salt)).encode('utf-8')).hexdigest()

    def create_new(self, session_id):
        pass

    def save_session(self, session):
        pass

    def load_session(self, session_id=None):
        pass


class MongoSessionManager(SessionManagerBase):
    # def __init__(self, **kw):
    #     pass

    def create_new(self, session_id):
        return BaseSession(session_id)

    def save_session(self, session):
        session.save()

    def load_session(self, session_id=None):
        data = {}
        sessions=None
        if session_id:
            session_data = Sessions.objects(session_id=session_id)
            # print(__file__,':',session_data.count())
            if session_data.count():
                sessions = session_data[0]
                data = sessions.session_dict
            sessions = sessions if sessions else Sessions()
        return BaseSession(session_id, sessions, data)

class BaseSession(dict):
    def __init__(self, session_id='', sessions=Sessions(), data={}):
        self.__session_id = session_id
        self.__session = sessions
        self.__session.session_id = session_id
        self.update(data)
        # self.__session.session_dict.update(data)
        self.__change = False

    def get_session_id(self):
        return self.__session_id

    def save(self):
        if self.__change:
            self.__session.session_dict.update(self)
            self.__session.save()
            self.__change = False

    def destroy(self):
        if self.__session.id:
            self.__session.delete()
            self.__change = False

    def __missing__(self,key):
        return None

    def __delitem__(self,key):
        if key in  self:
            del self[key]
            self.__change = True
            self.save()

    def __setitem__(self, key, val):
        self.__change = True
        super().__setitem__(key, val)
        self.save()


mgr = MongoSessionManager()
import logging
logger = logging.getLogger()


def session(func):
    @functools.wraps(func)
    def warpper(self, *args, **kwargs):
        cookie_name = session_settings['cookie_name']
        cookie_expires = session_settings["cookie_expires_days"]
        session_id = self.get_secure_cookie(cookie_name)
        if session_id:
            session_id = session_id.decode('utf-8')
            # print('session id:',session_id)
            session = mgr.load_session(session_id)
            logger.debug("Load session: {0}".format(session_id))
            setattr(self, 'session', session)
        else:
            secret_key = session_settings['secret_key']
            session_id = mgr.generate_session_id(secret_key)
            self.set_secure_cookie(cookie_name, session_id, expires_days = cookie_expires)
            session = mgr.create_new(session_id)
            logger.debug("New session: {0}".format(session_id))
            setattr(self, 'session', session)
        logger.debug("Session Id: {0}".format(session_id))
        return_val = func(self, *args, **kwargs)
        self.session.save()
        return return_val
    return warpper

# def destroy_sessions():
#     sessions = Sessions.objects().delete()

# ioloop.PeriodicCallback(destroy_sessions,session_settings['invalid_days'] * 60 * 60 * 1000).start()