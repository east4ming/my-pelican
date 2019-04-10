Title: Dynatrace AppMon 实战手册 - 13.Dynatrace Agent 迁移
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十三篇, AppMon毕竟是商业软件, 可能因为商务和价格原因, 无法做到生产应用全覆盖. 这时, 就需要根据应用的重要级别, 生命周期, 近期性能表现等, 对AppMon的Agent进行迁移, 复用.

## 概述

在实际生产环境中，由于Dynatrace 的License有类型、数量上的限制（限制同时接入的agent数量），但是并不限制agent必须永远嵌入同一个JVM中。而且，根据生产环境中不同应用系统的上下线，也需要对Dynatrace 的Agent进行调整迁移，以最大化地发挥Dynatrace的监控价值。

## 操作步骤

Dynatrace Agent迁移主要分为3大步骤：

- Dynatrace迁移前相关告警项的临时关闭（即创建Dynatrace事件**停机时间**）
- Agent从原有JVM中移除，并重启对应JVM
- Agent嵌入新的JVM，并重启对应JVM

最后生效。

### 创建停机时间

1. 在左侧**驾驶舱**中，双击**事件**，出现事件仪表板 -> 点击“旦”形的停机时间图标，可以看到已经创建好的停机时间规则。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXj3wRLW/iZTj3.jpg)

2. 右击**停机时间**表格空白处 -> **创建停机时间**，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXj3wEfp/6NQPj.jpg)

3. 跳出**创建停机时间**对话框，包括：停机开始时间及持续时间；重复周期；结束时间。此处配置如下图，然后点击下一步。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXj3xe7v/11CaLh.jpg)

4. 选择对应的告警事件，此处需要选择对应的系统配置文件的告警事件：**Application Process Unavailable (unexpected)** ，并点击下一步。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXj3xnC3/medium.jpg)

5. 配置完成后，返回停机时间表查看，规则已存在，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXj3wJlM/QbX65.jpg)

### 移除Dynatrace Agent

> :notebook:说明:
> 以Weblogic为例。其他中间件操作类似。

- 备份对应中间件实例启动脚本。

- 取消对应中间件实例启动脚本中的Dynatrace Agent字段，移除启动脚本中的如下内容：`-agentpath:<DT_HOME>/agent/lib/libdtagent.so=name=<AgentName>, server=<dynaTraceCollectorName>`

- 在重启窗口时间段内，重启对应中间件实例。

- 移除Dynatrace Agent已完成。

### 安装Dynatrace Agent

> 请参考文档：[dynaTrace安装文档- 6.4  Agent 配置]( http://cloud.189.cn/t/V7VZze3uqERv)

安装完成后，可以在Dynatrace客户端左边**驾驶舱** -> 双击**Agent概述** -> 查看迁移后的Agent是否存在及抓取的Purepath总数。

至此，Dynatrace Agent迁移完成。
