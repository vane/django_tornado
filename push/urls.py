#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'

from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
)