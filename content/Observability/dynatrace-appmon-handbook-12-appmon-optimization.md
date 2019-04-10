Title: Dynatrace AppMon 实战手册 - 12.Dynatrace细节优化
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十二篇, 主要是关于AppMon应用监控的响应时间和失败率阈值进行细致优化.

## 应用响应时间失败率阈值优化

### 概述

Dynatrace的应用相关阈值（包括：响应时间、最慢响应时间、失败率）是由Dynatrace 的**Smart Baseline** 功能来进行动态调整的。

> :notebook:备注:
> 具体的实现原理可以查看官方文档：[Baseline and Smart Alerting Explained](https://community.dynatrace.com/community/display/DOCDT62/Baseline+and+Smart+Alerting+Explained)
>
> 大致是根据**过去7天**的表现来进行动态调整。

在某些特殊应用中，Dynatrace的自动基线并不符合生产系统的实际情况，会出现较多的误报。具体如下：

![](http://pic.yupoo.com/east4ming_v/FXiRtsLv/5BIUQ.png)

在这种情况下，我们需要根据应用的实际情况将动态基线改为静态基线。

### 操作步骤

下面以修改具体请求的响应时间基线为例，来说明如何对基线、阈值进行优化。

1. 在Dynatrace指定系统配置文件的**监控**页面 -> 点击中下方的**应用程序** -> 选择对应的应用 -> 选择需要调整的**业务分析** -> 点击具体业务分析的**齿轮**图标 -> 选择**配置基准**。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXiRu0Af/aY6N4.jpg)

2. 跳出如下**基准设置**对话框。可以设置失败率、响应时间、是否告警等内容。在此，我们将**响应时间**设置为静态基准：1000ms。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXiRtDaw/nPr34.png)

3. 将**最慢响应时间**（最慢的10%请求）的静态基准设为：10000ms。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXiRtFcD/WkmXY.png)

4. 至此设置完成，回到**应用程序** -> 具体的业务分析页面。我们看到基准已经按照配置调整为静态。（绿色线条）。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXiRtNUs/QklZs.png)
