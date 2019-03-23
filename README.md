# my-pelican
My blog with pelican.

## TODO

1. ~~创建2篇 `article` (web框架开发的文章)~~
   1. ~~添加`images`文件夹放图片, 并链接静态文件-图片~~
   2. ~~站内链接~~
   3. ~~Category 暂定为文件夹`python`~~
   4. ~~包含所有元数据关键字.~~
2. 创建2个`pages`:
   1. About
   2. Contact
3. 通过脚本导入已有内容
4. 添加备案相关链接 - DOING
5. ~~`pelicanconf.py` `publishconf.py` 配置优化 ~~
6. ~~articles合并~~
7. 新增pages, 包括: about, contact, 404, 50X等
8. 调整pelican `tasks.py` `Makefile`, 如发布方式等
9. 生产发布
10. 配置ssl
11. 选择并安装插件. 如: 图片插件等
12. 选择并安装主题, 如: 大小屏适配, 淡雅主题.
13. 创建content批量倒入工具

## Feature

### init-articles

- ~~BUG: `Docutils has no localization for 'chinese (simplified)'. Using 'en' instead.` ~~
- BUG: 图片按原尺寸显示, 未自动缩放.
- 优化: `周五 01 三月 2019` 显示方式不好, 应调整为: `2019年3月1日 周五 14:44`或者`2019-03-01 14:44`
- 优化: 中文字体优化
- 优化: 显示emoji
- BUG: 不支持`[TOC]`

### beian-links

- 20190320: TODO

### conf-optimazation

1. 调整`pelicanconf.py`
2. 调整`publishconf.py`
3. 增加 emoji 包
4. 增加`robots.txt` `faviron`

#### 具体调整内容

1. 添加`SITESUBTITLE`
2. `SOCIAL` 添加 weibo和简书
3. `LOAD_CONTENT_CACHE`: `pelicanconf.py` 为`False`, `publishconf.py`为`True`
4. `RELATIVE_URLS`: `pelicanconf.py` 为`True`, `publishconf.py`为`False`
5. github
6. `USE_FOLDER_AS_CATEGORY = True`
7. `OUTPUT_RETENTION = [".git", ".idea"]`
8. `LOG_FILTER`
9. `MARKDOWN`:
   1. `markdown.extensions.codehilite` 增加行号;
   2. `markdown.extensions.extra`: 增加footnotes和fenced_code;
   3. 启用toc功能
   4. 启用emoji功能
      1. `pipenv`安装`pymdown-extensions`
      2. `pelicanconf`增加`import  pymdownx.emoji`
      3. 增加配置`pymdownx.emoji`
10. `publishconf.py`导入`pelicanconf.py`配置.
11. `STATIC_PATHS` 加入`assets`
12. `SLUGIFY_SOURCE` 使用文章的文件名
13. `publishconf.py`修改:`CACHE_CONTENT = True` (默认为False)
14. 增加年度/月度存档
15. 修改默认存档的`SAVE_AS`
16. 修改默认日期格式为:`%Y-%m-%d %A`
17. 添加`DATE_FORMATS`
18. 添加`LOCALE`
19. 添加`faviron.ico`
20. 添加`robots.txt`
21. 添加 feed conf: 禁用atom feed, 启用rss feed
   1. `FEED_DOMAIN`
   2. `FEED_RSS`
   3. `FEED_ALL_RSS`
   4. `CATEGORY_FEED_RSS`
   5. `AUTHOR_FEED_RSS`
   6.`TAG_FEED_RSS`
   7. `RSS_FEED_SUMMARY_ONLY`

#### Bugs

1. 行号宽度显示错乱(可能跟: `fenced_code` 或 `linenums`有关)

### add-pages

1. 增加 about 页面
2. 增加 contact 页面
3. 增加 404 页面
4. 增加 50X 页面
5. social 增加 LinkedIn 链接: https://www.linkedin.com/in/%E5%87%AF%E4%B8%9C-%E5%B4%94-136128116/

#### TODO

1. 增加支付宝付款码
2. 调整 about contact位置到最后


## Releases

### 0.1.0

- Inital my pelican blog
- Create 3 md articles, mod internal content link
- Mod pelicanconf and articles' metadata
- Add images in articles

## Hotfix

### docutils localization

- Change `DEFAULT_LANG = 'zh_CN'`
