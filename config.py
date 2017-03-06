#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import sys
sys.path.append(os.curdir)

import plugins.trb
import private as private_settings

# Site information
AUTHOR = 'TRB ADC70'
SITENAME = 'Transportation Energy Committee'
SITEURL = 'http://trbenergy.org'

PATH = 'content'

TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

# Clean URLs
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'

# Theme options
THEME = 'pelican-bootstrap3'
DISPLAY_PAGES_ON_MENU = True
HIDE_SIDEBAR = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Document-relative URLs for development
RELATIVE_URLS = True

# Load the plugin for TRB committee members and presentations
PLUGINS = [plugins.trb]
TRB = private_settings.TRB


# See
# https://github.com/getpelican/pelican-themes/issues/460#issuecomment-269821765
class i18n(object):
    # looks for translations in
    # {LOCALE_DIR}/{LANGUAGE}/LC_MESSAGES/{DOMAIN}.mo
    # if not present, falls back to default

    DOMAIN = 'messages'
    LOCALE_DIR = '{THEME}/translations'
    LANGUAGES = ['de']
    NEWSTYLE = True

    __name__ = 'i18n'

    def register(self):
        from pelican.signals import generator_init
        generator_init.connect(self.install_translator)

    def install_translator(self, generator):
        import gettext
        try:
            translator = gettext.translation(
                self.DOMAIN,
                self.LOCALE_DIR.format(THEME=THEME),
                self.LANGUAGES)
        except (OSError, IOError):
            translator = gettext.NullTranslations()
        generator.env.install_gettext_translations(translator, self.NEWSTYLE)

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PLUGINS.append(i18n())
