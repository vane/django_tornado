#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'

from django.http import HttpResponse
from pusher import PushClientStore, PUSH_ID_NAME
import utils
import pytz
import datetime

class ChatStorage():
    chat_nicks = {}
    chat_message = []
    @classmethod
    def callback(self, data):
        if data['action'] == 'add':
            pass
        elif data['action'] == 'del':
            client = data['client']
            if self.chat_nicks.has_key(client.channel):
                nick = self.chat_nicks[client.channel]
                del self.chat_nicks[client.channel]
                PushClientStore.broadcast_all(_construct_message('ch_usr_del', nick))

    @classmethod
    def add_nick(self, id, user):
        self.chat_nicks[id] = user

    @classmethod
    def get_nick(self, id):
        return self.chat_nicks[id]

    @classmethod
    def add_message(self, msg):
        if len(self.chat_message) > 10:
            self.chat_message.pop()
        self.chat_message.append(msg)


def _construct_message(type, msg):
    data = {
        'type':type,
        'data':msg
    }
    return utils.tojson(data)

def users_GET(request):
    return HttpResponse(_construct_message('ch_usr', ChatStorage.chat_nicks.values()))

def last_message_GET(request):
    return HttpResponse(_construct_message('ch_last_msg', ChatStorage.chat_message))

def check_nick_POST(request):
    if request.method == "POST":
        nick = request.POST.get('nick')
        result = nick in ChatStorage.chat_nicks.values()
        return HttpResponse(_construct_message('ch_nick_check', result))
    return HttpResponse(_construct_message('err', 'POST_ONLY'))

def enter_POST(request):
    if request.method == "POST":
        nick = request.POST.get('nick')
        channel = request.session.get(PUSH_ID_NAME)
        if channel is not None:
            PushClientStore.user_msg(_construct_message('ch_usr', ChatStorage.chat_nicks.values()), channel)
            PushClientStore.user_msg(_construct_message('ch_last_msg', ChatStorage.chat_message), channel)
            PushClientStore.broadcast_all(_construct_message('ch_usr_new', nick))
            ChatStorage.add_nick(channel, nick)
            return HttpResponse(_construct_message('res', 'OK'))
        return HttpResponse(_construct_message('err', 'PUSH_NULL'))
    return HttpResponse(_construct_message('err', 'POST_ONLY'))

def message_POST(request):
    if request.method == "POST":
        msg = request.POST.get('msg')
        channel = request.session.get(PUSH_ID_NAME)
        nick = ChatStorage.get_nick(channel)
        data = {
            'date':datetime.datetime.now(tz=pytz.UTC),
            'usr':nick,
            'msg':msg,
        }
        ChatStorage.add_message(data)
        PushClientStore.broadcast_all(_construct_message('ch_msg', data))
        return HttpResponse(_construct_message('res', 'OK'))
    return HttpResponse(_construct_message('err', 'POST_ONLY'))