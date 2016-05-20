# -*- coding: utf-8 -*-

""" Inherit ~tornado.web.RequestHandler to change the template engine,
and define a decorator to wrap handler to do url route.

Here is the example::

    from common.web import BaseHandler, route

    @route(r'/')
    class IndexHandler(BaseHandler):
        def get(self):
            self.write("Hello, world!")

Note: To let the ``route`` decorator be right, you must see also the ``url.py``
module.
"""
import os
import socket
import fcntl
import struct
from tornado import gen
import tornado.web
import mako.lookup
import mako.template
import mako.exceptions
from mylib.session import session
from mylib import tools

from sha3._sha3 import sha3_512
import settings


TEMPLATE_PATH = settings.web_server['template_path']
LOOK_UP = mako.lookup.TemplateLookup(
    directories=[TEMPLATE_PATH, ],
    input_encoding='utf-8',
    encoding_errors='replace',
    strict_undefined=True)


class BaseHandler(tornado.web.RequestHandler):

    _mako_templates = {}

    def initialize(self, lookup=LOOK_UP):
        '''
           Set template lookup object, Defalut is LOOK_UP
        '''
        self._lookup = lookup

    def get_template_path(self):
        return TEMPLATE_PATH

    def render(self,tmpl_name,kwargs=None):
        kwargs = kwargs if kwargs is not None else {}
        super().render(tmpl_name,**kwargs)

    def render_string(self,template_name,**kwargs):
        kwargs = kwargs if kwargs is not None else {}
        print(__file__,':',template_name)
        if template_name in BaseHandler._mako_templates:
            mtemplate = BaseHandler._mako_templates.get(template_name)
        else:
            try:
                mtemplate = self._lookup.get_template(template_name)
            except mako.exceptions.TopLevelLookupException:
                print('Do not find templates files!')
                self.send_error(404)
            else:
                BaseHandler._mako_templates[template_name] = mtemplate
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        content = mtemplate.render(**namespace)
        return content

    @property
    def hint_info(self):
        info = self.get_secure_cookie('info')
        if info:
            return info.decode('utf-8')
            self.set_secure_cookie('info','')
        return ''

    @session
    def get_current_user(self):
        name = self.get_secure_cookie('name').decode('utf-8')
        if name:
            v = tools.make_verifytext_key(name)
            if v == self.session['name']:
                return name

def handler(obj):
    import mongoengine
    from bson import ObjectId
    if isinstance(obj, (mongoengine.Document, mongoengine.EmbeddedDocument)):
        out = dict(obj._data)
        for k, v in out.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
    elif isinstance(obj, mongoengine.queryset.QuerySet):
        out = list(obj)
    elif isinstance(obj, (list, dict)):
        out = obj
    else:
        out = dict(obj)
    return out

def route(pattern, priority = 0, domain_pattern = None):
    """ Wrap the request handler to do url route

    :param pattern: url pattern
    :param priority: the priority of url pattern
    :param domain_pattern: domain pattern
    """
    def wrap(handler):
        if not issubclass(handler, tornado.web.RequestHandler):
            raise ValueError("must be a subclass of tornado.web.RequestHandler")

        if hasattr(handler, "__routes__"):
            handler.__routes__.append((pattern, priority))
        else:
            handler.__routes__ = [(pattern, priority)]

        handler._domain_pattern = domain_pattern

        return handler

    return wrap