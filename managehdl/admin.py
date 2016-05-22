# -*- coding: utf-8 -*-

import os
import settings
from mylib.web import BaseHandler, route
from db import controls

@route('/admin')
class AdminHdl(BaseHandler):

    def get(self):
        if self.current_user != 'superadmn':
            self.set_secure_cookie('info','Please login as superadmin!')
            self.redirect('/')
            return

        name = self.get_argument('name','')
        if name:
            info = controls.del_user(name)
            if info:
                self.set_secure_cookie('info','User %s already has been remove!' % name)

        pname = self.get_argument('pname','')
        if pname:
            controls.chn_status(pname)

        all_user = controls.get_all_user()
        all_proj = controls.get_all_pro()
        paras = {"hint_info":self.hint_info,
        'all_user':all_user,
        'all_proj':all_proj}
        self.render('admin.html',paras)

    def post(self):
        if self.current_user != 'superadmn':
            self.set_secure_cookie('info','Please login as superadmin!')
            self.redirect('/')
            return
        name = self.get_argument('name','',strip=True)
        url = self.get_argument('url','',strip=True)
        if name and url:
            controls.add_proname(name,url)
        self.redirect('/admin')
        # self.write('abc')