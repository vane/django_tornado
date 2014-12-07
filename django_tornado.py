#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'

import os
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

import sockjs.tornado

from django.core.handlers import wsgi

import pusher
import constraint

import logging as _


SETTINGS_PATH="django_tornado.settings"


_H = _.StreamHandler()
_F = _.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging = _.getLogger('')
logging.setLevel(_.DEBUG)
logging.addHandler(_H)
_H.setFormatter(_F)

def main():

    wsgi_app = tornado.wsgi.WSGIContainer(wsgi.WSGIHandler())

    Router = sockjs.tornado.SockJSRouter(pusher.PushClient, '/stream')
    Router.urls.append((r'/static/(.*)$', tornado.web.StaticFileHandler, {'path': './static'}))
    Router.urls.append(('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)))
    logging.debug("start")

    ping = pusher.Pinger()
    ping.start()
    tornado_app  = tornado.web.Application(Router.urls)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(address=constraint.HOST, port=constraint.PORT)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_PATH)
    main()
