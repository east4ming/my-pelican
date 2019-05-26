Title: Dynatrace AppMon 实战手册 - 20.报告功能
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第二十篇, 主要介绍如何自动手动生成各类报告.

## 综述

dynaTrace可以将dashboard和dashlet转换为自定义的报告。
报告可以有客户端或者服务端生成。计划报告是一种服务端报告。

## 类型和格式

dynaTrace包括下列自定义报告格式：

- PDF

- HTML

- XML

- Excel和Excel2007

- CSV

![PDF](http://pic.yupoo.com/east4ming_v/FhuunmKR/medium.jpg)

![HTML](http://pic.yupoo.com/east4ming_v/FhuumWhj/medium.jpg)

![xml](http://pic.yupoo.com/east4ming_v/FhuuoRBf/medium.jpg)

![Excel](http://pic.yupoo.com/east4ming_v/FhuunQEO/medium.jpg)

![CSV](http://pic.yupoo.com/east4ming_v/FhuumrDF/medium.jpg)

## 客户端报告

### 默认报告

可以通过下列操作创建报告：

- 创建一个dashboard，从**Dashboard**按钮或者右击在右上方的dashboard图标，选择**Report**。

- 生成单个dashlet的报告，邮寄dashlet的标签并且选择**Report**。

之后会出现**Generate Report**对话框，可以进行细节项设置。

![创建报告对话框](http://pic.yupoo.com/east4ming_v/FhuyMfcb/medium.jpg)

1. 报告标题和描述自动由dashboard创建。可以进行修改。
2. 选择报告格式。
3. 更改纸张方向和纸张大小。
4. 定义输出路径
5. 点击**Generate**创建报告。完成后，会自动打开。
这些变更只会应用在一个报告里。

### 自定义dashboard报告

在dashboard属性里选择**Reporting**标签页来改变下列设置：

- 默认格式

- 纸张方向和纸张大小

- 自定义页眉图片

- dashlet顺序和包含项

- 按计划生成报告

![Reporting标签页](http://pic.yupoo.com/east4ming_v/FhuFqY65/medium.jpg)

![自定义项](http://pic.yupoo.com/east4ming_v/FhuGlt9I/medium.jpg)

这些变更将会应用到由这个dashboard生成的每份报告里。

## 计划报告

### 计划报告

报告可以在给定的时间间隔自动生成，并且储存在dynaTrace Server端的文件系统或者通过email发送。计划报告由dynaTrace Server创建。
创建报告任务，执行如下步骤：

1. 打开你想要生成报告的dashboard
2. 邮寄dashboard或者打开dashboard菜单，选择**Report**
3. 自定义报告，可以更改标题、描述、格式、纸张方向和大小、文件名。
4. 点击**Create Schedule**
5. 自定义后处理--通过email发送或储存在dynaTrace Server文件系统。
6. 选择**Schedule**标签页
7. 在Schedules Editor增加或编辑计划。

![计划报告_1](http://pic.yupoo.com/east4ming_v/FhuKKVdo/medium.jpg)

![计划报告_2](http://pic.yupoo.com/east4ming_v/FhuKM5hh/medium.jpg)

![计划报告_3](http://pic.yupoo.com/east4ming_v/FhuKKZ7B/medium.jpg)

### Server端自动报告任务

#### 为什么需要自动化报告？

通过自动化报告，你可以展示累计数据给利益相关者或者发送每日的KPI状态更新到你的邮箱。报告是必须的，而且你不想花费太多时间收集数据，设计报告，执行。如果你曾做同一个报告2次，那么你应该使用dynaTrace的报告功能来自动化生成报告。

#### 目标演练

本次目标演练展示了dynaTrace的报告功能，以及如何更容易的生成报告。学习如何生成你的计划报告。

#### 需求

创建你自己的dashboard或者使用dynaTrace自带的。如果你没有System Profile，没有来自agent的数据的话，使用自监控的内置dashboard。

#### 详细步骤

根据以下步骤自动化生成报告：

1. 打开报告对话框到报告文档
2. 自定义必须的信息
3. 创建一个报告计划
4. 基于计划自动化生成报告

#### 创建报告计划

如果你想通过邮件每天、每周、或者发报告或者发送给多个接收者，那么可以创建报告计划。到**Report**设置项，创建计划。比如，可以创建计划，发送PDF报告，每天8点到你的邮箱，每周到你经理的邮箱。你必须创建两个计划。
对于每天的计划，使用下列的定义：

- Start on：每天

- Time to Send：8:00AM

- End：永久

- Recurrence：每天

定义周六、周日例外：

- Schedule Exclusion：总是排除

- On：周六、周日

- In：每月

![创建报告计划_1](http://pic.yupoo.com/east4ming_v/Fhw8OvM2/medium.jpg)

![创建报告计划_2](http://pic.yupoo.com/east4ming_v/Fhw8PIOd/medium.jpg)

![创建报告计划_3](http://pic.yupoo.com/east4ming_v/FhuKM5hh/medium.jpg)

![创建报告计划_4](http://pic.yupoo.com/east4ming_v/Fhw8PHcr/medium.jpg)

第二个计划每月第一天执行

- Start on:每月第一天

- End：永久

- Recurrence：每月

- 月度计划：每月第一天发送报告

![创建报告计划_5](http://pic.yupoo.com/east4ming_v/Fhw8RcHJ/medium.jpg)

#### 总结

你用dashboard相关的数据配置后，自动报告节省了很多时间。而且自动化的技能可以作为一个数据导出引擎将数据发送到你的工具上。定时拿到数据或者把数据发送到自动化工具以备之后处理。

## 报告的限制

### 客户端报告限制

客户端报告有明确的限制：

- 只有客户端上有数据展示才会报告-报告之前不会触发刷新

- 客户端报告会跳过没有激活的dashlet。要确保所有dashlet的数据显示在报告里，你必须在创建报告前手动刷新。这项不适用于通过REST的server端报告或计划报告。

### 大小限制

dynaTrace限制报告大小，这样dynaTrace Server或客户端不会受到非常大的报告的影响。要生成大的报告，使用下列配置项：

#### 软限制：每个dashlet 100行

dashlet和dashboard被设置每个表100行。该设置会被具体的dashboard和dashlet的设置覆盖。如果你设置高于硬限制：5000行，硬限制仍然起作用。

#### 硬限制：每个报告5000行

所有dashlet的报告不能超过5000行。如果你需要更大值，你可以设置下列系统属性：
![硬限制](http://pic.yupoo.com/east4ming_v/Fhwjvk0s/14Nfau.jpg)

你可能需要设置该项在多个地方。下列描述了报告类型和相应的设置：

#### 客户端报告：本地安装的客户端

本地安装的客户端配置位是*dtclient.ini*,位于C:/Users/$username/.dynaTrace/dynaTrace $version/dtclient.ini(Liunx/Mac OS X 是 ~/.dynaTrace/..)

```ini
-vargs

-Dcom.dynatrace.diagnostics.reporting.maxTableRows=10000
-Xmx512M
```

直接增加该设置到*-vmargs*。

#### 每个报告最多50个dashlets

为了防止超大的报告导致性能问题而作此设置。当然，你可以创建多个有50个dashlets的报告。

#### 客户端报告：通过dynaTrace Server站点的Webstart客户端

没有本地安装，因此当你使用Webstart客户端时，必须在dynaTrace Server设置。位置：  C:\Program Files\dynaTrace\dynaTrace $version\server\conf\plugins\c.d.d.autoupdate.client.common_$version\common\plugin.properties.在文件末尾增加如下配置。

```properties
...osgi.user.area=@user.home/$$workdingdir
osgi.install.area = file:
com.dynatrace.diagnostics.reporting.maxTableRows=10000
```

### Server端报告：计划报告和REST报告

当你通过计划任务或REST接口创建报告时，dynaTrace Server创建的报告。如果必须要配置更高的限制。在*dtserver.ini*,位于$dynaTrace Installation\dtserver.ini,例如 C:\Program Files\dynaTrace\dynaTrace 5.5.0\dtserver.ini

```ini
-restartonfailure

-vmargs

-Dcom.dynatrace.diagnostics.reporting.maxTableRows=10000
-Xmx1920M
```

加到*-vmargs*之后。

## Troubleshooting

- 配置应用，server或客户端重启后，第一份报告触发后，你应该在日志文件里看到下面信息：

> 2015-14-03 09:26:53 INFO [ServerReportManager] Using non-default limit of table rows per report: '10000'
如果没有出现，验证配置文件，并且重启server和客户端来激活新的变更。

- 你也必须在dashboard或dashlet修改软限制，因为软限制仍然是100行。

- *dtclient.ini*文件只位于C:\Users.如果该文件位于像是这样的位置：C:\Program Files (x86)\dynaTrace\dynaTrace $version,删除掉。

### 非拉丁语脚本

要启用PDF报告的非拉丁语系脚本，需要设置系统属性com。dynatrace.diagnostics.reporting.pdf.english为*false*。这可能会导致连字符错误，但是允许从右到左书写。
取决于报告是由dynaTrace Client还是dynaTrace Server创建，对应的系统属性也必须设置在*dtclient.ini*或*dtserver.ini*。
