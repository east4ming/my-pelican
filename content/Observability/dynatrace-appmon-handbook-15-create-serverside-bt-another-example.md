Title: Dynatrace AppMon 实战手册 - 15.Dynatrace创建Server-side业务分析 - 实时抓取某系统大于30s的请求
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十五篇, AppMon的一个很强大的功能就是"业务分析", 在AppMon中, 可以通过不同的数据来源(浏览器端, app端, server端)来创建业务分析, 本次用另外一个实战案例介绍如何创建 Server-side 业务分析.

## 案例介绍

某系统是某保险公司的核心系统。需要对系统进行性能上的优化工作，开发及项目组同事想要抓取到系统上个月所有响应时间超过30s的请求，以及请求的详细信息（如请求的具体时间等）。

## 操作步骤

思路分解如下：

- 创建针对 **核心系统**响应时间**大于30s**的**web 请求**的测量； -- 第1-3步
- 创建业务分析，用来筛选并按照URI拆分相应的请求；-- 第4-8步
- 结果展示 -- 第9-10步

具体步骤如下：

1. 进入**系统配置文件首选项** -> 左面版**测量** ->  查找**web请求**-**时间** 测量 -> 复制**web请求测量** ，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXW3gTEn/10SqYN.jpg)

2. 跳出编辑测量属性的对话框，在**阈值** -> 严重级别上限值设置为 30000ms，如下图:

   ![](http://pic.yupoo.com/east4ming_v/FXW3hgdf/5lMEx.jpg)

3. 转到**详细信息**标签页，选择要抓取请求的系统--**核心系统**。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXW3hmv8/pTYrW.jpg)

4. 在**系统配置文件首选项** -> **创建...** ，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXW3hBdF/byLKG.jpg)

5. 跳出**业务分析编辑器**，设置业务分析的**名称**、**描述**、**筛选器**。点击筛选器右侧“+”按钮，选择之前创建的测量。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXW3hRyy/2DyIX.jpg)

6. 选择业务分析拆分方式。点击**拆分结果** -> 点击“+”按钮 -> 选择对应的拆封规则。本例中应该选择的拆分规则为：**完整的URI**。（图片仅用作说明）如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXW3i4uG/HzFFm.jpg)

7. 选择拆分限制。点击**拆分选项...** ，跳出拆分选项对话框，选择**不限制**。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXW3ibxt/KIdRF.jpg)

8. 配置完成后的**业务分析**如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXW3hHP6/FMqWt.jpg)

9. 至此，业务分析配置完成。显示效果如下图（该图展示的是关于符合条件的URI的统计信息，上表显示的结果按照完整的URI进行拆分，每个拆分项都有**计数**、**平均响应时间** 等统计数据；下图中按照需求可以对**计数**、**平均响应时间**等生成饼图。

   ![](http://pic.yupoo.com/east4ming_v/FXW3ijPU/14leMe.jpg)

10. 如果需要查看每个URI执行的**开始时间**、**持续时间**、**执行堆栈**、**客户端IP**等详细信息，可以右击对应的URI，点击**深入分析** -> PurePath 跳转到PurePath界面，以此来查看完整的信息。
