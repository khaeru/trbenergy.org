#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import sys

sys.path.append(os.curdir)

import private as private_settings  # noqa: E402

# Site information
AUTHOR = "TRB AMS30"
SITENAME = "Transportation Energy Committee"
SITEURL = "https://trbenergy.org"

PATH = "content"

TIMEZONE = "America/New_York"
DEFAULT_LANG = "en"

# Clean URLs
ARTICLE_URL = "news/{date:%Y}-{date:%m}-{date:%d}"
ARTICLE_SAVE_AS = "news/{date:%Y}-{date:%m}-{date:%d}/index.html"
INDEX_SAVE_AS = "news/index.html"
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}/index.html"

# Theme options
THEME = "pelican-bootstrap3"
DISPLAY_PAGES_ON_MENU = True
HIDE_SIDEBAR = True


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Document-relative URLs for development
RELATIVE_URLS = True

# Load the plugin for TRB committee members and presentations
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["trb"]
TRB = private_settings.TRB

# See https://github.com/getpelican/pelican-themes/issues/460
JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.i18n"]}
PLUGIN_PATHS.append("../other/pelican-plugins")
PLUGINS.append("i18n_subsites")

STATIC_PATHS = ["extra"]
EXTRA_PATH_METADATA = {
    "extra/htaccess": {"path": ".htaccess"},
}
