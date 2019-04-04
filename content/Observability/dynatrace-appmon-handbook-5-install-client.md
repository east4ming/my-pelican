Title: Dynatrace AppMon 实战手册 - 5.Dynatrace 客户端安装
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第五篇, 主要是Dynatrace各种客户端的安装, 包括富客户端和web端.

[TOC]

## 1 Dynatrace客户端类型简介

Dynatrace有3种类型的客户端：

- 网页端
- WebStart客户端
- 富客户端

三者有以下区别：

**网页端**：

- 通过浏览器（最新版本IE/Firefox/Chrome等）访问
- 默认端口：9911（HTTPS）
- 具有基本的监控功能（包括仪表板、应用、运维的基本监控信息），进一步分析需要跳转到后两种客户端执行

**WebStart客户端**

- 需要JRE/JDK  7/8支持
- 需要通过网页下载一个jnlp文件并打开
- 具有完整的监控分析功能（与富客户端功能相同）
- 支持32位、64位系统
- 支持的系统取决于JRE/JDK所支持的系统

**富客户端**

- 为安装包或绿色压缩包
- 只支持64位系统

## 2 Web 客户端安装

1. 访问IP地址：[https://10.100.61.171:9911](https://10.100.61.171:9911),并继续浏览。如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVynxlr/medium.jpg)

2. 跳转到Dynatrace Web登录页，输入自己的账号密码，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVynKLL/medium.jpg)

3. 登录后跳转到Dynatrace首页，最上从左到右依次为：（如下图）

   1. 菜单
   2. 仪表板
   3. 筛选应用
   4. 筛选时间范围
   5. 分享
   6. 用户信息

   ![](http://pic.yupoo.com/east4ming_v/GeVyu6tA/medium.jpg)

4. 日常使用的相关菜单及说明如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVyCwo8/medium.jpg)

## 3 WebStart客户端安装（推荐32位系统安装）

1. 下载并安装JRE/JDK 7/8，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVyD3Kn/medium.jpg)

   ![](http://pic.yupoo.com/east4ming_v/GeVyCVEm/medium.jpg)

2. 浏览器访问Dynatrace Server IP：[https://10.100.61.171:8021](https://10.100.61.171:8021),如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVyDEFL/medium.jpg)

3. 访问后跳转到首页，点击**Webstart客户端**，会下载一个client.jnlp文件。如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVyGvZ8/medium.jpg)

4. 打开client.jnlp文件，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVyTbtC/medium.jpg)

5. 忽略告警并继续，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVyTEQ2/medium.jpg)

6. 之后会自动下载WebStart客户端，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVyV7rn/medium.jpg)

7. 之后会自动启动，忽略告警并继续，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVyWtVK/medium.jpg)

8. WebStart客户端的界面显示，输入账号密码，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz0xXl/medium.jpg)

9. WebStart的界面展示如下：

   ![](http://pic.yupoo.com/east4ming_v/GeVz1NOi/pFI7J.jpg)

## 4 富客户端安装（仅适用64位系统）

1. 安装包包括苹果OS安装包、windows安装包及绿色解压版、linux版（jar包）如下图所示：

   ![](http://pic.yupoo.com/east4ming_v/GeVz8tVT/medium.jpg)

2. 下面以windows安装包为例（windows压缩包直接解压使用），点击安装包运行，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz2dG3/medium.jpg)

3. 接受协议，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz2Ruw/medium.jpg)

4. 选择路径，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz3f0G/medium.jpg)

5. 安装开始，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz3JQe/medium.jpg)

6. 安装完成，运行客户端，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz47sp/medium.jpg)

7. 填入IP+端口、账号密码，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz4RqZ/medium.jpg)

8. 登录后会提示升级客户端，点击'YES'并继续，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz5flw/medium.jpg)

9. 下载升级包，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz5sTF/medium.jpg)

10. 升级后需重启客户端，如下图：

    ![](http://pic.yupoo.com/east4ming_v/GeVz5SVf/medium.jpg)

11. 重启后会提示选择**语言**，根据需要选择中文或英文，如下图：

    ![](http://pic.yupoo.com/east4ming_v/GeVz6OMI/medium.jpg)

12. 跳转到首界面，界面简介如下图：

    ![](http://pic.yupoo.com/east4ming_v/GeVz7qPQ/12Mkk2.jpg)

## 5 Web端和客户端（WebStart 富客户端）联动

Web端无法深入分析，可以在分析指定事务的时候，直接点击**OPEN IN CLIENT** 后在WebStart或富客户端中进行分析。具体操作如下：

1. 在Web端分析具体的事务，需要深入分析，点击**OPEN IN CLIENT**如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz7I3h/cFcZZ.jpg)

2. 首次因为https信任会失败，接受告警后再次点击会跳出客户端，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GeVz8dUA/FePWL.jpg)
