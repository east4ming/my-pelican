#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import logging

AUTHOR = '东风微鸣'
SITENAME = '东风微鸣 Blog'
SITESUBTITLE = "Focus on Python/Java/DevOps/Observability"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh_CN'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('<img src="/images/favicon-jianshu.ico" width="16" height="16"> 简书',
           'https://www.jianshu.com/u/0f08daeaa5a9'),
          ('<img src="/images/favicon-weibo.ico" width="16" height="16"> '
           '微博', 'https://weibo.com/long5to2gf'),
          ('<img src="/images/favicon-linkedin.ico" width="16" height="16"> '
           '领英', 'https://www.linkedin.com/in/%E5%87%AF%E4%B8%9C-%E5%B4'
                       '%94'
                '-136128116/'),
          )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# my-pelican conf

# base conf
DEFAULT_DATE = 'fs'
SUMMARY_MAX_LENGTH = 100
# FILENAME_METADATA = '(?P<slug>.*)'  # SLUGIFY_SOURCE 已配置
LOAD_CONTENT_CACHE = False
GITHUB_URL = "https://github.com/east4ming"
USE_FOLDER_AS_CATEGORY = True
OUTPUT_RETENTION = [".git", ".idea"]
LOG_FILTER = [(logging.WARN, 'TAG_SAVE_AS is set to False'),
              (logging.WARN, 'Empty alt attribute for image %s in %s'),
              ]
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            # 'linenums': True,
        },
        'markdown.extensions.extra': {
            'markdown.extensions.footnotes': {},
            'markdown.extensions.fenced_code': {},
        },
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {
            # 'anchorlink': True,
            'permalink': True,
            'toc_depth': 3,
        },
        "pymdownx.emoji": {
            "options": {
                "attributes": {
                    "align": "absmiddle",
                    "height": "20px",
                    "width": "20px"
                },
            },
        },
    },
    'output_format': 'html5',
}
STATIC_PATHS = ['images',
                'assets',
                ]
EXTRA_PATH_METADATA = {
    'assets/robots.txt': {'path': 'robots.txt'},
    'assets/favicon.ico': {'path': 'favicon.ico'},
}
SLUGIFY_SOURCE = 'basename'

# URL conf
YEAR_ARCHIVE_URL = 'archives/{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = 'archives/{date:%Y}/index.html'
MONTH_ARCHIVE_URL = 'archives/{date:%Y}/{date:%m}/'
MONTH_ARCHIVE_SAVE_AS = 'archives/{date:%Y}/{date:%m}/index.html'
ARCHIVES_SAVE_AS = 'archives/index.html'

# time date conf
DEFAULT_DATE_FORMAT = '%Y-%m-%d %A'
DATE_FORMATS = {
    'en': ('en_US', '%a, %d %b %Y'),
    'cn': ('zh_CN', '%Y-%m-%d %A'),
}
LOCALE = ('en_US.utf8', 'zh_CN.utf8')

# content order
PAGE_ORDER_BY = 'basename'
