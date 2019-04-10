Title: Dynatrace AppMon 实战手册 - 16.Dynatrace创建Server-side业务分析实战案例3
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十六篇, AppMon的一个很强大的功能就是"业务分析", 在AppMon中, 可以通过不同的数据来源(浏览器端, app端, server端)来创建业务分析, 本次用第三个实战案例介绍如何创建 Server-side 业务分析.

## 案例介绍

某关键业务不仅仅需要URI进行过滤，同时需要对query字段*busiid*和*showflag*进行过滤。

## 操作步骤

思路分解如下：

- 配置sensor属性 - **Servlet** 的**请求属性** -- 添加对应的query字段；
- 创建业务分析，配置指定的POST的URI、query；
- 将配置好的测量作为组合条件配置业务分析。

> :notebook:说明:
> 需要实现的业务分析示例如下：
>
> ![](./images/bt_1.jpg)
>
> :heavy_exclamation_mark:不正确的配置示例如下：
>
> ![](./images/bt_2.jpg)

具体步骤如下：

1. 配置**servlet**传感器属性 -- **请求参数** 来抓取对应的**query**信息，如下图：

   ![](./images/bt_4.jpg)

2. 创建包含指定query的测量 -- busiid （通过**Web请求 - 参数值** 这个模板测量）。如下图：

   ![](./images/bt_5.jpg)

3. 创建包含指定query的测量 -- showflag，如下图:

   ![](./images/bt_7.jpg)

4. 注意**测量**的**拆分阈值**要设置为超过**1**就拆分。如下图：

   ![](./images/bt_6.jpg)

5. 通过组合3种测量 - post URI 、 query 字段 busiid、query字段showFlag 通过组合 **与** 条件来创建业务分析。如下图：

   ![](./images/bt_3.jpg)

6. 至此，通过query设置业务分析已经完成。
