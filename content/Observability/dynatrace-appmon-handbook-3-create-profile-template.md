Title: Dynatrace AppMon 实战手册 - 3.创建系统配置文件模板
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第三篇, 主要是创建系统配置文件模板.

## 步骤

1. 在左侧边栏中，右键**系统配置文件模板** → **创建系统配置文件模板**， 如下图：

   ![](http://pic.yupoo.com/east4ming_v/Gcwcoiwt/hknCr.png)

2. 配置系统配置文件模板基本信息，如下图：

   ![](http://pic.yupoo.com/east4ming_v/GcwcowF1/QOxbw.jpg)

3. 选择对应的技术栈（Java、.NET、Web server、PHP、Native）,如上图。具体解释如下：

   1. Java  .NET  PHP无须解释
   2. Web server - 对应一系列Web server，如Apache、Nginx、IIS等
   3. Native - 对应的是Dynatrace的ADK，通过在应用中嵌入该ADK，可以实现对C++、Python等的监控。

## 要点

### 事件（即告警）相关配置

**使某些事件活动或不活动**

以下事件规则不需要启用，具体如下图：

- 部署
- 测试违例
- 事物整体失败率高（**失败率太高**已经覆盖）
- 数据库Agent相关（没有购买数据库Agent license则无需开启）
- 页面操作失败率高（需要UEM license；**失败率太高**有交集）
- 应用程序进程关闭（根据需求确定是否开启）

![](http://pic.yupoo.com/east4ming_v/GcwcoCV4/M1i31.png)

### 错误检测配置

**不要将日志标记为错误**

删除**重要的日志记录**规则。

原因：

有的开发为了在生产上显示日志，会将一些Info等级别的信息设置为Error，而出现Error日志报错并不一定意味着**事务**失败。

![](http://pic.yupoo.com/east4ming_v/GcwcoNLt/P7SbT.png)

### 错误规则创建

可以根据应用所特有的Exception、Logging等来创建，具体如下：

![](http://pic.yupoo.com/east4ming_v/GcwcsOkh/65iq5.jpg)

### 应用程序定义

Dynatrace 6.5 可以通过Web/Mobile（6.5之前只有这一种定义方法）、Messaging、Entry Point来定义应用，可以进一步细化应用的定义。如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcsTQp/R2lT9.jpg)

### 用户体验

如果没有购买UEM license，则禁用UEM，如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcoZMb/amzM1.png)

### Schedule

**创建时间计划**，如创建**每个工作日、每周、每月**计划。如下图：

![](http://pic.yupoo.com/east4ming_v/Gcwcp5kE/44NZA.jpg)

### Agent Group - Java

创建Java技术栈的Agent Group模板，如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcpaOy/8KhP9.jpg)

**选择需要放置的Sensor**

原则：最少最需要。如下图：

必须的Sensor：

- JDBC
- Exceptions
- Java Logging
- JMX MBean Server
- JMS
- JMS Receive Entry Point
- Executor Tagging
- Thread Start Tagging
- Java Web Requests
- Servers
- Java Web Services

![](http://pic.yupoo.com/east4ming_v/Gcwcpjjm/12bHs1.jpg)

#### Sensor - Exception (Java)

对Dynatrace默认的Exception定义进行细化，如下图：

原因：原有的直接排除java.开头的Exception会排除大量我们需要获取的Exception，如网络相关的报错等。所以我们需要尽可能细化不需要抓取的Exception，如**beans**、 **方法找不到**相关异常。

![](http://pic.yupoo.com/east4ming_v/GcwcpAV9/YqhSj.jpg)

#### Sensor - JDBC

- 启用聚合（推荐生产环境开启，因为单个事务的SQL执行次数较多，如果不聚合分析起来很不方便。启用聚合了则无法获取**绑定值**）
- SQL长度跳大（如：10240）（默认512长度，经常会抓取到不完整的SQL，从而无法定位SQL问题。建议该值大于所监控的应用中的最大的SQL长度）

如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcpVjP/10a2Js.jpg)

#### Sensor - Logging (Java)

此处Log等级大小写敏感，我们可以添加我们监控的级别，如对于WebLogic，可以添加**Error**等级别，如下图：

![](http://pic.yupoo.com/east4ming_v/Gcwcqeew/5M54W.jpg)

#### Sensor - Servlet

- 通常，我们认为静态资源不会对系统性能造成影响，无需监控，此处设置排除对静态资源的监控。
- 此外，一些中间件、硬件设备，会有与应用无关的URI，我们也需要排除。

如下图：

![](http://pic.yupoo.com/east4ming_v/Gcwcqnte/hunpl.jpg)

### Agent Group - .NET

创建.NET Agent Group模板，如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcquzV/Pc4ms.jpg)

**选择必要的Sensor**，如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcqFMu/CkZXe.jpg)

#### Sensor - ADO.NET

与JDBC Sensor类似，如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcqMPS/iVLgB.jpg)

#### Sensor - ASP.NET

与Servlet类似，见下图：

![](http://pic.yupoo.com/east4ming_v/GcwcqRLY/8DuGF.jpg)

### API

可以针对应用开发的需求，定义API，如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcqXC8/th008.jpg)

![](http://pic.yupoo.com/east4ming_v/Gcwcr2YK/14SZ6f.jpg)

### Measure

根据应用监控的需求，进行相关Measure的定义，此类数据可以进一步作为**过滤、聚合、拆分**等条件创建Business Transaction。

如需要创建**大于10s的web请求**的measure，则具体创建如下：(由**web requests - time**复制修改而来，设置上限阈值)，如下图：

![](http://pic.yupoo.com/east4ming_v/GcwcsFyB/4pne8.jpg)

### Business Transaction

如需要进行更为复杂的应用监控（如针对应用细节的监控、对关键业务的监控等），可以创建Business Transaction。

如要抓取所有**web响应时间大于10s**的请求，可以将之前创建的Measure作为过滤条件来创建。如下图：

![](http://pic.yupoo.com/east4ming_v/Gcwcrg0x/eFEUX.jpg)

> TIPS:
>
> - 勾选**Active** 才会正式启用。
> - 勾选对应选项后结果会存放到数据库中。
> - 三大因子
>     - Filter
>     - Calculate Results
>     - Split Results
> - Splitting 也是重要的选项
> - 基线设置用来设置动态或静态的告警阈值

### Monitor

> Monitor这块内容待完善及丰富。

#### Unix Monitor

![](http://pic.yupoo.com/east4ming_v/GcwcrlB8/kLc10.jpg)

#### VMware Monitor

**Host System Performance Monitor**

![](http://pic.yupoo.com/east4ming_v/GcwcrlB8/kLc10.jpg)

![](http://pic.yupoo.com/east4ming_v/GcwcrLyx/9Rh2b.jpg)

**Virtual Machine Performance Monitor**

![](http://pic.yupoo.com/east4ming_v/GcwcrU8l/7iHmE.jpg)

![](http://pic.yupoo.com/east4ming_v/Gcwcs3as/cUXUV.jpg)

#### Windows Performance Monitor

![](http://pic.yupoo.com/east4ming_v/GcwcsqFN/hKRir.jpg)

## 总结

至此，系统配置文件模板及关于系统配置文件大部分要点已经配置完成，后续可以基于该模板创建正式的系统配置文件。

正式的系统配置文件还需要配置的内容有：

- Agent基础配置（如mapping、分辨率等）
- 观察层（Messaging、Load Balance等）

需要细化的内容有：

- 应用定义
- Monitor
- 任务（定时报告、定时采样等）
- Measure（中间件指标、JMX指标、应用其他指标等）
- Business Transaction （关键业务等）
- Sensor（应用特定Sensor，如关键方法--核保金额；定义入口点，如批处理、TCP Socket及其他）
