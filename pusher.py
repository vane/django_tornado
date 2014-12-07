#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'
from django.conf import settings
from django.utils.importlib import import_module

from sockjs.tornado import SockJSConnection
from threading import Thread
import utils
import time,pytz,datetime,json

import logging

class PushClientStore():
    clients = {}
    ids_channel = {}

    @classmethod
    def add_client(self, client):
        self.clients[client.channel] = client
        if client.user.is_authenticated():
            self.ids_channel[client.user.id] = client.channel
            return True
        return False

    @classmethod
    def del_client(self, client):
        if self.clients.has_key(client.channel):
            if client.user.is_authenticated():
                del self.ids_channel[client.user.id]
            del self.clients[client.channel]
            return True
        return False

    @classmethod
    def broadcast_all(self, msg):
        for client in self.clients.values():
            client.send(msg)

    @classmethod
    def broadcast_auth(self, msg):
        for client in self.clients.values():
            if client.user.is_authenticated():
                client.send(msg)

    @classmethod
    def user_auth(self, user, msg):
        if self.ids_channel.has_key(user.id):
            channel = self.ids_channel[user.id]
            client = self.clients[channel]
            if client.user.is_authenticated():
                client.send(msg)

    @classmethod
    def user_msg(self, msg, channel):
        if self.clients.has_key(channel):
            client = self.clients[channel]
            client.send(msg)

class Pinger():

    def start(self):
        def sendPing():
            while True:
                time.sleep(1)
                #print "try send : %d" % self.i
                data = {
                    'type':'test',
                    'data':datetime.datetime.now(tz=pytz.UTC)
                }
                PushClientStore.broadcast_all(utils.tojson(data))
        t = Thread(target=sendPing)
        t.start()


class PushClient(SockJSConnection):

    def error(self, message, error_type=None):
        """
        send some error
        """
        return self.send(utils.tojson({
            'error': error_type,
            'msg': message,
            }))

    def get_session_key(self, request):
        """
        get session key - django sets it as Set-Cookie: sessionid={session}
        so we need to ensure the key is correct ;)
        """
        session_key = request.cookies.get(settings.SESSION_COOKIE_NAME, None)
        temp = str(session_key).split("sessionid=")
        if len(temp) == 2:
            session_key = temp[1]
        return session_key

    def get_session_store(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = self.get_session_key(request)
        return engine.SessionStore(session_key)

    def on_open(self, request):
        """
        get django user based on session
        """
        from django.contrib import auth as user_auth
        session = self.get_session_store(request)
        request.session = session
        self.user = user_auth.get_user(request)
        self.channel = self.session.session_id
        PushClientStore.add_client(self)
        logging.debug("open channel : %s" % self.channel)

    def on_message(self, msg):
        """
        handle messages
        """
        logging.debug("msg")
        try:
            message = json.loads(msg)
        except ValueError:
            self.error("Invalid JSON")
            return
        self.error("Invalid data type %s" % message['type'])
        logging.debug("Invalid data type %s" % message['type'])

    def on_close(self):
        """
        Remove client from store
        """
        logging.debug("close : %s" % self.channel)
        PushClientStore.del_client(self)
        return super(PushClient, self).on_close()
