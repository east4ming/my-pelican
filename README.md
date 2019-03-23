# my-pelican
My blog with pelican.

[TOC]

## TODO

- [x] 创建2篇 `article` (web框架开发的文章)
  - [x] 添加`images`文件夹放图片, 并链接静态文件-图片
  - [x] 站内链接
  - [x] Category 暂定为文件夹`python`
  - [x] 包含所有元数据关键字.
- [ ] 添加备案相关链接 - DOING
- [x] 配置`pelicanconf.py` `publishconf.py` 优化
- [x] articles合并
- [x] 新增pages, 包括: about, contact, 404, 50X等
- [x] 调整pelican `tasks.py` `Makefile`, 如发布方式等
- [x] 生产发布
- [ ] 配置ssl
- [ ] 选择并安装插件. 如: 图片插件等
- [ ] 选择并安装主题, 如: 大小屏适配, 淡雅主题.
- [ ] 创建content批量倒入工具

## Feature

### init-articles

- [x] BUG: `Docutils has no localization for 'chinese (simplified)'. Using 'en' instead.` 
- [ ] BUG: 图片按原尺寸显示, 未自动缩放.
- [x] 优化: `周五 01 三月 2019` 显示方式不好, 应调整为: `2019年3月1日 周五 14:44`或者`2019-03-01 14:44`
- [ ] 优化: 中文字体优化
- [x] 优化: 显示emoji
- [x] BUG: 不支持`[TOC]`

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

- [x] 行号宽度显示错乱 - 删除行号配置

### add-pages

1. 增加 about 页面 - 增加支付宝付款码和weixin赞赏码
2. 增加 contact 页面
3. 增加 404 页面
4. 增加 50X 页面
5. social 增加 LinkedIn 链接: https://www.linkedin.com/in/%E5%87%AF%E4%B8%9C-%E5%B4%94-136128116/

#### Bugs

- [ ] LinkedIn 自带有图标, 而国内网站没有. 导致显示错位

### optimize-publish-scripts

1. 优化`tasks.py`文件. 通过`rsync` local方式同步; (不压缩, 通过`sudo`执行)
2. 调整`Makefile`文件.
3. 调整`publishconf.py`:
   1. 导入`pelicanconf.py`的配置
   2. rss配置: 类别和tag加上前置单词, 避免冲突, rss包括全部文章内容

> :notebook: 备注:
>
> ```bash
> sudo rsync -pthrvc --cvs-exclude --delete
> -p --perms：保持perms属性(权限，不包括特殊权限)。
> -t --times：保持mtime属性。强烈建议任何时候都加上"-t"，否则目标文件mtime会设置为系统时间，导致下次更新检查出mtime不同从而导致增量传输无效。
> -h, --human-readable        以人类可读方式输出信息。
> -r, --recursive             以递归模式拷贝目录
> -v, --verbose               输出rsync daemon启动时的详细信息
> -c, --checksum              改变了rsync检查文件改变和决定是否要传输的方式. 使用该选项，将对每个匹配了大小的文件比较128位的校验码。
> --delete                删除receiver端有而sender端没有的文件，但不是删除receiver端所有文件，而是只对将要同步的目录生效
> ```
>

## Releases

### 0.1.0

- Inital my pelican blog
- Create 3 md articles, mod internal content link
- Mod pelicanconf and articles' metadata
- Add images in articles

### 0.2.0

- 正式对外发布我的博客

#### 内容

- 包括3个类别: python, java和可观察性
- 包括2个pages: About 和 Contact
- 可以通过[rss feed](http://www.ewhisper.cn/feeds/all.rss.xml)订阅

#### 功能

- markdown编写
   - 支持toc
   - 支持emoji
- 添加 faviron
- 添加 robots.txt
- 添加 404页面
- 添加 jianshu weibo linkedin 个人主页链接

## Hotfix

### docutils localization

- Change `DEFAULT_LANG = 'zh_CN'`
