# -*- coding: utf-8 -*-

from mylib.web import BaseHandler, route

@route('/404')
class NotFndHdl(BaseHandler):
    def get(self):
        self.write('404')