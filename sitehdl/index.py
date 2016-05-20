# -*- coding: utf-8 -*-

import os
import settings
from mylib.web import BaseHandler, route
from mylib.myxltools import verify

@route('/')
class IndexHdl(BaseHandler):
    def get(self):
        self.render('index.html',{"hint_info":self.hint_info,
            "upload_max_size":settings.UPLOAD_MAX_SIZE })

    def post(self):
        # print('recieve file.')
        if self.request.files['myfile']:
            myfile = self.request.files['myfile'][0]
            name = myfile.filename
            # mypath = os.path.join(settings.UPLOAD_DIR,self.current_user)
            mypath = settings.UPLOAD_DIR
            if not os.path.exists(mypath):
                os.makedirs(mypath)
            name = os.path.join(mypath,name)
            if os.path.exists(name):
                nm,ext = os.path.splitext(name)
                name = ''.join((name,'1',ext))
            with open(name,'wb') as f:
                f.write(myfile.body)
            info = verify.verify_file(filename,settings.filters,settings.limits,settings.ncols)
            if info:
                os.remove(name)
                info = '数据有误，请重新上传！\n' + info
                self.write(info)
            else:
                self.write('上传成功！')
