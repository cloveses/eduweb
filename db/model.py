from datetime import datetime
from mongoengine import *

connect("mypro")

class Sessions(Document):
    session_id = StringField()
    token = StringField()
    session_dict = DictField()

class User(Document):
    name = StringField()
    passwd = StringField()
    lastdate = DateTimeField(default=datetime.now())

class ProjectName(Document):
    name = StringField(required=True)
    url = StringField(required=True)
    introduce = StringField()
    status = BooleanField(default=True)

        