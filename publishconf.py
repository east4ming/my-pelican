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
SITEURL = 'https://www.EWhisper.cn'
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "ewhisperblog"
GOOGLE_ANALYTICS = "UA-136986082-1"

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
STATUSCAKE = {
    'trackid': 'CbJdcjmnCx',
    'days': 7,
    'design': 7,
}
GOOGLE_TAG_MANAGER = 'GTM-T9334L3'
GOOGLE_ADSENSE = {
    'ca_id': 'ca-pub-2290120018010607',    # Your AdSense ID
    'page_level_ads': True,          # Allow Page Level Ads (mobile)
    'ads': {
        'aside': '',          # Side bar banner (all pages)
        'main_menu': '',      # Banner before main menu (all pages)
        'index_top': '',      # Banner after main menu (index only)
        'index_bottom': '',   # Banner before footer (index only)
        'article_top': '',    # Banner after article title (article only)
        'article_bottom': '', # Banner after article content (article only)
    }
}
GUAGES = '5c9a5706a2f54b13557a67d0'
