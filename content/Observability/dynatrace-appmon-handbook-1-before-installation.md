Title: Dynatrace AppMon 实战手册 - 1.安装组件前必备工作
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability, 性能调优
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第一篇, 主要是安装Dynatrace前的准备工作. 如容量评估和资源需求.

[TOC]

## 安装前准备

- 禁用**超线程**（Hyper-Threading）
    - `/proc/cpuinfo`  
    - 这是开启了超线程: `threads per core: 2`  processor = core * 2
- 对于**Medium**及以上规模，CPU时钟频率需大于等于2.6GHz

### Size

![size1](http://pic.yupoo.com/east4ming_v/GcvZBqZN/2IfCJ.jpg)

![size2](http://pic.yupoo.com/east4ming_v/GcvZByIh/RicSG.jpg)

![size3](http://pic.yupoo.com/east4ming_v/GcvZBDNd/KGXM7.jpg)

## Dynatrace Server

- 语言及字符集必须为**LANG=en_US.UTF-8** (否则可能仪表板、告警邮件会乱码)
- Linux修改 ~/.bash_profile （直接cd到软件目录或```export DT_HOME=/opt/dynatrace-6.5```）
- Linux修改chkconfig（配置服务项）
- Linux关闭selinux
- 6.3+ Linux用户注意语言设置为中文。
- Linux需要安装JRE 6+（推荐Oracle JRE 8）
- 会话存储不要多于**2T** （500tps，一天1TB空间）
- ulimit -n 2048或更高
- 内存分析服务器：在dtanalysisserver.ini中设置-Xmx。
- Windows：电源选项设置为**高性能** （Linux也需要查看: `/proc/cpuinfo`）
- 不建议SAN-based存储，**可能**会成为瓶颈(需要测试性能)

> **为什么需要这么多核?**
>
> Dynatrace 是一个复杂的软件解决方案，每时每刻都在后台进行海量的复杂计算。因此高性能的CPU是吞吐量的必要保障。下列列出Dynatrace Server需要较多CPU核数的一些原因：
>
> - 关联引擎
> - 实时分析
> - 通信（Clients, Collectors, etc.）
> - 数据库
> - 存储
> - 分析缓存
> - 数据导出
> - Web servers
> - 任务和监视器的job center
> - 事件（告警）中心
> - 垃圾收集
> - 自监控和检查
> - 操作系统
> - ...

### 禁用Index唯一化Agent名称

要禁用这个功能，需要在Dynatrace Server的启动文件中加入一个布尔值。默认为true，需要将其设为false。如下

```java
-Dcom.dynatrace.diagnostics.collector.agentcenter.unique_agent_names_with_index=false
```

### PurePath超时时间

默认为600s（10min），最大可以设置到3600s（1 hour）。在**dtserver.ini**

```java
-Dcom.dynatrace.diagnostics.completenessTimeout=<valueInSeconds>
```

### 业务分析最大分裂数

在**dtserver.ini**中，在 *-server* 前一行添加如下内容：(第二个参数可以根据需要更改，如修改为75000)

```java
-Dcom.dynatrace.diagnostics.server.OverruleMaxSplittingsBTs=MeasureExplosionPreventionTest:
ManySplittingsTimeMillis=50000, MeasureExplosionPreventionTest:MeasureExplosionTriggeringBT=50000
```

### Server Side报告限制

在**dtserver.ini**中，设置如下参数：(需要添加在*-vmargs* 后一行)

```java
-vmargs
-Dcom.dynatrace.diagnostics.reporting.maxTableRows=10000
-Xmx1920M
```

> **并行报告数设置**
>
> 默认为3
>
> `-Dcom.dynatrace.diagnostics.reporting.maxConcurrentReports=5`
>
> **报告等待超时**
>
> 默认60s
>
> `-Dcom.dynatrace.diagnostics.reporting.reportWaitTimeout=120`
>
> **报告等待队列长度**
>
> 默认为3
>
> `-Dcom.dynatrace.diagnostics.reporting.maxWaitingReports=5`
> **非拉丁语系PDF报告**
> `-Dcom.dynatrace.diagnostics.reporting.pdf.english=false`

### GC告警设置

有以下3个参数可以进行设置，在**dtserver.ini**中，使用-D<参数>=<值>

| 参数                                                             | 值                    | 描述                                                     |
| ---------------------------------------------------------------- | --------------------- | -------------------------------------------------------- |
| com.dynatrace.diagnostics.maxRelativeGCActivity                  | int (default = 15) %  | Set custom health threshold for max relative GC activity |
| com.dynatrace.diagnostics.healthWatchPeriodGc                    | int (default = 5) min | Set custom process health threshold for the watch        |
| com.dynatrace.diagnostics. healthWatchPeriodViolationThresholdGc | int (default = 4) min | Set custom process health threshold for the watch        |

## Dynatrace Analysis Server

- 按照监控的JVM的最大heap+25% 修改最大内存-Xmx

## Dynatrace 数据库

### 不同分辨率细节说明

![分辨率细节](http://pic.yupoo.com/east4ming_v/GcvZCl1E/NcZPS.jpg)

### SQL Server

- 起始空间5G
- DBowner权限
- 表排序规则要求：**Chinese_PRC_CI_AS**

### Oracle

- dba
- 字符集：**UTF-8**

## Dynatrace Collector

- 预置JDK 8（推荐Oracle）

- Linux修改 ~/.bash_profile （直接cd到软件目录）

- Linux修改chkconfig（配置服务项）

- Linux关闭selinux

- 如果Collector和Server不在一块，在脚本或注册文件中加入`-server <dynaTraceServerName>`

- 如果要配置多实例，添加`./dtcollector -instance collector02 -listen :10001`

- 对于服务项，拷贝$DT_HOME/init.d/dynaTraceCollector 脚本到/etc/init.d/dynatraceCollector02。并做以下修改：(2选1)
    - `DT_OPTARGS="-instance collector02"`
    - `DT_INSTANCE=collector02`

### 最小需求

50个Java或25个.Net Agents

- Disk：30GB
- Memory：2GB（Collector组件需要的，OS要更多一点，3GB+）
- CPU Cores：1 （禁用超线程，推荐2Core+）
- limits.conf 打开文件数 最小为：(500+3×Agents数)×Collectors数

### 使用Index唯一化Agent名字

要禁用这个功能，需要在Dynatrace Collector的启动文件**dtcollector.ini**中加入一个布尔值。默认为true，需要将其设为false。如下

`-Dcom.dynatrace.diagnostics.collector.agentcenter.unique_agent_names_with_index=false`

## Dynatrace Client

### 客户端最小需求

- x64（Dynatrace 6.5+）
- Disk：100MB
- Memory：1GB
- 分辨率：1024×768
- Webstart Client：
    - IE 8+ Firefox 38-48是经过Dynatrace认证的
    - Oracle JRE >= 1.8.0_45

### Client Side 报告限制

可以在**dtclient.ini**中修改如下参数：(参数得加在 *-vmargs* 后一行，而不是最后。)

```java
-vmargs
-Dcom.dynatrace.diagnostics.reporting.maxTableRows=10000
-Xmx512M
```

对于Webstart Client，需要设置**JAVA_TOOL_OPTIONS**环境变量：

`JAVA_TOOL_OPTIONS=-Dcom.dynatrace.diagnostics.reporting.maxTableRows=10000`
