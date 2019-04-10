Title: Dynatrace AppMon 实战手册 - 18.Dynatrace创建自定义告警事件
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十八篇, 主要介绍如何创建自定义告警事件.

## 概述

Dynatrace有以下概念：

- **Measure**（测量） -- 即需要监控的指标。（包括需要监控的指标、对应的Agent、阈值等）
- **Incidents**（事件） -- 即告警事件。订阅了Measure，配置了Measure的阈值，然后才能创建Incidents，并且定义好根据哪个阈值来告警，以何种方式发送，产生告警该做的动作（如threaddump等）。

本次将介绍如何创建自定义告警事件。

## 操作步骤

本次以创建**指定系统**的**WebLogic的Hogging线程数**告警为例。

操作步骤分解：

- 创建需要监控的指标--**Measure**(测量) -- 1-5步
- 创建告警事件--**Incidents** -- 6-8步

1. 打开**系统配置文件** -> **测量结果**标签页 -> 点击**创建测量**。如下图：

   ![](./images/appmon_create_incidents_1.JPG)

2. 默认有所有系统的Hogging线程数Measure。可以通过复制，并修改来创建。如下图：

   ![](./images/appmon_create_incidents_2.JPG)

3. 对复制出来的测量进行编辑。如下图：

   ![](./images/appmon_create_incidents_2-1.JPG)

4. 编辑Measure（测量）的相关属性。（包括：名称、具体的测量属性、阈值、对应的Agent组）。如下图：

   ![](./images/appmon_create_incidents_3.JPG)

   ![](./images/appmon_create_incidents_4.JPG)

   ![](./images/appmon_create_incidents_5.JPG)

5. 至此，Measure（测量）创建完毕。

6. 开始创建**事件规则**，点击 **事件**标签页 -> 点击 **创建事件规则**。如下图：

   ![](./images/appmon_create_incidents_6.JPG)

7. 告警**条件**选择上文创建好的Measure（测量）。

8. 告警**动作**可以配置发邮件，做快照等。如下图：

   ![](./images/appmon_create_incidents_7.JPG)

9. 告警**操作**可以进行更多的设置。另外，可以对告警的细粒度、严重性、告警抑制时间等进行设置。如下图：

   ![](./images/appmon_create_incidents_8.JPG)

10. 至此，自定义告警创建完毕。
