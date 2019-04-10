Title: Dynatrace AppMon 实战手册 - 19.Dynatrace创建告警事件停机时间
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十九篇, 主要介绍如何屏蔽告警.

## 概述

Dynatrace在生产环境的使用中，往往会碰到所监控系统的正常生产重启（如停机窗口、发版本、维护等）导致的误告警。

为了避免这种问题，可以通过设置告警**停机时间**（downtime)来减少不必要的告警。

## 操作

1. 点击**事件**仪表板右上角按钮。如下图：

   ![](./images/appmon_downtime_1.JPG)

2. 点击后出现**停机窗口**表。如下图：

   ![](./images/appmon_downtime_2.JPG)

3. 在表中点击右键**创建停机时间**。勾选对应的系统配置文件中的对应的告警规则（如停机或重启时会出现的告警：应用关闭和应用进程不可用）。出现如下对话框：

   ![](./images/appmon_downtime_3.JPG)

4. 点击下一步，进行详细的设置，如下图：

   ![](./images/appmon_downtime_4.JPG)

5. 停机时间规则可以时临时性的一次。也可以根据生产重启窗口的要求，如设置为每月的第三周周六。如下图：

   ![](./images/appmon_downtime_5.JPG)

6. 配置完成后显示如下。

   ![](./images/appmon_downtime_6.JPG)
