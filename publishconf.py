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

# DISQUS_SITENAME = ""
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
