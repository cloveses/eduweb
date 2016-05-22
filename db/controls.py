# -*- coding: utf-8 -*-

from datetime import datetime
from mylib import tools
from .model import User
from .model import ProjectName

superadmin = 'superadmn'

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

def del_user(name):
    res = User.objects(name=name)
    if res.count():
        res[0].delete()
        return True

def add_proname(name,url):
    if name and url:
        ProjectName(name=name,url=url).save()

def chn_status(name):
    res = ProjectName.objects(name=name)
    if res.count():
        doc = res[0]
        doc.status = not doc.status
        doc.save()

def add_admin():
    if not User.objects(name=superadmin).count():
        add_user(superadmin,'myadmin')

def get_all_user():
    res = User.objects(name__not__exact=superadmin)
    if res.count():
        return res
    return []

def get_all_pro():
    res = ProjectName.objects()
    if res.count():
        return res
    return []
