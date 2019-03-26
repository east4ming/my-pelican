#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'http://www.EWhisper.cn'
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "ewhisperblog"
# GOOGLE_ANALYTICS = ""

# my publish conf
LOAD_CONTENT_CACHE = True
CACHE_CONTENT = True

# feed conf
FEED_DOMAIN = SITEURL
# FEED_RSS = 'feeds/'
FEED_ALL_ATOM = None
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = 'feeds/category.{slug}.rss.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = 'feeds/{slug}.rss.xml'
TAG_FEED_RSS = 'feeds/tag.{slug}.rss.xml'
RSS_FEED_SUMMARY_ONLY = False

# theme: Flex
USE_LESS = False
ROBOTS = 'index, follow'
ADD_THIS_ID = "ra-5c98c3e21c4def55"
# STATUSCAKE = {
#     'trackid': 'SL0UAgrsYP',
#     'days': 7,
#     'rumid': 6852,
#     'design': 6,
# }
GOOGLE_TAG_MANAGER = 'T9334L3'
GOOGLE_ADSENSE = {
    'ca_id': 'ca-pub-2290120018010607',    # Your AdSense ID
    'page_level_ads': True,          # Allow Page Level Ads (mobile)
    'ads': {
        'aside': '1234561',          # Side bar banner (all pages)
        'main_menu': '1234562',      # Banner before main menu (all pages)
        'index_top': '1234563',      # Banner after main menu (index only)
        'index_bottom': '1234564',   # Banner before footer (index only)
        'article_top': '1234565',    # Banner after article title (article only)
        'article_bottom': '1234566', # Banner after article content (article only)
    }
}
# PIWIK_SITE_ID = ''
# PIWIK_URL = ''
