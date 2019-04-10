Title: Dynatrace AppMon 实战手册 - 14.Dynatrace创建Server-side业务分析
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十四篇, AppMon的一个很强大的功能就是"业务分析", 在AppMon中, 可以通过不同的数据来源(浏览器端, app端, server端)来创建业务分析, 本次主要介绍如何创建 Server-side 业务分析.

## 概述

业务分析（**Business Transaction**）可以经过对应用的分析来跟踪一些特殊的交易（如：登陆和购买）。例如，你可以跟踪某应用特定用户群的登陆操作响应时间。业务分析包含过滤方法来检查指定的用户标签的出现（如：一个标记过的web请求测量）。默认会计算响应时间和计数。拆分方法默认是**应用**。

针对Dynatrace的业务分析又可以根据数据来源的不同，细分为以下几类：

- 基于Server端数据的业务分析
- 基于UEM用户访问数据的业务分析
- 基于UEM用户行为数据的业务分析

本次将介绍如何创建Server-side业务分析。

## 案例介绍

客户发现人寿显示影像资料频繁告警相应缓慢。怀疑与用户和具体的IP有关，希望创建针对**显示影像**这一业务，按照用户名和IP地址进行拆分过滤。以进一步分析。

## 操作步骤

> :notebook:备注:
> 推荐使用**第一个**而不是**最后一个**来作为业务分析的筛选条件。
> 这2者的主要区别是：如果PurePath树很长的话，最后一个将导致每个方法都会查看一遍，如果是第一个，就只看第一个节点就行了
> 所以**第一个**作为筛选条件效率会高很多。

操作步骤分解：

- 创建特定业务的**测量（measure）** -- *1-4步*
- 创建作为过滤条件的**测量**--客户端IP、用户名 -- *5-7步*
- 创建**业务分析** --  *8-11步*

1. 进入指定系统配置文件的**编辑系统配置文件**菜单，在左面板找到**测量**标签，如下：

   ![](http://pic.yupoo.com/east4ming_v/FXkeeeHe/sgCJu.jpg)

2. 点击**创建测量...** ，这里需要按照**URI模式值**进行创建。如上图：

3. 跳出创建新测量对话框，可以通过ctrl+f 直接查找关键字（在任何列表类界面都可以搜索） -> 点击**web请求 - URI模式值**，需要根据实际需求填写：名称、URI模式和值、拆分等内容。如下：

   ![](http://pic.yupoo.com/east4ming_v/FXkeeyWo/2g7eJ.jpg)

4. 配置好的**显示影像**（showimage）的测量如下，并点击**确定** ：

   ![](http://pic.yupoo.com/east4ming_v/FXkeeWmD/x6wu1.jpg)

5. 再次点击**创建测量...**,查找并选择**Web请求 - 客户端IP**，并点击**添加**，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXkef6xe/SGhyA.jpg)

6. 再次点击**创建测量...**,查找并选择**Web请求 - 会话属性值** ，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXkefgJ3/mTATJ.jpg)

7. 并进行详细的配置，配置可以抓取到用户名的**会话属性**，本例中的会话属性为：**lifeuser.getUserName()**。关于具体的会话属性，可以询问应用项目组的成员，也可以通过Dynatrace进行配置后发现。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXkefpPU/EZUFO.jpg)

8. 回到**系统配置文件首选项**，在左面版点击业务分析，点击**创建...**，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXkeeqoQ/whjeF.jpg)

9. 跳出**业务分析编辑器**对话框。先对**筛选器**进行选择，点击“**+**”按钮，选择之前创建好的**showimage**测量。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXkefBbi/10GYpe.jpg)

10. 再对结果抓取结果进行拆分，在**拆分结果**栏 -> 点击“**+**”按钮，选择之前创建好的测量--用户名和客户端IP。如下图：

    ![](http://pic.yupoo.com/east4ming_v/FXkefKdS/wNnu6.jpg)

11. 设置**拆分选项**，按照需求进行拆分。如下图：

    ![](http://pic.yupoo.com/east4ming_v/FXkefVOx/xWmhe.jpg)

12. 至此创建Server-side业务分析完成。可以选择按照**平均响应时间**排序，排序后下方会显示出平均响应时间占比的饼图。如下：

    ![](http://pic.yupoo.com/east4ming_v/FXkeg73O/5odkC.jpg)

> :notebook:说明:
> 关于第7步，如果需要测量该指标，则应该先抓取该指标。
>
> 要抓取该指标，需要配置Servlet的传感器属性。具体如下：
>
> ![](http://pic.yupoo.com/east4ming_v/FXkrJrPK/PRzj5.jpg)
