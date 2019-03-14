# my-pelican
My blog with pelican.

## TODO

1. 创建2篇 `article` (web框架开发的文章)
   1. 添加`images`文件夹放图片, 并链接静态文件-图片
   2. 站内链接
   3. Category 暂定为文件夹`python`
   4. 包含所有元数据关键字.
2. 创建2个`pages`:
   1. About
   2. Contact
3. 通过脚本导入已有内容
4. 添加备案相关链接

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

## Releases

### 0.1.0

- Inital my pelican blog
- Create 3 md articles, mod internal content link
- Mod pelicanconf and articles' metadata
- Add images in articles

## Hotfix

### docutils localization

- Change `DEFAULT_LANG = 'zh_CN'`
