# -*- coding: utf-8 -*-

from datetime import datetime
from mylib import tools
from .model import User

def add_user(name,passwd):
    if name and passwd:
        passwd = tools.make_password(passwd)
        doc = User(name=name,passwd=passwd)
        doc.save()
        return doc

def get_user(name,passwd):
    passwd = tools.make_password(passwd)
    res = User.objects(name=name,passwd=passwd)
    if res.count():
        u = res[0]
        u.lastdate = datetime.now()
        u.save()
        return u