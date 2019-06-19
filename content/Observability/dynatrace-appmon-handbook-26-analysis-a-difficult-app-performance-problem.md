Title: Dynatrace AppMon 实战手册 - 26.分析诡异的应用性能问题
Category: Observability
Date: 2019-06-19 18:50
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第二十六篇, 主要介绍Dynatrace分析一次某保险客户诡异的应用性能问题.

[TOC]

## 一 概述

### 1.1 客户需求

#### 1.1.1 客户问题描述

客户通过Dynatrace发现某台Jboss的JVM**内存突然提交，然后垃圾回收**。如下图。

![](http://pic.yupoo.com/east4ming_v/GmHC5HKe/6IqvB.jpg)

#### 1.1.2 客户需求

**客户想要了解Root Cause。**

### 1.2  收集信息概述

客户发现Jboss的内存突然彪增，且JVM的GC时间大幅增长。查看Dynatrace发现，当时该及节点已经发生**Perm区内存溢出**。且有**告警**产生（同时应用关键业务错误率大幅增长）（Perm区内存溢出导致的OLD去彪增和GC时间彪增，具体分析见下文）。如下图：

![](http://pic.yupoo.com/east4ming_v/GmHC5NsA/8zCBy.jpg)

![](http://pic.yupoo.com/east4ming_v/GmHC5SAB/jRbrt.jpg)

## 二 事故影响范围

查看当时的主机、JVM及应用业务情况，该问题造成一系列的连锁影响，包括：

- **CPU利用率升高**
- 物理内存升高
- JVM heap区增大
- **JVM gc及挂起时间变长**
- Jboss线程数上升
- **关键业务全部失败**
- 关键业务响应变慢
  具体如下图：

### 2.1 主机

![](http://pic.yupoo.com/east4ming_v/GmHC6cC7/AeojF.jpg)

### 2.2 中间件

![](http://pic.yupoo.com/east4ming_v/GmHC5XC0/VPQzr.jpg)

### 2.3 应用

![](http://pic.yupoo.com/east4ming_v/GmHC6Wjg/myso8.jpg)

## 三 问题分析及定位

### 3.1 我定制2个仪表图来分析问题

具体如下图。**直接Perm OOM的原因是：类加载量的大幅增长**（因为Perm区存放的就是静态类和常量等，而Perm OOM JDK默认会做fullgc，因此导致gc及挂起时间增加；因为无法GC掉，会导致Heap区调整及CPU增加、线程数增加）

![](http://pic.yupoo.com/east4ming_v/GmHC6jtL/WnSxj.jpg)

### 3.2 为什么加载的类会突然飙增

我们对上图放大，查看细节。如下图：

类加载数量是在**8:25-8:30**期间大幅增长的。**接下来我们需要查看这期间的该Jboss具体在做什么业务。**

![](http://pic.yupoo.com/east4ming_v/GmHC7g9r/M5dMD.jpg)

### 3.3 查看8:25-8:30的Jboss上的purepath

> purepath简单理解：所有的事务的分布式方法调用栈及相关信息。（如响应时间、时间细分、线程、LOG、Exception、SQL、Message等）

如下图，直接可以看出：

- **导致该问题的root cause 事务：/RuleManager/showCalib1QueryCondition.htm**
- **导致该问题的root casue代码：c3p0(c3p0性能有问题。调用c3p0前后会有类加载的动作，正是这个情况导致了当时大量的类加载)**  （下图forName0就是类加载的相关方法）
  ![](http://pic.yupoo.com/east4ming_v/GmHC7aDf/JGcrG.jpg)

## 四 总结及优化建议

### 4.1 问题发生的先后顺序

1. 出现大量的/RuleManager/showCalib1QueryCondition.htm请求
2. 需要加载大量的C3p0相关类
3. 类加载数量大幅增长
4. Perm区256M内存用完
5. 触发JVM full gc
6. gc及挂起时间增加
7. 无法GC掉 -> CPU增加、线程增加、Heap区增加、业务失败

### 4.2 优化建议

#### 4.2.1 中间件（治标不治本）

1. 增大Perm区大小

2. 优化与Perm清理有关的参数（如Perm满后清理，不执行full gc等）

3. 为了更方便的定位问题，特别是在没有Dynatrace的情况下，**建议在生产环境开启GC日志。**

   > 阿里的JAVA专家说过:
   >
   > 其实线上开GC日志没关系啦，我们线上就一直开着，对性能不会有那么大影响的。

#### 4.2.2 开发

- 优化JDBC相关代码（如果想要优化c3p0代码可以看3.3的代码逻辑。如果不想优化建议直接不要采用c3p0作为JDBC框架，选择其他JDBC框架）

### 4.3 最后说一句

其实这个问题一个月以前就已经分析过了，但是由于当时的影响只是*应用关键业务变慢*，所以并没有引起重视。但是这次造成的影响就比较大了，直接导致关键业务全部失败以及Jboss长时间挂起（即不可用）。

所以，大的生产事故，其实可能都是因为一些细小的，我们认为没关系或者可以忽略的性能问题导致的。

> ​:punch:​ 生产无小事！责任大于天！
