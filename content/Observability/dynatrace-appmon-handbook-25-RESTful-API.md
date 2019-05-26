Title: Dynatrace AppMon 实战手册 - 25.RESTful API
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第二十五篇, 主要介绍Dynatrace监控的RESTful API.

## REST 接口

Dynatrace Server 和 Dynatrace Client都通过REST接口提供管理功能。这些接口可以用于执行以下任务：

- 启停session recording
- 为系统配置文件切换活动配置
- 触发内存快照、线程快照及CPU采样
- 重启Dynatrace Server 和 Dynatrace Collector
- 执行传感器热部署
- 生成报告

> Dynatrace 6.1中，由于安全原因，对SSLv3的支持已经不再继续。在Java 7中，默认已经禁用对伪协议SSLv2Hello的支持。这也在RSET接口中得以体现。使用Java6或者更早版本运行的应用，如果他们通过HTTPS访问REST接口，也可能会受影响。为了能够使用Java 6访问REST接口，SSLv2Hello必须被禁用：
>
> ```java
> Set<String> protocols = new HashSet<String>(Arrays.asList(socket.getEnabledProtocols()));
> protocols.remove("SSLv2Hello");
> socket.setEnabledProtocols(protocols.toArray(new String[protocols.size()]));
> ```

### Server REST接口

#### 概览

Dynatrace Server 和 Dynatrace Client都通过REST接口提供管理功能。通过这些接口，你可以启动和停止session recording，触发内存和线程快照，创建报告等等。

你可以用默认的8020和8021端口，使用HTTP 1.1和HTTPS 1.1 访问所有的Dynatrace Server REST 接口。如何更改端口设置和如何启用/禁用REST接口参见“Setup Communication”（见dynaTrace 6.2 Documentation 525页）。

大多数接口通过HTML被暴露，可以通过浏览器访问。默认，HTML的接口访问地址为：<https://DT_SERVER:8021/rest/html/management/server>

下列主题描述了如何访问REST服务。

- Agent Groups (REST) (2438页)
- Agents and Collectors (REST) (2447页)
- 仪表板和报告 (REST) (2450页)
- “停机时间” (REST) (2459页)
- 事件 （REST) (2463页)
- 活动Sessions (REST) (2497页)
- 内存快照 (REST) (2468页)
- 性能仓库 (REST) (2479页)
- 插件管理 (REST) (2485页)
- 资源快照 (REST) (2490页)
- Server 管理 (REST) (2492页)
- 存储的Sessions (REST) (2500页)
- 系统配置文件 (REST) (2507页)
- 任务和监视器 (REST) (2511页)
- 测试自动化 (REST) (2512页)

#### HTTP响应码

HTTP状态响应码展示了你的访问的结果。*RFC 2616* 标准（[W3C](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html), [IETF](http://www.ietf.org/rfc/rfc2616.txt)描述了这些状态码。

例如，如果请求被成功收到，理解，并接受，REST接口返回2xx状态码。如果请求不能被Dynatrace Server理解，会返回4xx状态码。状态码5xx表示有server error在组织Dynatrace Server完成该请求。

下列是常见的响应码：

- **200** - OK：请求已成功。
- **201** - Created：请求被执行，一个新资源被创建。
- **202** - Accepted: 请求被接受处理，但是处理尚未完成。
- **204** - No Content: 请求已成功，但是响应没有entity-body。
- **400** - Bad Request: 一些请求参数不正确。
- **401** - Unauthorized: 需要一个合法认证头（基本认证），但是却没有。
- **403** - Forbidden: 请求的执行不被允许，例如：用户没有权限。
- **404** - Not Found: 一些实体找不到，如：系统配置文件，仪表板，Collector，或Agent。
- **500** - Internal Server Error: 具体信息请查看response body。
- **501** - Not Implemented: 请求的服务当前没有被执行。

#### 身份认证和授权

为访问Dynatrace REST接口，User Agent必须通过HTTP 基本认证证实它自己。[RFC2617](http://www.ietf.org/rfc/rfc2617.txt)描述了该认证技术。基于用户名，一个冒号(:)，和密码的串联的字符串的BASE 64 hash key必须被计算。*Basic*加上该hash key的字符串必须被设为HTTP请求的*Authorization* 头。参见[Wiki page](http://en.wikipedia.org/wiki/Basic_access_authentication) 获取更多信息。

如果用户成功被认证，Dynatrace Server检查该用户是否可以访问该REST接口。如果该用户没有*Web Service Interface Access*权限，返回HTTP状态码401(Unauthorized)。取决于被请求的服务，用户可能需要额外的权限（如：访问一个具体的仪表板或者系统配置文件。）

#### Agent Groups (REST)

##### Agent Groups

Dynatrace Server提供几个RESTful接口URL：`http://<server>:8020/rest/management/profiles/<profilename>/agentgroups/<groupname>` 来管理一个系统配置文件的Agent Groups。使用HTTP GET (2439页)来请求一个Agent Group的细节信息。使用HTTP PUT (2440页)来创建新的Agent Groups或者修改已经存在的Agent Groups。使用HTTP方法DELETE(2442页)来删除已存在的Agent Group。也有一个接口，用于list(2439页)一个具体系统配置文件的所有的Agent Groups。

###### List Groups

这个接口列出一个具体系统配置文件的的所有Agent Groups。

| GET | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups` | produces application/xml |
| --- | -------------------------------------------------------------------------- | ------------------------ |
|     |                                                                            |                          |

| 类型 | 参数            | 描述                   | Mandatory | 默认值 |
| ---- | --------------- | ---------------------- | --------- | ------ |
| 路径 | **profilename** | 相应的系统配置文件名称 | 是        |        |

> **请求URL**
> GET `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups`
> **响应内容**
>
> ```xml
> <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
> <agentgroups>
>     <agentgroupreference name="Business Backend Server (Java)" href="http://localhost:8020/rest/management
> /profiles/easyTravel/agentgroups/Business%20Backend%20Server%20(Java)" />
>     <agentgroupreference name="Customer Web Frontend (Java)" href="http://localhost:8020/rest/management
> /profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)" />
>     <agentgroupreference name="CreditCardAuthorization (C++)" href="http://localhost:8020/rest/management
> /profiles/easyTravel/agentgroups/CreditCardAuthorization%20(C++)" />
>     <agentgroupreference name="Payment Backend (.NET)" href="http://localhost:8020/rest/management/profiles
> /easyTravel/agentgroups/Payment%20Backend%20(.NET)" />
>     <agentgroupreference name="B2B Web Frontend (.NET)" href="http://localhost:8020/rest/management/profiles
> /easyTravel/agentgroups/B2B%20Web%20Frontend%20(.NET)" />
> </agentgroups>
> ```
>
> **响应代码**
> 200 OK

###### GET Group

在一个指定的Agent Group使用HTTP GET来获取XML展示的Agent Group。

| GET | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>` | produces application/xml |
| --- | -------------------------------------------------------------------------------------- | ------------------------ |
|     |                                                                                        |                          |

| 类型 | 参数            | 描述                | Mandatory | 默认值 |
| ---- | --------------- | ------------------- | --------- | ------ |
| 路径 | **profilename** |                     | yes       |        |
| 路径 | **groupname**   | 对应Agent Group名称 | yes       |        |

> 本例展示了Agent Group Customer Web Frontend (java)的XML描述如何被请求。返回的XML包含Agent Group名称，描述，相关Agent映射的引用。
>
> **请求URL**
> GET `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)`

**响应内容**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agentgroup name="Customer Web Frontend (Java)">
   <description>Web application which provides the customer web pages via JSF/icefaces technology. Accesses the siness backend via WebServices.></description>
   <agentmappingsreference href="http://localhost:8020/rest/management/profiles/easyTravel/agentgroups/stomer%20Web%20Frontend%20(Java)/mappings" />
</agentgroup>
```

> **响应代码**
> 200 OK

###### PUT Group

使用HTTP PUT接口创建或覆盖一个Agent Group通过发送XML格式作为请求的内容。请求内容的期望XML格式内容与响应HTTP GET接口的内容类似。需要有写入系统配置文件的权限。重载POST接口提供与HTTP PUT相同的输出。

| PUT  | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>`                | consumes application/xml |
| ---- | ----------------------------------------------------------------------------------------------------- | ------------------------ |
| POST | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>?httpMethod=PUT` | consumes application/xml |

agentmappingsreference元素没有被PUT接口显示。要增加一个Agent映射到Agent Group，使用Agent 映射的HTTP PUT接口（2445页）。不支持通过该接口重命名Agent Group。

| 类型 | 参数            | 描述                          | Mandatory | 默认值 |
| ---- | --------------- | ----------------------------- | --------- | ------ |
| 路径 | **profilename** |                               | yes       |        |
| 路径 | **groupname**   | 要创建或更新的Agent Group名称 | yes       |        |

> 本例演示如何修改已有的Agent Group Customer Web Frontend (Java)的描述。如果请求被成功执行，会返回状态码204(No Content)。
>
> **请求URL**
> PUT `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)`

**请求内容**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agentgroup>
    <description>This is a modified description.</description>
</agentgroup>
```

> **响应代码**
> 204 No Content
>
> 本例展示了如何创建一个包含描述的，叫做New Agent Group的新的Agent Group。Agent Group的名称通过路径参数指定，描述在XML内容中指定。如果请求执行成功，返回响应码201，然后头信息Location指定为刚创建的Agent Group的URL。
>
> **请求URL**
> PUT `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/New%20Agent%20Group`

**请求内容**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agentgroup>
    <description>This is a new agent group.</description>
</agentgroup>
```

> **响应代码**
> 201 Created
>
> **响应头**
> Location: `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/New%20Agent%20Group`

###### DELETE Group

使用HTTP DELETE接口来删除已有的Agent Group。需要有修改系统配置文件的权限。重载POST接口提供和HTTP DELETE相同的输出。

| DELETE | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>`                   |
| ------ | -------------------------------------------------------------------------------------------------------- |
| POST   | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>?httpMethod=DELETE` |

| 类型 | 参数            | 描述                    | Mandatory | 默认值 |
| ---- | --------------- | ----------------------- | --------- | ------ |
| 路径 | **profilename** |                         | yes       |        |
| 路径 | **groupname**   | 要删除的Agent Group名称 | yes       |        |

> 本例展示如何删除一个叫做Cunstomer Web Frontend (Java)的Agent Group。
>
> **请求URL**
> DELETE `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)`
>
> **响应代码**
> 204 No Content

##### Agent映射

与Agent Groups（2439页）类似，Dynatrace Server提供几个接口管理Agent映射。使用HTTP GET（2444页）来请求Agent映射的细节信息。使用HTTP方法PUT（2445页）和DELETE（2446页）来创建、修改和删除Agent映射。使用Lists 接口（2443页）来得到一个Agent Group的Agent映射列表。

###### List 映射

该接口列出一个Agent Group的所有Agent映射。

| GET | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>/mappings` | produces application/xml |
| --- | ----------------------------------------------------------------------------------------------- | ------------------------ |
|     |                                                                                                 |                          |

| 类型 | 参数            | 描述 | Mandatory | 默认值 |
| ---- | --------------- | ---- | --------- | ------ |
| 路径 | **profilename** |      | yes       |        |
| 路径 | **groupname**   |      | yes       |        |

> **请求URL**
> GET `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)/mappings`

**响应内容**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agentmappings>
    <agentmappingreference alias="CustomerFrontend_easyTravel" href="http://localhost:8020/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)/mappings/CustomerFrontend_easyTravel" />
        <agentmappingreference alias="easyTravel_CF" href="http://localhost:8020/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)/mappings/easyTravel_CF" />
</agentmappings>
```

> **响应代码**
> 200 OK

###### GET 映射

在一个指定的Agent Mapping使用HTTP GET来获得该Agent映射的XML格式描述。

| GET | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>/mappings/<mappingalias>` | produces application/xml |
| --- | -------------------------------------------------------------------------------------------------------------- | ------------------------ |
|     |                                                                                                                |                          |

| 类型 | 参数             | 描述                       | Mandatory | 默认值 |
| ---- | ---------------- | -------------------------- | --------- | ------ |
| 路径 | **profilename**  |                            | yes       |        |
| 路径 | **groupname**    |                            | yes       |        |
| 路径 | **mappingalias** | 请求的Agent Mapping的alias | yes       |        |

> 本例展示了如何请求CustomerFrontend_easyTravel的XML格式的Agent 映射。返回的XML描述了该映射匹配哪些agent名和主机名。
>
> **请求URL**
> GET `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20%28Java%29/mappings/CustomerFrontend_easyTravel`

**响应内容**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agentmapping alias="CustomerFrontend_easyTravel">
    <agentnamepattern>CustomerFrontend_easyTravel</agentnamepattern>
    <agentnamematchtype>starts</agentnamematchtype>
    <hostnamepattern />
    <hostnamematchtype>starts</hostnamematchtype>
</agentmapping>
```

> **响应代码**
> 200 OK

###### PUT映射

使用HTTP PUT接口来创建或覆盖Agent映射。需要有写系统配置文件的权限。重载POST接口提供与HTTP PUT相同的输出。

| PUT  | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>/mappings/<mappingalias>`                | consumes application/xml |
| ---- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| POST | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>/mappings/<mappingalias>?httpMethod=PUT` | consumes application/xml |

| 类型 | 参数             | 描述                                  | Mandatory | 默认值 |
| ---- | ---------------- | ------------------------------------- | --------- | ------ |
| 路径 | **profilename**  |                                       | yes       |        |
| 路径 | **groupname**    |                                       | yes       |        |
| 路径 | **mappingalias** | 需要创建或修改的Agent Mapping 的alias | yes       |        |

请求必须发送XML格式的Agent 映射。Agent 映射的HTTP GET请求可以查看需要的XML架构。*agentnamematchtype* 和 *hostnamematchtype* 元素可以有以下的其中一个值：*starts*，*ends*，*contains*，*equals* 或 *regex*。（详见Agent Group - Agent 映射（979页））。该接口不支持Agent映射重命名。

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agentmapping alias="CustomerFrontend_easyTravel">
    <agentnamepattern>CustomerFrontend_easyTravel</agentnamepattern>
    <agentnamematchtype>starts</agentnamematchtype>
    <hostnamepattern />
    <hostnamematchtype>starts</hostnamematchtype>
</agentmapping>
```

> 本例展示如何修改CustomerFrontend_easyTravel的Agent 映射。如果请求成功执行，返回状态码204(No Content)。
> **请求URL**
> PUT `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)/mappings/CustomerFrontend_easyTravel`

**请求内容**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agentmapping>
    <agentnamepattern>sampleApp</agentnamepattern>
    <agentnamematchtype>contains</agentnamematchtype>
    <hostnamepattern>machineX</hostnamepattern>
    <hostnamematchtype>contains</hostnamematchtype>
</agentmapping>
```

> **响应代码**
> 204 No Content
> 本例展示如何使用alias名New Mapping来创建一个新的Agent映射。如果请求被成功执行，返回响应码201，对应的创建Agent映射的URL会指定Location头信息。
>
> **请求URL**
> PUT `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)/mappings/New%20Mapping`

**请求内容**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agentmapping>
    <agentnamepattern>someprefix</agentnamepattern>
    <agentnamematchtype>starts</agentnamematchtype>
    <hostnamepattern>machineX</hostnamepattern>
    <hostnamematchtype>ends</hostnamematchtype>
</agentmapping>
```

> **响应代码**
> 201 Created
>
> **响应头信息**
> Location: `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)/mappings/New%20Mapping`
>

###### DELETE映射

使用HTTP DELETE接口来删除已经存在的Agent映射。需要有修改系统配置文件的权限。重载POST接口提供与HTTP DELETE相同的输出。

| DELETE | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>/mappings/<mappingalias>`                   |
| ------ | -------------------------------------------------------------------------------------------------------------------------------- |
| POST   | `https://<server>:8021/rest/management/profiles/<profilename>/agentgroups/<groupname>/mappings/<mappingalias>?httpMethod=DELETE` |

| 类型 | 参数             | 描述                       | Mandatory | 默认值 |
| ---- | ---------------- | -------------------------- | --------- | ------ |
| 路径 | **profilename**  |                            | yes       |        |
| 路径 | **groupname**    |                            | yes       |        |
| 路径 | **mappingalias** | 需要删除的Agent映射的alias | yes       |        |

> 本例展示如何删除Agent映射CustomerFrontend_easyTravel的alias。
>
> **请求URL**
> DELETE `https://localhost:8021/rest/management/profiles/easyTravel/agentgroups/Customer%20Web%20Frontend%20(Java)/mappings/CustomerFrontend_easyTravel`
>
> **响应代码**
> 204 No Content

#### Agents和Collectors (REST)

##### Agents

Dynatrace Server提供2个RESTful 接口与Dynatrace Agents交互。使用List Agents(2447页)接口来收集Dynatrace Agents的信息。使用Hot Sensor Placement接口来执行指定Dynatrace Agent的传感器热部署(2448页)

###### List Agents

该接口列出所有已知的Dynatrace Agents，并且提供诸如它们连接的Collector和其他元数据信息。

| GET | `https://<server>:8021/rest/management/agents` | produces text/xml |
| --- | ---------------------------------------------- | ----------------- |
|     |                                                |                   |

> **请求URL**
> GET `https://localhost:8021/rest/management/agents`

**响应代码**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<agents>
    <agentinformation>
        <agentGroup>easyTravelBackend</agentGroup>
        <agentId>-91443089</agentId>
        <capture>true</capture>
        <classLoadCount>4783</classLoadCount>
        <collectorinformation>
            <name>Embedded dynaTrace Collector</name>
            <host>GRABS</host>
            <connected>true</connected>
            <embedded>true</embedded>
        </collectorinformation>
        <configuration>easyTravel</configuration>
        <connected>true</connected>
        <eventCount>70</eventCount>
        <host>GRABS</host>
        <licenseInformation>License OK</licenseInformation>
        <licenseOk>true</licenseOk>
        <name>easyTravelBackend</name>
        <processId>6612</processId>
        <skippedEvents>0</skippedEvents>
        <skippedPurePaths>0</skippedPurePaths>
        <startupTimeUTC>1250107304703</startupTimeUTC>
        <supportsHotSensorPlacement>true</supportsHotSensorPlacement>
        <systemProfile>easyTravel</systemProfile>
        <technologyType>Java</technologyType>
        <totalClassLoadCount>0</totalClassLoadCount>
        <totalCpuTime>0.0</totalCpuTime>
        <totalExecutionTime>0.0</totalExecutionTime>
        <totalPurePathCount>0</totalPurePathCount>
    </agentinformation>
</agents>
```

> **响应代码**
> 200 OK

###### 传感器热部署

该接口执行ID为<agent_id>的Dynatrace Agent的传感器热部署。

| GET | `https://<server>:8021/rest/management/agents/<agent_id>/hotsensorplacement` | produces text/xml |
| --- | ---------------------------------------------------------------------------- | ----------------- |
|     |                                                                              |                   |

| 类型 | 参数         | 描述                    | Mandatory | 默认值 |
| ---- | ------------ | ----------------------- | --------- | ------ |
| 路径 | **agent_id** | 对应Dynatrace Agent的ID | yes       |        |

> 本例激活了ID为-86650354的Dynatrace Agent的传感器热部署。XML响应描述了请求被成功执行。
>
> **请求URL**
> GET `https://localhost:8021/rest/management/agents/-86650354/hotsensorplacement`

**响应内容**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<result value="true"/>
```

> **响应代码**
> 200 OK

##### Collectors

###### 列出Collectors

| GET | `https://<server>:8021/rest/management/collectors` | produces text/xml |
| --- | -------------------------------------------------- | ----------------- |
|     |                                                    |                   |

返回的XML包含关于已连接的collectors的根节点和子节点的详细信息。

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<collectors href="https://localhost:8021/rest/management/collectors">
  <collectorinformation href="https://localhost:8021/rest/management/collectors/Embedded%20dynaTrace%20Collector@GRABS">
    <connected>true</connected>
    <embedded>true</embedded>
    <host>GRABS</host>
    <name>Embedded dynaTrace Collector</name>
  </collectorinformation>
</collectors>
```

###### Collector细节

| GET | `https://<server>:8021/rest/management/collectors/<collectorname>` | produces text/xml |
| --- | ------------------------------------------------------------------ | ----------------- |
|     |                                                                    |                   |

返回的XML包括该collector的根节点的细节信息。

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<collectorinformation href="https://localhost:8021/rest/management/collectors/Embedded%20dynaTrace%20Collector@GRABS">
  <connected>true</connected>
  <embedded>true</embedded>
  <host>GRABS</host>
  <name>Embedded dynaTrace Collector</name>
</collectorinformation>
```

###### 重启和关闭Collector

Dynatrace Server提供2个REST接口来重启和关闭已连接的Dynatrace Collectors。都是HTTP POST请求。下列2个例子展示了如何重启和停止已连接到Dynatrace Server的collectors。

```
POST https://<server>:8021/rest/management/collector/<collectorname>/restart HTTP/1.1
POST https://<server>:8021/rest/management/collector/<collectorname>/shutdown HTTP/1.1
```

#### 仪表板和报告 (REST)

Dynatrace Server提供一系列的RESTful接口来通过HTTP请求创建仪表板报告。使用这个接口来取回不同文件格式的仪表板中的信息，并且通过灵活的参数来选择报告数据的源和时间段。
关于报告的概览信息和Dynatrace的报告功能，见报告(1966页)。

##### 生成仪表板报告

通过REST生成报告的语法如下：

| GET | `https://<server>:8021/rest/management/reports/create/<dashboardname>` |
| --- | ---------------------------------------------------------------------- |
|     |                                                                        |

###### 参数

你可以添加请求参数来完善报告。
> ​:heavy_exclamation_mark: 更改只应用在仪表板等级。单个dashlet（如数据源）的特殊配置不受这些参数的影响。

| 参数           | 描述                                                       | 强制 | 默认值                       |
| -------------- | ---------------------------------------------------------- | ---- | ---------------------------- |
| 类型(2451页)   | 指定请求输出类型                                           | no   | HTML                         |
| 格式(2451页)   | 指定用于选择的报告类型的报告格式                           | no   | 已选择的基于报告内部基本类型 |
| 过滤器(2451页) | 设置源的过滤器，但是会被指定的源过滤器覆盖。可以被指定多次 | no   |                              |
| 源(2452页)     | 负载仪表板的默认源                                         | no   |                              |
| 比较(2452页)   | 覆盖(如必要则激活)默认数据源的参照                         | no   |                              |

####### 参数细节
**type**
指定输出类型。指定类型可以在Reporting(1966页)找到或者可以通过REST列出(2454页)。
示例：
URI    `https://localhost:8021/rest/management/reports/create/demo?type=CSV`
这会创建一个CSV格式的，叫做**demo**的报告。

**format**
一些类型提供不同的格式。每种类型可用的格式可以在"每种类型支持格式列表"(2454页)找到。
示例：
URI    `https://localhost:8021/rest/management/reports/create/demo?type=HTML&format=HTML%20Paged`
这会创建一个叫做**demo**的HTML报告。

**filter**
Filters可以自定义报告使用的数据。关于filters的详细届时，参见REST Filters(2550页)。
示例：
URI    `https://localhost:8021/rest/management/reports/create/demo?filter=tf:Last5Min&filter=ag:AgentGroups?Browser`
这会创建一个dashboard demo的HTML格式的报告，时间为过去5min，Agent Group为**Browser**。

**source**
源可以覆盖报告的dashboard的源系统配置文件。
示例：
URI   `https://localhost:8021/rest/management/reports/create/demo?source=live:easyTravel`
这回创建**demo** dashboard的HTML格式的报告，使用活动session **easyTravel**作为源。

> ​:heavy_exclamation_mark:​ source参数的值是在Dynatrace Client上储存会话的名字。你可能需要encode一些字符来构造一个合法的URL。

**compare**
URI   `https://localhost:8021/rest/management/dashboard/Incident%20Dashboard?compare=stored:easyTravel%20baseline`
这个事件仪表板会比较默认源和储存的会话**easyTravel**。

**示例**

- 查询默认配置的本地Server的事件仪表板： `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard`
- 改变默认仪表板的源为live session easyTravel。 `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard?source=live:easyTravel`
- 对默认仪表板源应用web 请求过滤  `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard?filter=wr:/frontend/userlogin.do`
- 设置一个基线session作为比较源  `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard?compare=stored:easyTravel%20baseline`
- 过滤UserLogin和UserLogout事务。  `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard?filter=bt:UserLogin&filter=bt:UserLogout`
- 请求过去15min数据。  `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard?filter=tf:Last15Min`
- 请求昨天数据  `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard?filter=tf:Yesterday`
- 请求过去15s的数据  `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard?filter=tf:OffsetTimeframe?15:SECONDS`
- 请求from 2015-03-14 09:26 GMT to 09:27 GMT的数据。  `https://localhost:8021/rest/management/reports/create/Incident%20Dashboard?filter=tf:CustomTimeframe?1426339613000:1426339620000`

##### 仪表板信息

###### 列出可用仪表板

要得到可用仪表板，发送下列RESTful请求：
|     |                                                    |                   |
| --- | -------------------------------------------------- | ----------------- |
| GET | `https://<server>:8021/rest/management/dashboards` | produces text/xml |

返回的XML包含仪表板的根节点和子节点。*href*属性包含报告这个仪表板的链接。在特殊情况下，一个仪表板会把一个icon作为引用，icon可以请求，带有*icon*属性的链接。

> ​:heavy_exclamation_mark:​ 只会列出登陆用户可用的仪表板。没有权限的仪表板不会列出。

###### 仪表板Icon

一些预配置的仪表板引用了PNG，GIF，或JPEG格式的图标。使用下列请求来下载指定仪表板的图标：
GET    `https://<server>:8021/rest/management/dashboards/<dashboardname>/icon`

##### 类型和格式

###### 列出受支持的报告类型

报告类型是指由Dynatrace Server提供的报告功能中的一种输出格式，如PDF和HTML。报告类型可以支持多种报告格式，如HTML不同的排版，但是一般情况下每种报告类型只有一种报告格式。

|     |                                                       |                   |
| --- | ----------------------------------------------------- | ----------------- |
| GET | `https://<server>:8021/rest/management/reports/types` | produces text/xml |

返回XML包含一个*reporttypes*根节点，和列出可用类型的*reporttype*子节点。

**响应示例**

```XML
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<reporttypes href="https://localhost:8021/rest/management/reports/types">
    <reporttype id="HTML"/>
    <reporttype id="PDF"/>
    <reporttype id="CSV"/>
    <reporttype id="XML"/>
    <reporttype id="XLS"/>
    <reporttype id="XLSX"/>
    <reporttype id="XSD"/>
    <reporttype id="XSL"/>
</reporttypes>
```

###### 列出每种类型受支持的格式

|     |                                                         |                   |
| --- | ------------------------------------------------------- | ----------------- |
| GET | `https://<server>:8021/rest/management/reports/formats` | produces text/xml |

返回XML包含一个*reporttypes*根节点和列出可用仪表板的*reporttype*子节点。

**示例**
要得到可用的HTML报告的格式：
URL   `https://localhost:8021/rest/management/reports/formats/HTML`

返回：
**响应示例**

```XML
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<reportformats href="https://localhost:8021/rest/management/reports/formats/HTML">
    <reportformat id="HTML Report">
        <description>Produces a report in HTML format</description>
    </reportformat>
    <reportformat id="HTML Paged">
        <description>Produces a report in HTML format with tabs to quickly switch between the Dashlets</description>
    </reportformat>
</reportformats>
```

##### 扩展XML报告

XML报告可以像任何其他报告一样被创建。也有一个指定的XML报告接口（2455页）支持一些额外的参数。

##### XML报告（REST）

###### 介绍

除了常规的REST 报告（2450页），Dynatrace Server对于XML报告也支持另一种REST接口。它提供比常规接口更多的参数。XML报告也可以使用客户端报告(1973页)来生成。

> ​:heavy_exclamation_mark:​ XML REST报告与常规REST报告不同。一些参数列在下边，这些参数在其他报告类型和格式里不可用。

###### XML请求接口

创建XML报告的常用语法是：

| 请求类型 | HTTP GET                                                                  |
| -------- | ------------------------------------------------------------------------- |
| URI      | `http://DTSERVER:8020/rest/management/dashboard/DASHBOARDNAME?PARAMETERS` |

查看安装通信(525页)获取更多配置细节。

> ​:heavy_exclamation_mark:​ 请注意常规REST报告使用接口 /rest/management/reports/create/ 。

###### 参数

下列参数配置报告和仪表板。变更只应用在仪表板级别。对于单个dashlet的特定设置无法修改。
参数**source**， **compare**， **filter**在仪表板和报告(REST)(2451页)中有说明。

| 参数                    | 描述                                                                                                                    | 强制 |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---- |
| 源(2452页)              | 覆盖仪表板默认数据源                                                                                                    | no   |
| includeLayout(2456页)   | 设为*true*(默认为false)，额外的布局信息被添加，像是表的列顺序，列显示名称，或排序。(只有XML可用)                        | no   |
| 过滤器(2451页)          | 设置源的过滤器，但是会被指定的源过滤器覆盖。可以被指定多次                                                              | no   |
| 源(2452页)              | 负载仪表板的默认源                                                                                                      | no   |
| 比较(2452页)            | 覆盖(如必要则激活)默认数据源的参照                                                                                      | no   |
| purePathDetails(2457页) | 启用报告的全部细节，包括报告仪表板中一个或者所有PurePath的所有节点数据。这只会影响PurePath dashlet的报告。(只有XML可用) | no   |

####### includeLayout
*includeLayout*决定是否需要在XML报告里添加额外的布局信息。
*示例：*
URI    `http://localhost:8020/rest/management/dashboard/demo?includeLayout=true`
这会创建一个包含额外布局信息的XML报告，如下：

```XML
<layout>
  <sort field="exec" order="descending"/>
  <field order="0" name="state" display=""/>
  <field order="1" name="name" display="PurePath"/>
  <field order="5" name="agent" display="Agent"/>
  <field order="4" name="node_count" display="Size"/>
  <field order="8" name="exec" display="Duration [ms]"/>
  <field order="7" name="start" display="Start Time"/>
  <field order="9" name="agentid" display="Agent ID"/>
  <field order="10" name="tagid" display="Tag ID"/>
  <field order="6" name="application" display="Application"/>
  <field order="3" name="breakdown" display="Breakdown"/>
  <field order="2" name="response_time" display="Response Time [ms]"/>
</layout>
```

####### purePathDetails
*purePathDetails* 和PurePath dashlet中PurePath 树显示的是等效的。该参数只影响PurePath dashlet的报告。它可以选择所有的PurePath(purePathDetails=ALL)或者通过PurePath标识符(2457页)选择指定的Purepath。
*示例：*
URI    `http://localhost:8020/rest/management/dashboard/demo?purePathDetails=ALL`
这将会创建XML报告，包括demo仪表板(包含一个PurePath dashlet)的所有PurePath细节。
> ​:heavy_exclamation_mark:​  请求所有PurePath细节可能会产生巨大的数据量。导出所有PurePath会花费很长时间，取决于报告中PurePath的数量和节点。当导出所有PurePath数据时，Dynatrace Server的CPU开销可能会增加。

###### XML报告的PurePath 标识符

要选择你想看到细节的PurePath，你需要通过它的Agent ID和Tag ID来确定。要得到这些数据，打开PurePath dashlet，选择指定Purepath的**详细信息**。**Agent ID**和**Tag ID**会列出。你也可以再PurePath dashlet上显示该列。

| 部分 | 描述                                  | 强制 | 示例          |
| ---- | ------------------------------------- | ---- | ------------- |
| PA   | 十进制或十六进制('0x'开头)的Agent tag | yes  | PA=0x4ae37f41 |
| PT   | 十进制格式的tag 号                    | yes  | PT=0          |
*示例:*
下列请求会从demo仪表板中获取一个指定PurePath的详细信息：
URI    `http://localhost:8020/rest/management/dashboard/demo?purePathDetails=PT=1175239;PA=0xe1bfd3b9`

**返回的XML(节选)**

```XML
<dashboardreport name="demo" version="6.2.0.1140" reportdate="2015-03-18T13:44:21.006+01:00" description="">
  <source name="easyTravel" filtersummary="last 30 minutes (auto)"/>
  <data>
    <purepathsdashlet name="PurePaths" description="" displaysource="Base">
      <purepaths>
        <purepath state="OK" name="/CalculateRecommendations" agent="CustomerFrontend_easyTravel_8080@lnz126872d02:5872" node_count="6639" exec="3292.459228515625" start="Wed Mar 18 13:43:53 CET 2015" agentid="e1bfd3b9" tagid="1178204" application="easyTravel portal" breakdown="CPU: 844.514 ms, Sync: -, Wait: -, Suspension: 1,978.724 ms" response_time="0.25823116302490234"/>
        <purepath state="Transaction failed" name="/services/BookingService/storeBooking" agent="CustomerFrontend_easyTravel_8080@lnz126872d02:5872" node_count="49" exec="3008.294189453125" start="Wed Mar 18 13:43:05 CET 2015" agentid="e1bfd3b9" tagid="1175239" application="easyTravel mobile" breakdown="CPU: 832.091 ms, Sync: -, Wait: -, Suspension: 1,075.756 ms" response_time="3008.294189453125">
          <node method="doGet(javax.servlet.http.HttpServletRequest req, javax.servlet.http.HttpServletResponse resp)" class="com.dynatrace.easytravel.frontend.servlet.BackendServicesServlet" argument="/services/BookingService/storeBooking" agent="CustomerFrontend_easyTravel_8080@lnz126872d02:5872" api="easyTravel, Servlet" totaltime="3008.2942302301526" relativestart="0.0">
            <attachment type="EuWebRequestNodeAttachment">
              <property key="sessioncookie" value="2EB3EB92778753CF9A2C12BC2D0AA006"/>
              <property key="id" value="8"/>
              <property key="requestid" value="1882790301"/>
              <property key="responseid" value="1744252718"/>
            </attachment>
...
```

##### 示例

1. 为demo仪表板创建默认XML报告： `http://localhost:8020/rest/management/dashboard/demo`
2. 使用session 'easyTravel'，时间为'过去7天': `http://localhost:8020/rest/management/dashboard/demo?source=live:easyTravel!tf:Last7d`
3. 使用'easyTravel Baseline'作为比较源： `http://localhost:8020/rest/management/dashboard/Incident%20Dashboard?compare=stored:easyTravel%20Baseline`
4. 报告包含布局信息： `http://localhost:8020/rest/management/dashboard/demo?includeLayout=true`
5. 包含Agent ID xe1bdf3b9 和 Tag ID 1306756 的PurePath详细信息： `http://localhost:8020/rest/management/dashboard/demo?purePathDetails=PA=0xe1bfd3b9;PT=1306756`

###### XML Schema

响应被XML Schema指定，可以在Dynatrace Server上查到具体定义：
URI `http://DTSERVER:8020/rest/management/schema/dashboard`

#### 事件停机时间(REST)

##### 概览

在Dynatrace，如果超过指定阈值，事件规则可以被定义来执行行为(如发邮件)。某些情况下，你可能不想触发这些行为，比如系统备份，数据库镜像，server重启等等。你可以配置事件停机时间(1893页)来抑制这些规则。
使用Dynatrace客户端或者Dynatrace Server RESTful服务:  `http://<server>:8020/rest/management/profiles/<profilename>/incidentdowntimes/<downtimename>` 来管理事件停机时间。你可以通过发送HTTP GET请求来检查事件停机时间细节。你必须使用HTTP方法PUT来添加一个新的事件停机时间或者升级一个现有的停机时间。使用HTTP方法DELETE来删除事件停机时间。

##### GET 事件停机时间

|     |                                                                                                 |                           |
| --- | ----------------------------------------------------------------------------------------------- | ------------------------- |
| GET | `https://<server>:8021/rest/management/profiles/<profilename>/incidentdowntimes/<downtimename>` | produces  application/xml |

会得到一个已存在事件停机时间的XML展示。
**参数**
| 类型 | 参数         | 描述               | 强制 | 默认值 |
| ---- | ------------ | ------------------ | ---- | ------ |
| Path | profilename  |                    | yes  |        |
| Path | downtimename | 对应停机时间的名称 | yes  |        |

**示例**
