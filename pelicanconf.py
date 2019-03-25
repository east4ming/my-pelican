#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import logging

AUTHOR = '东风微鸣'
SITENAME = AUTHOR + " Blog"
SITETITLE = AUTHOR
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
LINKS = ()

# Social widget
SOCIAL = (('reddit', 'https://www.jianshu.com/u/0f08daeaa5a9'),
          ('linkedin', 'https://www.linkedin.com/in/凯东-崔-136128116/'),
          ('facebook', 'https://weibo.com/long5to2gf'),
          ('github', 'https://github.com/east4ming'),
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
    'extra/custom.css': {'path': 'static/custom.css'},
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

# pelican theme: Flex conf
SITEDESCRIPTION = "Focus on Python/Java/DevOps/Observability"
SITELOGO = '//s.gravatar.com/avatar/7c743bc6ac83171e35a5aa8bd66cc1ea?s=120'
FAVICON = '/favicon.ico'
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'monokai'

ROBOTS = 'index, follow'
THEME = 'Flex'
I18N_TEMPLATES_LANG = 'zh_CN'
OG_LOCALE = 'zh_CN'
MAIN_MENU = True
HOME_HIDE_TAGS = False
MENUITEMS = (('存档', '/archives/index.html'),
             ('类别', '/categories.html'),
             ('标签', '/tags.html'),
             ('作者', '/authors.html')
             )
CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}
COPYRIGHT_YEAR = 2019

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['sitemap', 'post_stats', 'i18n_subsites', 'related_posts',
           'representative_image', 'neighbors',
           'optimize_images']
# plugin related_posts
RELATED_POSTS_MAX = 5
# plugin github-corners
GITHUB_CORNER_URL = "https://github.com/east4ming"

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'monthly',
    }
}
DISQUS_SITENAME = "ewhisperblog"
ADD_THIS_ID = "ra-5c98c3e21c4def55"
# STATUSCAKE = {
#     'trackid': 'SL0UAgrsYP',
#     'days': 7,
#     'rumid': 6852,
#     'design': 6,
# }
CUSTOM_CSS = 'static/custom.css'
USE_LESS = True
# GOOGLE_ANALYTICS = ''
# GOOGLE_TAG_MANAGER = ''
# GOOGLE_ADSENSE = {}
# PIWIK_SITE_ID = ''
# PIWIK_URL = ''
ARTICLE_HIDE_TRANSLATION = True
