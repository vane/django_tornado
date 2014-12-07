#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'

from django.conf.urls import patterns, url
import views
from view import chat
from pusher import PushClientStore

PushClientStore.register('chat', chat.ChatStorage.callback)


urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^chat/msg/$', chat.message_POST),
   url(r'^chat/enter/$', chat.enter_POST),
   url(r'^chat/users/get/$', chat.users_GET),
   url(r'^chat/msg/get/$', chat.last_message_GET),
   url(r'^chat/nick/check/$', chat.check_nick_POST),
)