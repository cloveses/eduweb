#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import settings
from tornado import web, httpserver, ioloop
from mylib.url import load_handlers

# settings.web_server["static_handler_class"] = MyStaticFileHandler
handlers,domain_handlers = load_handlers(settings.HDL_DIR)

application = web.Application(handlers, **settings.web_server)
for (host_pattern, handlers) in domain_handlers:
    application.add_handlers(host_pattern, handlers)
# locale.load_gettext_translations(settings.i18n_path, settings.i18n_domain)
http_server = httpserver.HTTPServer(application, xheaders=True)
port = int(sys.argv[1]) if len(sys.argv) > 1 else settings.port
http_server.listen(port)

if __name__ == '__main__':
    ioloop.IOLoop.instance().start()
