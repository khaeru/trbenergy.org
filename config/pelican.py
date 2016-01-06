#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import private

AUTHOR = 'TRB/ADC70'
SITENAME = 'Transportation Energy Committee'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['pdf']

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

THEME = 'pelican-bootstrap3'
DISPLAY_PAGES_ON_MENU = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins']
PLUGINS = ['data']

DATA_WB_KEY = private.DATA_WB_KEY
GOOGLE_EMAIL = private.GOOGLE_EMAIL
GOOGLE_PW = private.GOOGLE_PW
