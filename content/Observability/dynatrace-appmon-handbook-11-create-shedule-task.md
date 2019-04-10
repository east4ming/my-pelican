Title: Dynatrace AppMon 实战手册 - 11.Dynatrace创建定时任务
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十一篇, 主要是关于"定时任务"方面的功能介绍以及使用场景.

[TOC]

## 概述

Dynatrace可以设置在每隔一定时间后，执行指定的任务。

Dynatrace配置定时任务主要是在**System Profile**（系统配置文件）层面进行配置。与定时任务有关的配置项包括以下2类：

- **Schedule**（计划）：主要是与时间相关的配置。计划可以用于创建**Task** （任务）和**Monitor**（监视器）。
- **Task** （任务）：主要是具体执行的操作。如：做内存快照、线程快照、CPU采样、Session存储以及定期报告等。

## 操作步骤

### 创建月报，每月邮件发送

#### 创建计划

1. 右击指定的System Profile（系统配置文件）-> 编辑系统配置文件。可以看到编辑系统配置文件首选项，在左面版中可以找到**计划**和**任务**标签页。

2. 点击计划，默认的计划有每10min、每10s、每小时、每分钟。根据需要，创建一个**每月**的计划，每月计划细则为：从20160701 9:35开始执行，每一个月执行一次，直到永远。如下：

   ![](http://pic.yupoo.com/east4ming_v/FX9Fcrwn/vbDWA.png)

3. 下边以创建更复杂的**Every workday**来说明创建计划的具体操作。点击**创建计划...**跳出创建计划对话框。对话框分为2部分，分别为**运行计划**和**排除**，如下：

   ![](http://pic.yupoo.com/east4ming_v/FX9FczTZ/A4ZZf.png)

4. 创建或编辑**计划运行**，在对话框中可以选择**开始**、**结束**时间和**重复周期**。开始时间可以指定具体到时分秒；结束有3种方式：指定时间结束、执行一定次数后结束、永不结束。如下：

   ![](http://pic.yupoo.com/east4ming_v/FX9FcLIJ/medium.jpg)

5. 设置**重复周期**，重复周期可以选择具体的重复时间单位和具体的月份。如上图。

6. 创建**排除**。排除有3种方式：始终排除、排除时间（日期）、排除时间自-到。**Every workday**可以根据需求，始终排除1-12月的周六、周日。如下：

   ![](http://pic.yupoo.com/east4ming_v/FX9FcVKB/medium.jpg)

7. 至此，**计划**创建完毕。

#### 创建任务

1. 回到系统配置文件首选项。点击**任务**标签页。任务标签页可以对任务进行挂起和恢复以及停止。具体内容如下：

   ![](http://pic.yupoo.com/east4ming_v/FX9Fd93j/medium.jpg)

2. 可以在标签页点击**创建...**,在本页面可以创建的任务有：内存快照、CPU采样、线程快照、Session存储。注意：无法在本页面创建报告。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FX9Fdi7K/medium.jpg)

3. 如果需要创建报告任务，可以在Dynatrace客户端 -> 仪表板 -> 打开需要创建为报告的仪表板。如某系统的月报仪表板。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FX9FdrgC/FkwEk.png)

4. 在仪表板标签右击 -> 点击报告，如上图：

5. 弹出**报告创建**对话框，点击**创建计划...**，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FX9FdAUJ/medium.jpg)

6. 弹出计划报告任务对话框，主要有3个标签页可以设置：任务、计划、报告设置。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FX9FdNiy/medium.jpg)

7. **任务**标签页可以指定发送邮件，邮件接收人，主题；或者存放到本机或远程主机磁盘上。本例通过邮件发送。如上图：

8. **计划**标签页可以选择之前创建好的**Every Month**计划，计划执行于Dynatrace Server。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FX9FdPls/medium.jpg)

9. **报告设置**可以选择报告格式，支持以下格式：PDF、WORD、HTML、XML、EXCEL、CSV。这里选择HTML格式，可以直接显示在邮件里。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FX9FdWZP/medium.jpg)

10. 在**高级** -> **详细信息** 中可以进行更多细节设置。如下图：

    ![](http://pic.yupoo.com/east4ming_v/FX9Fe8zz/medium.jpg)

11. 可以自定义logo、显示行数、显示的仪表图。如下图：

    ![](http://pic.yupoo.com/east4ming_v/FX9Fecyh/medium.jpg)

12. 配置完成后**运行计划**，运行后月报效果如下：

    ![](http://pic.yupoo.com/east4ming_v/FX9FejjI/medium.jpg)

13. 至此，Dynatrace创建定时任务--月报全部完成。
