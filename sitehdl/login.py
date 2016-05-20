# -*- coding: utf-8 -*-

import random
import settings
from mylib.web import BaseHandler, route
from mylib.captcha import utils
from mylib.session import session
from mylib import tools
from db import controls

@route('/login')
class IndexHdl(BaseHandler):
    @session
    def get(self):
        vf_txt,v_key = self.gen_verify_text()
        self.session['verifytext'] = vf_txt
        if self.current_user:
            self.redirect('/')
            return
        self.render('login.html',{"v_key":v_key,"hint_info":self.hint_info})

    @session
    def post(self):
        name = self.get_argument('name','').strip()
        passwd = self.get_argument('passwd','').strip()
        action = self.get_argument('action','')
        vf_txt = self.get_argument('vf_txt','').strip()
        vf_txt_session = self.session['verifytext']
        self.session['verifytext'] = ''
        if vf_txt and vf_txt_session and vf_txt.lower() == vf_txt_session.lower():
            if passwd:
                if action=='login':
                    self.login(name,passwd)
                elif action == 'sign':
                    self.sign(name,passwd)
                else:
                    self.set_secure_cookie('info','Submit data error! ')
                    self.redirect('/login')
            else:
                self.set_secure_cookie('info','Password can not be empty! ')
                self.redirect('/login')
        else:
            self.set_secure_cookie('info','Verify text is error! ')
            self.redirect('/login')

    @session
    def login(self,name,passwd):
        user = controls.get_user(name,passwd)
        if user:
            self.set_secure_cookie('name',user.name)
            self.session['name'] = tools.make_verifytext_key(user.name)
        self.redirect('/')

    @session
    def sign(self,name,passwd):
        user = controls.add_user(name,passwd)
        if user:
            self.set_secure_cookie('name',user.name)
            self.session['name'] = tools.make_verifytext_key(user.name)
        self.redirect('/')


    def gen_verify_text(self):
        verifytext = utils.getstr(
            random.choice(settings.CPTCH_STR['cpth_len']),
            random.choice(settings.CPTCH_STR['cpth_type']),
            settings.CPTCH_STR['filte_char'])
        v_key = tools.make_verifytext_key(verifytext)
        return verifytext,v_key

@route('/logout')
class LogoutHdl(BaseHandler):

    @session
    def get(self):
        self.set_secure_cookie('name','')
        self.session['name'] = ''
        self.redirect('/')