import random
import settings
from mylib.web import BaseHandler, route
from mylib.captcha import utils
from mylib import tools
from mylib.session import session

@route(r'/captcha')
class VerifyjpegHandler(BaseHandler):

    @session
    def get(self):
        self.set_header("Content-Type", "image/jpeg")
        verifytext = self.session['verifytext']
        if verifytext and \
                    tools.make_verifytext_key(verifytext) == self.get_argument("key", ''):
            kwargs = {}
            kwargs.update(settings.CPTCH)
            kwargs.update({"text":verifytext,'font_color': random.choice(settings.INK),})
            period = random.uniform(0.11, 0.15)
            amplitude = random.uniform(3.0, 6.5)
            kwargs['distortion'] = [period, amplitude, (2.0, 0.2)]
            image = utils.gen_captcha(**kwargs)
            print(',,,,,,,,,,,,,,', image['text'])
            self.write(image['src'])
        else:
            self.redirect('/404')
