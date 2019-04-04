Title: Dynatrace AppMon 实战手册 - 9.Dynatrace自定义仪表板
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第九篇, 主要是定制化仪表板, 直观可视化展现监控数据.

[TOC]

▽ 仪表板 -> 新建
![新建仪表板](./images/appmon-add-dashboard-1.png)

▽ 在对应的系统配置文件下，选择图标绘制——自定义，添加系列：
![添加系列](./images/appmon-add-dashboard-2.png)

▽ 选择测量值，以下以“web页面请求——Purepath响应时间”为例，按应用程序拆分：
![web请求](./images/appmon-add-dashboard-3.png)

> :notebook:备注:
> 注：dynatrace上几乎所有地方都可以可以直接ctrl+F进行搜索。

▽ 调整图表属性. 如重命名、选择时间范围、分辨率、图标类型、拆分模式、可视性等：
![图表属性](./images/appmon-add-dashboard-4.png)

▽ 可以继续在该仪表板中添加系列，即将多个图表放在一个仪表板中：
![添加多个图表](./images/appmon-add-dashboard-5.png)

▽ 拖动图表的标题，结合每个图表的属性，直到调到满意的效果。
![最终效果](./images/appmon-add-dashboard-6.png)
