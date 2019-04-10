Title: Dynatrace AppMon 实战手册 - 17.Dynatrace与Tivoli整合
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第十七篇, 传统公司之前可能都有采购IBM Tivoli(或其他类似产品)做统一告警, 本文主要介绍Dynatrace与Tivoli的整合, 将Dynatrace的告警事件发送给Tivoli, 由Tivoli统一告警.

## 概述

Dynatrace与Tivoli整合是通过SNMP协议完成的。Dynatrace发送SNMP协议信息到Tivoli，Tivoli接收到信息后进行分析，根据Tivoli上相应的规则进行一系列的动作，如：发送告警邮件、告警短信等。

Dynatrace上有**SNMP Action Plugin** 插件，通过该插件来实现SNMP协议的发送。

![](http://pic.yupoo.com/east4ming_v/FXU473ky/medium.jpg)

要使用**SNMP Action Plugin**：

- 提供MIB库文件给SNMP目标系统的管理员。管理员会为其系统解析该文件。MIB库文件也会提供SNMP trap和你目标系统间的接口。
- 在Dynatrace Server设置里启用SNMP Action Plugin： **Dynatrace Server设置** -> **插件** -> **SNMP Action Plugin**。启用之后，SNMP action出现在**事件**行为列表中。

> :notebook:说明:
> Dynatrace SNMP 映射说明文档：[Dynatrace SNMP Mapping](http://cloud.189.cn/t/AfayAfvEjem2)

当前MIB库文件地址：[DYNATRACE-TRAP-MIB-V2](https://community.dynatrace.com/community/download/attachments/221381746/DYNATRACE-TRAP-MIB-V2?version=1&modificationDate=1432016056067&api=v2)。MIB为2种受支持的traps提供以下值：

> dynaTraceIncidentStart TRAP-TYPE
> ENTERPRISE dynaTrace
> VARIABLES (name, message, description, severity, violation, server, systemprofile, starttime)
> DESCRIPTION "Indicates that a new dynaTrace incident has begun."
> ::= 1
>
> dynaTraceIncidentEnd TRAP-TYPE
> ENTERPRISE dynaTrace
> VARIABLES (name, message, description, severity, violation, server, systemprofile, starttime, endtime, duration)
> DESCRIPTION "Indicates that a dynaTrace incident has ended."
> ::= 2

## 配置步骤

以配置**失败率太高**事件为例，说明事件如何通过SNMP协议发送给Tivoli。

1. 右击指定系统配置文件，弹出系统配置文件首选项 -> 左面版选择**事件** -> 右边点击**失败率太高**事件 -> 点击**编辑**，如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXU47qEb/ZZaXa.jpg)

2. 跳出**编辑事件规则**对话框。可以看到在下边**设置**里，默认的是基本设置，点击**高级配置**进入高级设置页面。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXU47xJD/c5CA3.jpg)

   ![](http://pic.yupoo.com/east4ming_v/FXU47CET/medium.jpg)

3. 在页面中点击**添加**，跳出如下界面：

   ![](http://pic.yupoo.com/east4ming_v/FXU47az8/medium.jpg)

4. 选中**SNMP Action Plugin**，下边出现一系列相关属性。根据对应的目标SNMP系统（如Tivoli的信息）来进行填写：

    1. **Target Host**
    2. **Target Port**
    3. **SNMP Version**
    4. **Community**
    5. **Maximum Number of Message Octets**

5. 完成后点击确定，然后在高级设置里，选择新配置的SNMP插件，设置发送SNMP trap信息 的严重性级别（一般、警告、严重）以及执行的条件（开始时、结束时、开始和结束时）。严重性级别一般警告配置邮件告警，严重配置邮件和短信告警，执行条件一般选择**开始和结束时**。如下图：

   ![](http://pic.yupoo.com/east4ming_v/FXU47iXN/PCCU0.jpg)

6. 后续工作由SNMP接受系统的管理员进行进一步的配置。包括确认消息送达，编写告警规则等。

## 其他配置说明

在某公司Dynatrace与Tivoli配置期间，出现了较多的问题。现在整理如下：

### 字符集编码

Dynatrace SNMP的编码格式为**utf-8**，且不可更改。

而该公司Tivoli的编码格式为**GBK**。

由于编码格式的不同，导致Dynatrace通过SNMP协议发送到Tivoli的内容，在有中文的地方发生**字段跳行**的情况。

为了尽量减少该问题，Dynatrace测量、事件等相关内容的名称和描述都尽量修改为**英文**，以此来减少跳行问题的发生。但是尽管所有的相关内容都改为英文，Dynatrace在发送告警的时候，会自动加入**超过了** 和**上限** 字样。具体见示例部分。

为了解决该问题，确定了如下的方案：

1. dynaTrace使用中文语言包（为了Dynatrace的易用性考虑）
2. 邮件告警使用dynaTrace自带的邮件告警服务
3. Severe级别、静态阈值部分告警通过Tivoli来实现短信告警。

之所以静态阈值部分可以采用Tivoli告警，有以下原因：

- 告警格式、字段、内容固定，即使有中文跳行，跳的行数也是相同的，可以通过Tivoli配置绕过该问题
- 由于动态告警以及Dynatrace自带告警无法手动进行触发，且这些告警的格式与静态阈值告警格式不同，所以并未将这些告警发送到Tivoli。

示例如下：

Dynatrace发给Tivoli的信息：

**HEX**格式内容：

> e8 b6 85 e8 bf 87 e4
> ba 86 20 57 65 62 4c 6f 67 69 63 20 39 2b 2f 45 4a 42 20 50 6f 6f 6c 20 54 69
> 6d 65 6f 75 74 20 54 6f 74 61 6c 20 43 6f 75 6e 74 20 3a 20 3c 6c 69 66 65 2d
> 73 65 72 76 69 63 65 5f 65 69 6e 73 75 3e 20 4a 44 42 43 5f 53 74 61 74 65 20 3c
> 61 6c 6c 2d 61 70 70 6c 69 63 61 74 69 6f 6e 73 3e 20 28 54 50 4c 69 66 65 5f
> 77 6c 73 5f 63 78 6a 6b 5f 6c 62 74 5f 33 36 5b 6c 62 74 61 70 70 53 65 72 76
> 65 72 31 5d 40 73 68 74 70 6c 73 65 65 70 6f 72 74 6c 62 74 30 31 29 20 e4 b8
> 8a e9 99 90

**utf-8** 格式内容：

> 超过了
> WebLogic 9+/EJB Pool Timeout Total Count : <life-service_einsu>
> JDBC_State <all-applications>
> (TPLife_wls_cxjk_lbt_36[lbtappServer1]@shtplseeportlbt01) 上限

**GBK**内容

> 瓒呰繃浜?WebLogic9+/EJB Pool Timeout Total Count : <life-service_einsu> JDBC_State<all-applications>(TPLife_wls_cxjk_lbt_36[lbtappServer1]@shtplseeportlbt01) 涓婇檺

经过排查，确定该字样位于：**oracle jre的lib库--rt.jar包中**。

> /path/to/dynatrace/dynatrace-6.2/jre/lib/rt.jar
>
> 具体位于：
>
> `com/sun/org/apache/xalan/internal/xsltc/compiler/util/ErrorMessages_zh_CN.class`

只要Dynatrace Server选择了中文语言，就会自动加入该字样。

同时，发现因为加入的字样类似，导致的**跳行**都是跳了固定的行数，所以我们在Tivoli上对跳了之后的行进行解析，得到了正确的告警信息。通过该方法绕过了字符集冲突的问题。

### HOSTNAME与IP映射

由于Dynatrace发送的告警信息都是具体的HOSTNAME而不是对应的IP。而Tivoli是通过IP来找到对应的系统并告警。所以，为了正确地告警，在Tivoli中加入了Dynatrace所监控主机的**HOSTNAME**和**IP**的映射表。

后续如有新增或调整监控主机，需要联系Tivoli的对应负责人进行相应调整。

示例如下：

> appserverxxx 10.1.1.xxx
>
> dzbd-app1 10.x.x.x
>
> hostnamexxx01 10.1.x.x

### 短信告警

短信告警格式如下：

**IP+服务器描述+系统+Weblogic Server+告警描述+当前值+发生时间**

> 示例（短信告警内容）：
>
> [XXXX公司]10.1.129.36:xx系统xx应用服务器1；xx系统；Weblogic服务器：TPLife_wls_cxjk_xx_xx[appServer1]发生告警：<life-service_einsu> WLS JVM FreeMemory is low；当前值：1698.515644564548已恢复！；发生时间：2016-05-11
> 18:40:31

### Severe级别静态告警阈值

目前的Severe级别静态阈值告警有：（该级别使用短信告警。）

> :notebook:TIPS：
> 目前已经实现各个系统的测量参数、告警阈值、邮件通知人的自定义。（如针对核心系统，活动线程数告警阈值比其他大）

1. Weblogic Hogging线程数过高     >50 告警
2. Weblogic JDBC连接池状态不正常
3. JVM剩余内存过小                    <50M 告警
4. WLS weblogic.kernel.System-MaxWaitTime 过长     >10min 告警

### Warning级别静态告警阈值

> 以下为初始的设置，后续可以根据实际的告警情况进行调整和优化。

1. 活动线程数     Warning：>250    （核心系统线程数为400，暂定：Warning： >300 )
2. JDBC连接延迟时间    Warning：>5s  Severe:>10s
3. JDBC失败重连        Warning：>5      Severe:>10
4. JDBC泄漏连接数    Warning：>15   Severe:>30
5. JDBC当前等待连接计数   Warning:>10  Severe:>30
