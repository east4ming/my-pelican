Title: Dynatrace AppMon 实战手册 - 10.Dynatrace权限管理
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十篇, 主要是AppMon的权限管理功能介绍和配置.

1. 在Dynatrace Server设置 -> 用户面板，如下：

   ![](http://pic.yupoo.com/east4ming_v/FX8vxzug/YnE01.jpg)

2. Dynatrace 关于权限管理方面，从3个层面实现对用户权限的精细化管理，从面到点依次为：**角色、组、账户**。同时，Dynatrace的权限管理支持LDAP以及密码复杂度的配置。

3. “角色”层面，主要负责Dynatrace所有详细权限的配置。Dynatrace默认配置的有如下角色：Administrator（管理员）、Guest（访客）、Power User、User（普通用户）。其中，Administrator具有Dynatrace的所有权限。具体如下：

   ![](http://pic.yupoo.com/east4ming_v/FX8vuSXj/7BPLt.jpg)

4. 可以根据生产环境的实际需要，创建新的角色及配置详细的权限。如：创建应用项目组的角色--Project Team。权限包括应用分析的所有权限及保密字符串的查看权限，以及可以做线程快照进行分析。权限细节如下：

   ![](http://pic.yupoo.com/east4ming_v/FX8vuCTD/8Iu8o.png)

5. “组”层面。对3个方面进行了细化，分别是：Dynatrace Server管理（指定角色权限）；系统配置文件（对具体的系统配置文件进行详细的角色权限配置）；仪表板（对具体的仪表板进行权限配置，分为：可读和读写权限。）默认的组有：Incident Email Group（事件邮件告警组）、Business Users。

6. 根据实际情况，创建新的组并配置详细的权限。如：创建ilog组--ilog。权限为Project Team，所有与ilog相关的仪表板都有可读权限。具体操作如下：

   ![](http://pic.yupoo.com/east4ming_v/FX8vuaV7/3bcPr.png)

   ![](http://pic.yupoo.com/east4ming_v/FX8vulJK/medium.jpg)

   ![](http://pic.yupoo.com/east4ming_v/FX8vuvnf/medium.jpg)

7. “账户”层面。就是实际使用Dynatrace的账户。包括以下内容：用户ID、电子邮件、所属用户组。具体操作如下：

   ![](http://pic.yupoo.com/east4ming_v/FX8vuLrs/medium.jpg)
