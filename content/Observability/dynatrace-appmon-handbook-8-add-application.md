Title: Dynatrace AppMon 实战手册 - 8.Dynatrace新增主机组&添加应用程序定义
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第八篇, 主要是2部分内容, 1是添加主机组, 用以批量配置主机监控, 2是添加应用程序, 用以按应用监控.

[TOC]

## 新增主机组

▽ 编辑系统配置文件--基础结构--创建
![基础结构](./images/appmon-add-application-1.png)

▽ 输入主机组名称
![主机组](./images/appmon-add-application-2.png)

▽ 根据主机hostname，添加主机组映射关系：有多重语法，“包含”、“开头为”、“结尾
为”等等。
![主机名规则](./images/appmon-add-application-3.png)

▽ 设置主机的告警阈值
![主机告警阈值](./images/appmon-add-application-4.png)

## 应用程序定义

▽ 编辑系统配置文件--应用程序--创建
![创建应用程序](./images/appmon-add-application-5.png)

▽ 添加应用程序的匹配关系：可以包含应用实例所在主机的IP、应用程序域名等。
![应用程序匹配规则](./images/appmon-add-application-6.png)

配置完成后, 还要查看监控面板，如果发现仍有一些URI没有纳入到自定义的应用程序监控，可以查看web请
求，进行全面的纳入。

▽ 系统配置文件--web请求--右键更多：
![web请求](./images/appmon-add-application-7.png)

▽ 根据“源”编辑筛选：
![筛选](./images/appmon-add-application-8.png)

▽ 应用程序条目筛选：
![条目筛选](./images/appmon-add-application-9.png)

▽ 将未包含的URI全部加入到定义的应用程序中：
![添加](./images/appmon-add-application-10.png)

▽ 查看监控面板，直到Default Application监控信息为空、以及不再出现其他未纳入的URI为止。
![default](./images/appmon-add-application-11.png)
