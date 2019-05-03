Title: Dynatrace 告警简要分析流程
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability, 性能调优
Summary: 在日常运维工作中, 我们经常会碰到各种各样的应用问题和告警, 如: 应用响应变慢, 应用失败率升高, 应用不可用等等, 本文介绍通过Dynatrace分析这些问题的简要流程.

[TOC]

## 告警类别及含义

### 应用告警

#### 响应时间/速度较慢的请求的响应时间降低

1. 响应时间降低--对应的应用或URL平均响应时间(中值)明显高于期望。即使所观测的响应时间尚可被客户接受，这种状态明显是应用程序或是硬件问题导致，并且会降低所能达到的最大吞吐量。
2. 速度较慢的请求的响应时间降低--观测中 10% 最慢请求的反应时间明显增加。这将导致用户体验变差。应用程序及硬件问题都能导致该问题。

#### 失败率过高/页面操作/事务整体失败率高

1. 失败率过高--事务失败率远高于预期。
2. 页面操作失败率高--总体页面操作失败率超过预设阀值。
3. 事务整体失败率高--事务整体失败率高。

### 中间件告警

#### 应用程序进程不可用（非预期）

与之前连接的应用程序进程/Agent 之间的连接已丢失，无法与 Agent 断开连接。

一般出现该告警的原因为停止或杀掉对应中间件的进程。

#### 应用程序进程运行状况不佳

由于在垃圾回收过程中花费大量执行时间，因此应用程序进程的显著挂起时间会持续一段时间。

一般是由于频繁GC导致的。

#### 可能挂起的JVM

可能的java VM挂起。可能是由于heap/thread dump或者GC活动。原因未知需要手动分析。

#### 应用程序进程内存不足

应用程序进程报出内存不足。

一般是由于中间件内存使用已满或内存溢出。

### 主机告警

主机类告警的阈值与所属的主机组有关。如下图：

![](http://pic.yupoo.com/east4ming_v/FCXRay6p/bea1t.jpg)



### CPU运行状况不佳

CPU使用率或系统时间超过预设阈值。

CPU的阈值有2个阈值：

- 使用率
- 系统时间

#### 硬盘运行状况不佳

主机硬盘的可用空间大小及百分比低于预设阈值。有2个阈值：

- 可用空间大小
- 可用空间百分比

#### 内存运行状况不佳

主机的可用内存大小及百分比低于预设阈值或内存页面故障大于预设阈值。有3个阈值：

- 可用内存大小
- 可用内存百分比
- 页面故障数

#### 网络运行状况不佳

网络带宽使用率大于预设阈值。有1个阈值：

- 带宽使用率

## 告警简要分析流程

### 简介

#### 通用入口

1. “驾驶舱”，如下图：

![](http://pic.yupoo.com/east4ming_v/FCY07pnX/Ry7Q9.jpg)

2. Start Center，如下图：

![](http://pic.yupoo.com/east4ming_v/FCY32F9u/eT8op.jpg)

3. “监控”，如下图：(绿色正常/红色异常/灰色无数据)

![](http://pic.yupoo.com/east4ming_v/FCY4WDEM/l7JDg.jpg)

## 响应时间/速度较慢的请求的响应时间降低

1. 打开事件仪表板，如下图：(告警红色为Severe级别/黄色为Warning级别；告警时间段可以按需选择)

![](http://pic.yupoo.com/east4ming_v/FCY7f5oF/dYODm.jpg) 

2. 移动到对应的告警信息→右键→深入分析→PurePath，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYaxIBv/uWnkT.jpg)

3. 跳转到PurePath仪表板，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYdl5vQ/10ziUa.jpg)

4. 右键仪表板→编辑筛选器→筛选对应的PurePath并应用，如下图:

5. ![](http://pic.yupoo.com/east4ming_v/FCYehBhS/Jkp4w.jpg)

    ![](http://pic.yupoo.com/east4ming_v/FCYfBRlP/NMHo5.jpg)

6. 全选所有的PurePath→右键→深入分析→响应时间热点 （此处可以点击第二列”响应时间“对PurePath进行排序，针对性分析）

![](http://pic.yupoo.com/east4ming_v/FCYhLI4x/nAr3y.jpg)

7. 响应时间热点仪表板，如下：(针对“速度较慢的请求的响应时间降低”告警，需要在右上角“百分比筛选器进行选择。至此，初步分析结果已得出)

![](http://pic.yupoo.com/east4ming_v/FCYk4En1/n9rDF.jpg)

8. 最终分析结果：API细分仪表板及方法细分仪表板，如下图：

9. ![](http://pic.yupoo.com/east4ming_v/FCYlQlsd/NpiKX.jpg)

   ![](http://pic.yupoo.com/east4ming_v/FCYlQd76/REkXi.jpg)

10. 更近一步分析：可以直接分析源代码，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYnAAJy/yrJBF.jpg)

![](http://pic.yupoo.com/east4ming_v/FCYnwwKB/LynTC.jpg)



### 失败率过高/页面操作/事务整体失败率高

1. 事件→Purepath，如上文

2. 编辑筛选器内容，如上文。

3. 按错误排序，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYrsFLH/Qyujo.jpg)

4. 右键上图报错方法，出现具体的报错/异常/日志等内容，如下图：(可以多看十几条PurePath，如果报错内容都相同，则已经初步定位到告警原因)

![](http://pic.yupoo.com/east4ming_v/FCYsL7Nf/UcVBq.jpg)

5. 全选所有PurePath→深入分析→错误率相关菜单，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYtOs3i/Myyj4.jpg) 

6. 定位到告警原因，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYuXMxi/148DNZ.jpg)

### 应用程序进程不可用（非预期）

该类报错通常是由于停止或杀掉或重启中间件等进程导致的。

可以直接在”事件”仪表板中查看，如下图：（告警开始时间就是停进程的时间；终止时间就是启动进程的时间）

![](http://pic.yupoo.com/east4ming_v/FCYwhZNA/gEE3m.jpg)

### 应用程序进程运行状况不佳

该类报错分析起来较为复杂，需要有丰富的中间件运维经验和dynaTrace使用经验。详细信息参考附件：

> 《应用程序进程运行状况不佳分析示例》

### 可能挂起的JVM

如上文所述：可能是由于heap/thread dump或者GC活动。原因未知需要手动分析。具体问题具体对待。

### 应用程序进程内存不足

如上文所述，通常是由于内存溢出或内存快满。分析流程如下：

1. 通过上文提到的入口--“监控”→点击“进程”→查看进程仪表板，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYKC06L/RD3sF.jpg)

![](http://pic.yupoo.com/east4ming_v/FCYJdo4D/10CMzY.jpg)

2. 点击内存快照→创建内存快照→按需选择快照的类型并应用，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYMr7TG/RzIqA.jpg)

3. dynaTrace会自动分析并给出结果，如下图：(至此已经定位到问题所在)

![](http://pic.yupoo.com/east4ming_v/FCYO7UoS/jZMqd.jpg)

4. 如需进一步分析，可以点击内存快照分析的其他标签页。如下图：

![](http://pic.yupoo.com/east4ming_v/FCYPQTpk/T02uX.jpg)

> dynaTrace支持内存溢出时自动做内存快照，且默认开启，在生产环境建议关闭该功能，有需求可以针对性开启。如下图：
>
> ![](http://pic.yupoo.com/east4ming_v/FCYRN2UG/H6NSX.jpg)
>

### CPU运行状况不佳

1. 从入口“监控”进入→主机列表→主机监控，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYV9u5l/aweYD.jpg)

2. 主机监控仪表图分析，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYVyY4X/NmNbr.jpg)

3. 做CPU采样与线程快照（步骤与做内存快照类似，见上文）。CPU采样与线程快照分析如下：(已经定位到告警原因)

![](http://pic.yupoo.com/east4ming_v/FCYX1rCQ/RpJ2j.jpg)

4. 可以对线程快照进一步分析，定位到线程的堆栈以及当时线程执行的URL请求，如下图：

![](http://pic.yupoo.com/east4ming_v/FCYZHuqt/10KqLh.jpg)

### 硬盘运行状况不佳

直接进入主机仪表板，如下图：

![](http://pic.yupoo.com/east4ming_v/FCZ2mxAA/C7G0x.jpg)

### 内存运行状况不佳

1. 直接进入主机仪表板查看内存使用率，如下图：

![](http://pic.yupoo.com/east4ming_v/FCZ3lGA6/medium.jpg)

2. 分析占用物理内存的进程情况。

> JVM使用的JVM代码区、JVM数据区、heap区都应该是固定的。但是JVM进程所使用的线程栈区、永久代、内核内存是可能随着应用程序吞吐量、业务量、负载量的变化而变化的。
>
> JVM是作为一个进程运行在Linux上的。从进程的角度来看，进程能直接访问的用户内存（虚拟内存空间）被划分为5个部分：代码区、数据区、堆区、栈区、未使用区。代码区中存放应用程序的机器代码，运行过程中代码不能被修改，具有只读和固定大小的特点。数据区中存放了应用程序中的全局数据，静态数据和一些常量字符串等，其大小也是固定的。堆是运行时程序动态申请的空间，属于程序运行时直接申请、释放的内存资源。栈区用来存放函数的传入参数、临时变量，以及返回地址等数据。未使用区是分配新内存空间的预备区域。 
>
> JavaNIO使得JVM可以使用内核内存。

## 网络运行状况不佳

直接进入主机仪表板查看网络利用率，如下图：

![](http://pic.yupoo.com/east4ming_v/FCZ2o2RS/hLaMM.jpg)

# dynaTrace告警确认及关闭

dynaTrace的告警确认及关闭需要登录客户端，进入到“事件”仪表板进行操作。具体如下图：

![](http://pic.yupoo.com/east4ming_v/FCZ6HvHe/eop6b.jpg)
