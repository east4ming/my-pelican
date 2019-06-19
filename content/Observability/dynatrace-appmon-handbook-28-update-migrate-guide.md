Title: Dynatrace AppMon 实战手册 - 28.Dynatrace 6.5升级和迁移向导
Category: Observability
Date: 2019-06-19 19:00
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第二十八篇, 主要介绍Dynatrace AppMon 6.5的升级和迁移方法.

[TOC]

> 2017年2月22日

## 前言

本文档用于：

- 升级现有的Dynatrace环境到6.5，或者
- 迁移已存在的Dynatrace 6.5 Server 到另一台主机

### 1.准备迁移（见第一章）

开始之前，检查当前已安装（Servers, Collectors, Agents)来判定当前使用的版本，以及是否有组件可以直接升级到新版本。另外，检查**系统需求**来确定你正在使用受支持的硬件和平台。

### 2.安装新组件并迁移数据（见第二章）

安装新组件，**使用最新**的[*dynatrace-migration Tool*](https://files.dynatrace.com/downloads/migrationtool/dynatrace-migration.jar)来转移当前数据和配置至新版本。当你从命令行运行该工具时请检查所显示的版本！

你需要几步手工的操作和编辑来完成迁移。

### 3.如果需要，则升级Agents（见第三章）

大多数Agents会自动升级到最新版本。在某些情况下，你可能需要手动升级Agents。

### 4.最终检查和验证（见第四章）

启动Dynatrace AppMon并且查看是否Agents在发送数据，PurePaths和仪表板正确地显示。

## 1 准备升级

检查下列checklist来确保你已经做好迁移准备。

### 步骤一

检查已安装的Dynatrace的版本和安装类型：

- 对于5.6之前版本，你**必须**先迁移到6.2。具体见[《6.2升级向导》](https://community.dynatrace.com/community/display/DOCDT62/Upgrade+and+Migration+Guide)。
- 对于POC，需要[重新安装](https://community.dynatrace.com/community/display/DOCDT63/Installation+Overview)。
- 对于独立软件供应商版本（PTC Windchill),请使用供应商提供的文档。

### 步骤二

创建一个已安装的Collectors, Agents, Clients的详细清单，来审定升级的范围。

### 步骤三

验证[**系统需求**](https://community.dynatrace.com/community/display/DOCDT63/System+Requirements)是否符合。一些要点如下：

- Servers**只兼容**主版本相同，小版本相同或更小的Collectors。例如：一台6.1的Server可以和一台6.0的Collector正常工作，但是**不兼容**5.6或6.2的Collector.
- **推荐**使用**64位客户端**而不是32位的。查看*客户端配置*和*Webstart 客户端*获取更多信息。
- 迁移**不支持**Server内置的Collector。**升级之前**需要为当前版本安装一个stand-alone服务。特别是对于“开发团队版本”。
- 内置性能仓库**不支持**迁移。首先要切换到外置的，具体描述见[链接](https://community.dynatrace.com/community/display/DOCDT63/Performance+Warehouse+Administration)。
- 如果启用LDAP认证，用户需要至少称为一个Dynatrace LDAP组的一员用以登陆。查看[LDAP](https://community.dynatrace.com/community/display/DOCDT63/User+Permissions+and+Authentication#UserPermissionsandAuthentication-LDAP)获取更多信息。
- 如果你的Dynatrace和DC RUM整合，DC RUM必须>= 12.0.2.

### 步骤四

对于清单上的每个Agent，检查*Agent和新的Servers和Collectors的兼容性*（见1.1）。

推荐升级所有Agents，可能需要新功能来正常工作以及获取支持，来确保已知问题已经被修复。

> **Tip**
>
> 计划好利用已安排好的升级窗口来进行升级：
>
> - 必须能够重启Agent 组。

**注意项**：.NET和IIS Agent： 由于license的变动，所有.NET和IIS Agents在6.3之前的需要升级后重启只6.3或更高。

### 步骤五

**注意项**：如果当前的Dynatrace server安装路径<DT_HOME_OLD>,存在一个*server/instances*文件夹，并且你正在使用这些**Server实例**：该功能，dtserver和dtfrontendserver的*- instance*参数6.3版本已弃用。Collector实例仍然支持。

使用[该向导](https://community.dynatrace.com/community/display/APMDOC/Migrating+Server+Instances+to+Separate+Installations)，**升级前**检查迁移Server 实例到独立安装的需求。

### 步骤六

**注意项**：6.2主机监控发生重大更改。被监控的主机不在被映射到系统配置文件，而是在一个叫做**基础结构**的部分进行全局管理。

因为这些更改，迁移前被收集的历史主机监控数据和相关的系统配置文件在使用Dynatrace 6.2或以后版本将不再可以访问。

要使历史主机监控数据迁移后仍可以访问，具体步骤参考[*升级6.2后，来自升级前的主机度量无法显示*](https://community.dynatrace.com/community/display/DTKB/After+Upgrade+to+6.2%2C+Host+Metrics+From+Times+Before+the+Upgrade+Are+No+Longer+Shown)

### 步骤七

 检查Server sizing,如果从以下版本升级，请事先[联系support](https://support.dynatrace.com/) ：

- 5.6，并且*dtserver.ini*中*-Xmx*值大于14GB
- ≥ 6.0，并且在*dtserver.ini*或*dfrontendserver.ini*, *memory*的值不受支持。

### 步骤八

要证明是否正在使用**连续事务存储**。在客户端检查：**设置->Dynatrace Server->存储**

### 步骤九

- 要证明是否有安装额外插件：客户端：**设置->Dynatrace Server->插件**
- 要证明自监控Profile里的所有的**停机时间和事件规则**。

### 步骤十

**性能仓库数据库**和**Session存储**：

- 查看当前配置：从客户端：**设置->Dynatrace Server**，选择左侧面板：
    - **性能仓库**所有细节包括密码，因为6.1版本密码存储改变过，你需要迁移后重新输入密码。
- 该向导工作的一部分，要准备好创建备份。
- 检查[系统需求](https://community.dynatrace.com/community/display/DOCDT63/System+Requirements#SystemRequirements-pwh)，是否你的SQL DB server受支持：
    - 如果不支持，**升级前**创建**备份**并切换到受支持的DB
- 确认配置**性能仓库**的用户有权限创建和移除DBMS的表。

### 步骤十一

#### 会话存储

- 如果当前存储位置位于安装路径（默认的），并且你想保留sessions，为了简化session存储和未来的迁移，在迁移之前可以[移动session存储](https://community.dynatrace.com/community/display/DOCDT65/Move+Session+Storage+to+a+new+Disk+or+Directory)到一个2者（老的和新的安装）都可以访问到的独立目录。
- 确定当前配置：从客户端： **Settings -> Dynatrace Server**，选择左面版的**存储**
- 创建备份作为升级的一部分。

### 步骤十二

确定下列服务的密码：Email、LDAP、Proxy、DC-RUM、Gomez、数据库。

### 步骤十三

在现有的**Dynatrace Server**上停用license。可能需要升级现有的license。查看[license升级文档](https://community.dynatrace.com/community/display/DOCDT63/License+Upgrade)获取更多信息。

> 注意！
>
> 如果你使用z/OS Agents，（从6.3开始）不在需要额外的license（LMS - license管理系统）。取而代之的是你需要联系**license 管理**去获得需要数量的CICS和IMS agents 和/或 Java Agents加到你的Server license上。

### 步骤十四

迁移之前，需要下载软件：

- 对应应用平台和操作系统的[安装包](https://downloads.dynatrace.com/downloads/download.aspx?p=DT) (完整包 或 Server/Collector/Client/Memory Analysis Server 或只是Agent)
- 最新版的** dynatrace-migration Tool**.
- **最新的升级包**，如果可用，可以在6.5[下载列表](https://downloads.dynatrace.com/downloads/download.aspx?p=DT)的顶部找到。具体参考[安装升级包](https://community.dynatrace.com/community/display/DOCDT65/Install+an+Update)
- 如果Server无法联网，从[eServices](http://eservices.dynatrace.com/)下载**升级后的licenses**

### 步骤十五

如果正在使用自定义keys用于Dynatrace TLS通信（替换*keystore.jks*)或WebUI（通过*com.dynatrace.diagnostics.web.ssl.** 参数），准备好私钥和相应的证书链以防这些需要被重新导入。参见[自定义证书需求](https://community.dynatrace.com/community/display/DOCDT65/Custom+Certificate+Requirements)

### 步骤十六

你可以并行运行不同版本的Dynatrace来测试升级情况，另外要了解**并行运行配置需求**。

**下一步**：升级Server，Collectors，客户端（见第二章）。

### 1.1 Agent兼容矩阵

升级Agents取决于他们的类型：

- 当应用重启时，**Bootstrapped Agents**自动升级。
- 使用了**non-bootstrapped Agents**，需要手动升级。（安装到一个新的目录路径）当应用层被重启，Agent连接字符串必须被指定到新的路径。

要查看Agent的版本以及是否有引导程序，使用Dynatrace客户端的**驾驶舱 -> Agent概述**。

尽管老版本Agents连接新版本Collectors是支持的。但是Agents应该尽早升级到Collector的版本 -- 通过安装新的Agents并且重启apps。

*Agent/Collector 兼容性*

| Collector（横）/Agent(竖) | 6.0    | 6.1    | 6.2    | 6.3    | 6.5 |
| ------------------------- | ------ | ------ | ------ | ------ | --- |
| 5.6                       | OK     | OK     | OK     | OK     | OK  |
| 6.0                       | OK     | OK     | OK     | OK     | OK  |
| 6.1                       | n/a 1) | OK     | OK     | OK     | OK  |
| 6.2                       | n/a 1) | n/a 1) | OK     | OK     | OK  |
| 6.3                       | n/a 1) | n/a 1) | n/a 1) | OK     | OK  |
| 6.5                       | n/a 1) | n/a 1) | n/a 1) | n/a 1) | OK  |

1) 在非引导程序Agents之前升级Server和Collectors。

## 2 升级Server，Collectors，客户端

如果你需要迁移Server到新主机而不是升级到新版本，你只需要执行适当的步骤，例如，不需要停止和安装新的Collectors。

### 2.1 安装新的Server，Collectors和客户端

- 在所有相关机器上安装新的Dynatrace Server和Dynatrace Collectors和客户端。
- 应该被安装到**新的目录**，在该向导中被引用做<DT_HOME_NEW>。

**Windows**：使用完整安装包**自定义**选项或者使用Server, Collector, Client独立安装包。

> **重要**：Windows：在安装完成后，推荐手动启动Server, Collector和客户端。**不要在安装时启动这些组件。**
>
> [*NIX](https://community.dynatrace.com/community/display/DOCDT63/*NIX)：**不要**解压*.jar*。而是运行
> `java -jar <pathToInstallerJar>/dynatrace-6.5.0.<build>-linux-<bit>.jar`
>

自动化安装参见**无人值守（静默）安装**。

### 2.2 关闭老版本

1. 关闭老版本客户端，停掉老版本Server，Frontend Server，Collector和内存分析服务器服务。

   > **提示**：关于如何启动和停止Dynatrace 服务可以在[这儿](https://community.dynatrace.com/community/display/DOCDT63/How+to+Start+and+Stop+dynaTrace+Services+or+Daemons)找到。

2. 取消老版本Server，Frontend Server，Collector和内存分析服务器的自启动:

- **Windows**: **控制面板->管理员工具->服务**。在每个服务属性里，设置**启动类型**为**手动**。
- ***NIX**: 使用*chkconfig* 或者*update - rc.d *来禁用所有Dynatrace服务。

### 2.3 创建备份

准备期间进行配置信息收集：

1. 备份**性能仓库DB**
2. 备份**Session存储**
3. 在***NIX**，备份在*/etc/init.d*下的所有Dynatrace脚本。

*DT_HOME*的文件在下一步进行备份。

### 2.4 服务迁移（Server，Collector和内存分析服务器）

下载并在所有Server和Collector机器上使用最新[dynatrace-migration tool](https://files.dynatrace.com/downloads/migrationtool/dynatrace-migration.jar)。对于迁移的更多选项参见[dynatrace-migration Tool 细节](https://community.dynatrace.com/community/display/APMDOC/Migration+Tool+Details)或者运行`java -jar dynatrace-migration.jar`

#### 2.4.1 文件收集

使用*dynatrace-migration*创建迁移存档：

> **文件收集**
>
> ```shell
> java -jar dynatrace-migration.jar -migration -sourceDTHome "<DT_HOME_OLD>" -targetArchiveDir "<ARCHIVE_DIR>"
> ```

**<DT_HOME_OLD>**是老版本Dynatrace安装路径。名为<Server_name>_<creation_dateTime>.dtma的<MIGRATION_ARCHIVE>文件将会在<ARCHIVE_DIR>中被创建。

保留该生成文件作为永久备份。

#### 2.4.2 文件迁移

在目标主机， 要迁移所有Server和Collector实例<DT_HOME_NEW>，使用如下：

**推荐迁移方式**

```shell
java -jar dynatrace-migration.jar -migration -sourceArchive "<ARCHIVE_DIR>/<MIGRATION_ARCHIVE>" -targetDTHome "<DT_HOME_NEW>"
```

备份（文件转移到<DT_HOME_NEW>）,迁移日志会在*<DT_HOME_NEW>/migration/backup/* 创建一个新目录。

若果你在这些步骤遇到问题，可以获取支持或者考虑[手动文件迁移](https://community.dynatrace.com/community/display/DOCDT62/Manual+File+Migration)。

#### 2.4.3 编辑配置文件

最后， dynatrace-migration 会列出可能需要手动迁移到新版本的文件（如配置设置文件）。因此，相关的老版本文件被复制并加上后缀*.toBeMigrated* 。这些文件位于<DT_HOME_NEW>。**不要复用**这些老版本文件，因为6.3修改过boot bundles，将导致Server无法启动。

**以下是示例输出：**

```
There are some files left, which have to be migrated manually:
In C:\Program Files\dynaTrace\dynaTrace 6.5 :
 \dtanalysisserver.ini -> edit and integrate custom settings from old \dtanalysisserver.ini.toBeMigrated
 \dtcollector.ini -> edit and integrate custom settings from old \dtcollector.ini.toBeMigrated
 \dtfrontendserver.ini -> edit and integrate custom settings from old \dtfrontendserver.ini.toBeMigrated
 \dtserver.ini -> edit and integrate custom settings from old \dtserver.ini.toBeMigrated
 \server\selfmonitoring\dtselfmon.ini -> edit and integrate custom settings from old
\server\selfmonitoring\dtselfmon.ini.toBeMigrated
Do NOT re-use the old files, this may cause components not to start!
```

- *dtserver.ini* ：如果你正在升级，且使用连续事务存储，如果显式指定`-Dcom.dynatrace.diagnostics.memory.maxPurePathBufferSize=<x>`,则**不要**迁移该参数。
- 如果从 ＜ 6.1 升级，并且*dtserver.ini.toBeMigrated* 包含*-Dcom.dynatrace.diagnostics.SQLSERVERUSENTLMV2*，参考[该文章](https://community.dynatrace.com/community/display/DTKB/How+to+connect+the+Performance+Warehouse+to+a+MS+SQL+Server+via+Windows+Authentication),迁移该条目并且也需要新增2个条目到*dtfrontendserver.ini*.
- 迁移所有的-Xmx, -Xms, -XX:PermSize, 和 -XX:MaxPermSize条目。

> ​:warning: **自定义证书：** 如果ini文件包含*-Dcom.dynatrace.diagnostics.web.ssl.keystore*,则一个自定义web认证[被配置](https://community.dynatrace.com/community/display/DOCDT62/Configure+SSL+Communication)。不要带上该条目，而是在升级结束后使用新的[证书管理](https://community.dynatrace.com/community/display/DOCDT65/Certificate+Management)来roll out之前的证书。
>
> 如果修改*<DT_HOME_OLD>/server/conf/keystore.jks*，使用一个自定义证书用于通信，该证书将会被自动迁移。
>
> 如果两者都做过配置，推荐升级后使用[证书管理](https://community.dynatrace.com/community/display/DOCDT65/Certificate+Management)来切换到一个单一证书。

更多信息参见**Server配置**和**Collector配置**。

#### 2.4.4 注册并自动启动额外的Collector 实例

**关于多实例的信息扩展。**

如果你在老版本是使用Collector多实例：

**Windows**: 对于每个Collector实例，在老版本中使用相同的`<CollectorInstanceName>`,在目录<DT_HOME_NEW>中，执行：

```shell
dtcollector -service install -instance <CollectorInstanceName>
```

***NIX** ：在`/etc/init.d`中，对于每个Collector示例，会有一个老的启动脚本叫做`dynaTraceCollector<NN>` ， `<NN>`是数字。对于每个该文件：

- 记下变量*DT_OPTARGS*和*DT_INSTANCE*的值

- 使用新版本替换：

```
cp <DT_HOME_NEW>/init.d/dynaTraceCollector /etc
/init.d/dynaTraceCollector<NN>
```

- 编辑`/etc/init.d/dynaTraceCollector<NN>`并填写`DT_OPTARGS`和`DT_INSTANCE`的记录值

### 2.5 自动启动新服务

**仅限*NIX**：使用*chkconfig*或*update-rc.d*，确保新的Server，Collectors，内存分析服务器，和Frontend Server使用*/etc/init.d*脚本自动启动，并且权限是正确的。

### 2.6 客户端迁移

如果你在Dynatrace 客户端里有特殊设置，像是代理设置，比较<DT_HOME_OLD>和<DT_HOME_NEW>中的*dtclient.ini*,以及：

- **Windows**:`C:\Users\<username>\.dynaTrace\dynaTrace 6.5\`
- ***NIX**:  `~/.dynaTrace/dynaTrace 6.5/`

适用的属性仍然要延续。

### 2.7 启动新的Server组件

如果你配置过*DT_HOME*变量，把它升级到<DT_HOME_NEW>,并且之后启动Dynatrace Server和**Frontend Server**（6.0版本引入）。

### 2.8 启动新的客户端

在<DT_HOME_NEW>里启动*dtclient*或者使用[Webstart Client](https://community.dynatrace.com/community/display/DOCDT63/Webstart+Client): `http://<servername>:8020`。在**设置->Dynatrace Server->连接状态**面板配置，确保连接到正确的Dynatrace Server（hostname）。

### 2.9 激活新的Server的licenses

如过你需要代理服务器来访问互联网，手动配置[代理服务器设置来访问eServices的在线liensing站点](https://community.dynatrace.com/community/display/DOCDT63/Licensing+Details#LicensingDetails-proxysettings).

### 2.10 选择Server Sizing

license导入后，会显示选择不同的sizing选项（参见[Sizing设置](https://community.dynatrace.com/community/display/DOCDT63/Sizing+Settings)获取更多信息。）选择在准备阶段验证过的Sizing。**在启动新的Collectors之前**执行这一步骤很重要，可以避免内存溢出问题。

### 2.11 升级新的Dynatrace

检查[下载页面](https://downloads.dynatrace.com/downloads/download.aspx?p=DT)是否有Dynatrace 6.5的升级包，使用客户端[安装升级包](https://community.dynatrace.com/community/display/DOCDT65/Install+an+Update)，然后按照说明做。升级包安装好后会重启和升级Collectors和Agents。

### 2.12 连接性能仓库

在**设置->Dynatrace Server->性能仓库**，验证连接细节并且输入数据库授权信息来连接到老的数据库。

点击**测试**,如果DB连接状态正常，点击**连接**。

Server会自动升级schema和数据到最新版本。这可能会花费大概5分钟。

### 2.13 配置Session存储

如果你想迁移已存储的sessions，在**设置->Dynatrace Server->存储**修改目录到你的session存储数据。

### 2.14 启动新的Collectors

启动新的Collectors，然后在**设置->Dynatrace Server->Collectors**面板确保所有的Collectors已连接到新的Server。如果你应用过升级（到新的Server），你应该在当前的对话框中立刻重启Collectors，确保应用升级。

Dynatrace Server和Collector现在将接收Agent的连接。

**下一步**：升级Agents（见第三章）。

### 2.15 手动文件迁移

不推荐手动迁移文件。如果使用迁移工具出现问题，请开ticket。

## 3 升级Agents

### 3.1 升级Agents

那么推荐升级Agents到最新而且将需要接收升级包。

#### 3.1.1 Bootstrapped Agents(Java, .NET, HOST, Native ADK, Web Server, PHP, CICS, and IMS)

Bootstrapped Agents重启时自动升级。到那时，老的Agents会尝试连接运行中的 Collector/Server。参见在兼容性矩阵中关于重启考量的详细描述（见1.1）。

如果你从＜6.0升级，并且想使用[Controlled Update Rollout](https://community.dynatrace.com/community/display/DOCDT63/Updates),那么你必须重新安装Agents到**升级它们的bootstrap组件**（见3.3）。

如果你有 与你在升级的同一台主机上的bootstrapped Agents，它们将升级，但是会**继续使用<DT_HOME_OLD>**目录来恢复它们的配置。因此，需要手动迁移它们的配置文件到<DT_HOME_NEW>(新版本安装目录)或为了相关配置继续使用<DT_HOME_OLD>。查看特殊Agent 配置获取更多细节（见3.1.1下文）。

##### Bootstrapped Web Server Agents

使用正确顺序来重启Web Server Agent 服务和Web Server Agent是必要的。第一次重启Web Server Agent 服务并且等待直至重新连接。然后重启Web Server Agent。这个步骤是必须的以确保两个Agents都升级到正确的版本。对于老版本的，Apache Web Server自动启动Web Server Agent服务的Unix安装，Apache Web Server可能需要二次重启。

如果你想从客户端重启Webserver Agent 服务，那么你必须升级bootstrap(见3.3)。

##### NGINX Web Server Agent

6.2中，JSON偏移量文件包括比6.1更多的数据。如果NGINX binary包含debug标志，重命名JSON文件就好，Agent启动时它将被自动再次生成。然而，如果stripped NGINX binary被使用，偏移量文件需要在NGINX Agent重启前被手动再次生成，否则升级后的Agent将无法启动。

使用下列命令行重命名偏移量(offset)文件:

```shell
<AGENT_HOME>/agent/conf/ngx_offset_gen.sh <nginx binary> <nginx debug symbols file> <JSON offset file>
```

#### 3.1.2 Non-bootstrapped Agents需要手动升级（浏览器和移动APP ADK）

在[这儿](https://downloads.compuwareapm.com/downloads/download.aspx?p=DT)找到新的浏览器Agent安装包和新的ADK版本。

瞎子啊并应用新的Agent-only安装包升级到最新的浏览器Agent。

在移动APP开发环境，切换到新的ADK并部署新版本升级。

#### 3.1.3 z/OS Agents

它们可以被 bootstrapped 或 non-bootstrapped。参见**升级zOS Agents**（见3.4）。

### 3.2 重启Agents

除非你已经升级并手动重启Agents，否则请**对你所有相关的应用现在执行重启**来升级Agents。

**下一步**：最终检查（见第四章）

### 3.3 升级Bootstrap Agents

Dynatrace是6.5版本不支持bootstrap agents < 6.0 。 使用该向导升级6.0之前的 bootstrap agents到最新版本。

#### 3.3.1 准备

1. 从[downloads.dynatrace.com](https://downloads.dynatrace.com/downloads/download.aspx?p=DT)下载对应平台的新的agent安装包。
2. 备份当前agent的配置文件目录
3. 在你的目标平台上部署和安装agent靠近当前正在使用的agents安装。

#### 3.3.2 Bootstrap agent升级过程

##### Host Agent

1. 停掉所有老版本的host agent
2. 将*/conf/dthostagent.ini*（主要是名称和对应server）从老目录迁移到新目录。
3. 启动新的host agent。

##### Webserver Agent

1. 停掉老版本的web server agent
2. 将*conf/dtwsagent.ini*从老目录迁移到新安装目录。
3. 启动新的web server agent

##### Java Agent

1. 重新在应用配置里配置agent路径（如从-agentpath:/opt/dynatrace-5.6.0/agent/lib64/libdtagent.
   so=name=Application_Monitoring  到  -agentpath:/opt/dynatrace-6.2/agent/lib64
   /libdtagent.so=name=Application_Monitoring）。:light:你也可以安装和配置一个与版本无关的agent路径（如/opt/dynatrace-agent/)，并移除老版本，安装新版本到同一目录。
2. 重启应用。

##### .NET Agent

1. 安装好新agents后重启应用

##### zOS zLocal/zRemote agent

1. 升级zLocal/zRemote agents将自动升级bootstrap agents。请参考说明（见3.4）。

#### 3.3.3 卸载过时agents

- Linux：简单删除过时agents的安装目录
- Windows：使用添加/删除应用卸载过时agents。

### 3.4 升级zOS Agents

#### 3.4.1 前提条件

##### 升级Dynatrace Servers，Collectors，Agents和性能仓库

在启动z/OS Agents的任何迁移操作之前，先阅读通用**升级**（见前言）到6.5向导并创建一份详细的Dynatrace Servers，Collectors，其他Agents，性能仓库和其他组件的升级计划。为了减少维护开票，协调应用程序重启来配合这些升级。

> ​:warning: **重要**
>
> Dynatrace 6.2版本， z/OS Agent不先通过zRemote Agent则无法直接连接到Dynatrace Collector。使用zRemote Agent是为了减少z/OS上的CPU开销。如果你现在的6.2之前的z/OS Agent部署忽略了zRemote Agent，作为升级的一部分你需要安装它。更多信息参见**zRemote Agent**(见下文)。

##### License

你需要Dynatrace Server和z/OS Agents的有效licenses。参考[license 升级](https://community.dynatrace.com/community/display/DOCDT63/License+Upgrade)获取更多信息。z/OS Agent的license是基于MIPS的。参见**准备升级**（见第一章）和[license 升级](https://community.dynatrace.com/community/display/DOCDT63/License+Upgrade)获取更多信息。

对于任何Dynatrace 版本（预生产/测试中心或生产），z/OS license是有效的。如果硬件（“fingerprint”）发生改变（例如，加了一个CPU），license会失效，并且必须在14天内更新。

#### 3.4.2 升级步骤

1. 如升级描述（见前言）将Dynatrace Server和Collector优先升级到6.5，以此来升级主框架组件。新的zOS Agents一般无法与老的Dynatrace Collectors或Servers兼容，反而是新的Dynatrace Collectors或Servers通常可以和老的zOS Agents一起工作。

2. 按照标准Agent 安装步骤。这包括：运行JCL来下载agent 分发文件，运行SMP/E来为新版本填入目标数据集。更多信息，参考**下载并SMP/E 安装z/OS Agent组件**（见下文）。

3. 第二步之后，你可以选择下文的1或2的其中一个来做：

   1. 停掉当前zDC，并升级zDC认证库到6.5版。重启z/DC之前，你应该确保zDC参数*DTMSG_SMOSIZE*已经去掉注释，而且参数*DTMSG_QSIZE*已经被删除。这些参数控制无论信息已经队列进入zDC数据空间还是zDC 64位共享内存对象（SMO）挂起他们的写入，到Dynatrace Agent。       5.6版本，数据空间已经被弃用。如果你在5.6版本中自定义了ZDCSYSIN 样例，你可以跳过该步骤因为该样例已经包含了该变更。zDC启动后，CICS和IMS agents 应该在5分钟内注册。 **- OR -**
   2. 为zDC和zLocal（原名USS）Agent创建并行6.5环境。按照**安装zDC**（见上文）的指引。在并行6.5环境，当你迁移独立的CICS区域和IMS控制区域到新的zDC时,你可以继续运行老的z/DC，或者你可以优先测试几个区域来升级默认的zDC。如果多个zDC在运行，指定为DEFAULT（YES）的那个将被选中除非在CICS或IMS系统初始化字段指定了一个INITPARM参数，那样的话它必须使用一个独有名称：INITPARM=(ZDTPLT6x='xxxx')连接到zDC。

   > ​ :warning: **注意**
   >
   > - 有DEFAULT（YES）选项，每个LPAR只有一个zDC。
   > - 每个zDC的SUBSYSTEM_ID必须独一无二。
   > - zDC STEPLIB使用的库必须被授权。

4. 当bootstrap Agent 第一次连接到升级后的Dynatrace Collector/Server，会自动升级zLocal Agent。如果使用z/OS UNIX Agent的 non-bootstrap 版本，你必须运行 COPYAGNT来复制新版本到z/OS UNIX文件系统的相应执行位置。参考位于**安装zDC**中的COPYAGNT步骤（见上文）。

5. 因为Dynatrace新版本zDC兼容老的CICS和IMS agents，你不需要立刻升级所有的CICS区域和IMS控制区域。然而，如果你监控跨CICS区域或IMS控制区域的事务，这些相关区域应该agent版本相同，否则会有未完成的PurePath。因此，CICS区域和IMS控制区域的升级应该考虑应用组群来做。尽早计划升级所有的CICS区域和IMS控制区域，以此来使用最新Dynatrace版本的功能。

   1. 要升级CICS区域，使用新的PDS（或它的内容）来替换老的PDS（或它的内容）DFHRPL concatenation。

      ```
      // DD DISP=SHR,DSN=<hlq>.LZDT6 30.SZDTLOAD
      ```

   2. 要升级IMS控制区域，在JCL，执行IMS Agent注入程序，ZDTIINST，使用新的PDS（或它的内容）来替换STEPLIB PDS（或它的内容）。

      ```
      // DD DISP=SHR,DSN=<hlq>.LZDT6 30.SZDTAUTH
      ```

> ​:warning: **注意**
>
> - STEPLIB使用的库必须被授权。

关于Dynatrace组件兼容性列表，请参考[迁移故障排除](https://community.compuwareapm.com/community/display/DOCDT56/zOS+Agent+Troubleshooting#zOSAgentTroubleshooting-MigrationTroubleshooting)。

## 4 最终检查

### 4.1 检查配置

#### 4.1.1 应用自定义配置，不要被自动化的覆盖

##### 事件规则和停机时间

你需要重新定义Self-Monitoring系统配置文件的所有[停机时间](https://community.dynatrace.com/community/display/DOCDT63/Incidents+and+Alerting)和[事件规则](https://community.dynatrace.com/community/display/DOCDT63/Incidents+and+Alerting)。

##### 在自带项：传感器包 中重新应用修改项

dynatrace-migration不会迁移随着产品安装和分发的项，像是内置传感器包。因为这些在不同版本可能有改动，你不应该简单导出和导入它们，而是应该重新配置编辑。

##### 检查用户插件

在Dynatrace 客户端：**设置->Dynatrace Server**，检查是否所有的插件被迁移，是否需要重新安装。

##### 重新导入LDAP认证

如果额外认证（如为LDAP创建的CA或自签名证书）被导入到Dynatrace的keystore：

- server/conf/jssecacerts

重新导入证书到新的keystore。不要复制老的keystores，以此来避免通过潜在的被盗用的公有证书的安全漏洞。

在LDAP证书的案例中，你可以通过使用Dynatrace本地用户登陆并点击Dynatrace客户端：**设置->Dynatrace Server->用户->LDAP->测试连接**来重新导入之前的证书。

### 4.2 确认新的Dynatrace Server的运行

为确保新的Server正常运转，验证下列内容：

- **驾驶舱->状态概述->agent概述**中显示了所有的Agents：
    - 已连接
    - 有数据到达：水平滚动来验证**事件计数** 或 **类加载计数** （或2个一起）的变化
    - 如果安装了，有正确的Agent版本（6.5）和升级版本。
- 有PurePath
- 仪表板正确显示
- 如果迁移了Session存储，历史数据可以展现
- 如果使用自定义证书，通过Server的<http://localhost:8020/> 站点来验证。
- 验证这些服务和连机器工作：Email、LDAP、Proxy、DC-RUM、Gomez
- 查看**开始中心 -> 管理**的告警和错误。

> ​:ballot_box_with_check: **恭喜！**
>
> 迁移完成！

## 5 故障排除

### 5.1 常见问题

#### 什么版本Agent在运行

Server/Collector升级后，Agent bootstrap 升级部分现有Agent，但是老版本Agents会一直运行直到你重启了应用。

请准备一个应用层的重启计划/协调。

你可以在**驾驶舱->Agent概述**里找到Agent版本信息（bootstrap和活动部分）。

#### 我的性能仓库DB schema是哪个版本

当新的Dynatrace Server连接到老的性能仓库DB时，Dynatrace DB schema被升级。因此，如果你不确定版本，在连接前检查一下是个好主意。

对于SQL Server，例如：

```sql
SELECT * FROM dynatrace6 5.dbo.version;
```

#### 性能仓库DB schema向后兼容吗

不兼容。请使用DB备份进行回滚。

#### 升级后PurePath丢失

如果升级时没有迁移类缓存，且有丢失的PurePath或者PurePath包含`<unknown>`节点，尝试重启相关应用。需要重启**2次**来避免该问题。

#### 为什么dtserver.ini和dtfrontendserver.ini中的内存设置被忽略甚至移除

从Dynatrace 6.0开始，‘-Xmx’和‘-Xms’ VM参数被忽略。请通过**设置->Dynatrace Server->设置面板->Sizing**来选择合适的sizing。更多信息，见[Sizing 设置](https://community.dynatrace.com/community/display/DOCDT63/Sizing+Settings)。

### 5.2 Dynatrace 支持

如果需要更多支持，请访问我们的**支持页面**。
