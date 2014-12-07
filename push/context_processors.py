#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'

import constraint

def const(request):
    return {
        'SITE_PROTOCOL': constraint.PROTOCOL,
        'SITE_HOST': constraint.HOST,
        'SITE_PORT': constraint.PORT,
    }