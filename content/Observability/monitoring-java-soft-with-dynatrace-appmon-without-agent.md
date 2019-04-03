Title: 监控JAVA JMX 指标 - 通过Dynatrace AppMon而无需Agent
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 系列文章. 对于ActiveMQ, MuleESB, Jboss等JAVA软件, 如何通过JMX监控其常规指标和特定指标.

## 概述

在近期的中间件组会议中, 发现存在一个监控盲区, 即: **JBoss EAP 6.X和Wildfly 10的监控**. 目前CA Wily和Zabbix(Zabbix应该可以监控的)暂时无法实现对其监控, 需要Dynatrace对其进行监控.(有Agent和无Agent两种方式). 本次主要介绍**无Agent**的方式.

## 应用服务器端配置

JBoss EAP 6.X或Wildfly 10配置调整, **需要配置logmanager和暴露JMX Remote端口**. 如下:

对于Wildfly 10.1.0  (windows脚本, Linux下按照shell语法做相应修改, 下同)

```batch
rem # Set LogManager
set "JAVA_OPTS=%JAVA_OPTS% -Djboss.modules.system.pkgs=org.jboss.logmanager  -Djava.util.logging.manager=org.jboss.logmanager.LogManager -Xbootclasspath/p:D:\wildfly-10.1.0.Final\wildfly-10.1.0.Final\modules\system\layers\base\org\jboss\logmanager\main\jboss-logmanager-2.0.4.Final.jar -Xbootclasspath/p:D:\wildfly-10.1.0.Final\wildfly-10.1.0.Final\modules\system\layers\base\org\jboss\log4j\logmanager\main\log4j-jboss-logmanager-1.1.2.Final.jar"

rem # Set JMX Remote
set "JAVA_OPTS=%JAVA_OPTS% -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1090 -Dcom.sun.management.jmxremote.local.only=false -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false"
```

JBoss EAP 6.4

```batch
rem # Set LogManager
set "JAVA_OPTS=%JAVA_OPTS% -Djboss.modules.system.pkgs=org.jboss.logmanager -Djava.util.logging.manager=org.jboss.logmanager.LogManager -Xbootclasspath/p:D:\EAP-6.4.0\modules\system\layers\base\org\jboss\logmanager\main\jboss-logmanager-1.5.4.Final-redhat-1.jar -Xbootclasspath/p:D:\EAP-6.4.0\modules\system\layers\base\org\jboss\log4j\logmanager\main\log4j-jboss-logmanager-1.1.1.Final-redhat-1.jar"

rem # Set JMX Remote
set "JAVA_OPTS=%JAVA_OPTS% -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1090 -Dcom.sun.management.jmxremote.local.only=false -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false"
```

修改完成后重启对应的应用服务器.

## Dynatrace端配置

**说明:**

Dynatrace通过一个插件: **JMX Enhanced Monitor**来实现对JMX数据的收集.

要使用该插件, 需要做以下2步操作:

1. 创建**任务**, 通过该任务, 根据不同的JVM类型来抓取所有想要抓取的**监控指标**, 并生成一个包含相关**监控指标**的jar包到指定目录.
2. 再把该jar包以插件形式安装到Dynatrace Server上.
3. 创建**监视器**, 从对应的应用服务器上获取想要监控的指标.

最后, 通过监控到的指标, 可以实现 **监控面板展示/告警/报告导出**等功能.

**操作步骤:**

1. 在Dynatrace上, 通过安装插件**JMX Enhanced Monitor**来实现对数据的收集. 如下图:

    ![JMX监控插件](http://pic.yupoo.com/east4ming_v/ad38044d/358307e5.png)

2. 在具体的配置文件(如:CCIC2), 右键选择**编辑系统配置文件** → **任务** → **创建任务**. 如下图:

    ![创建任务1](http://pic.yupoo.com/east4ming_v/2310cada/9d4fc386.png)

3. 任务具体的配置如下:

    ![](http://pic.yupoo.com/east4ming_v/b2d66e68/e951a0be.png)

4. 在**Include MBeans Patterns**中, 编辑该配置, 如下图:

    ![包含MBeans](http://pic.yupoo.com/east4ming_v/3516c97c/54ece686.png)

5. 编辑执行该任务的频率和具体的组件. 如下图:

    ![](http://pic.yupoo.com/east4ming_v/bb7f8b32/d8dc5276.png)

6. **手动执行**该任务, 执行完成后, 右键查看该任务是否执行成功. 具体如下图:

    ![执行任务](http://pic.yupoo.com/east4ming_v/384547c0/1d6444d6.png)

7. 在第3步指定的路径的`mg/build`下找到生成的jar包. 如下图:

    ![生成的监控指标jar包](http://pic.yupoo.com/east4ming_v/0fe58827/9eef22a1.png)

8. **设置** → Dynatrace Server → **插件** → 安装插件, 选择上一步的jar包进行安装. 如下图:

    ![](http://pic.yupoo.com/east4ming_v/b5e54e54/ad19a4c1.png)

9. 在具体的配置文件(如:CCIC2), 右键选择**编辑系统配置文件** → **监视器** → **创建...**. 如下图:

    ![](http://pic.yupoo.com/east4ming_v/dec10b0f/193276e5.png)

10. 监视器的具体配置如下图:

    1. JMX Service URL的通用写法示例: `service:jmx:rmi:///jndi/rmi://127.0.0.1:1090/jmxrmi`
    2. 添加要监控的主机.

    ![](http://pic.yupoo.com/east4ming_v/a7fc275c/04c867d4.png)

11. 执行频率和具体的执行组件配置如下图:

    ![](http://pic.yupoo.com/east4ming_v/5e776a26/85260ee7.png)

12. 监控指标(测量结果)配置如下图:

    ![](http://pic.yupoo.com/east4ming_v/72fd31d7/4a3b783d.png)

13. 执行该**监视器**. 成功结果示例如下:

    ![](http://pic.yupoo.com/east4ming_v/058e36b4/86eae21e.png)

14. 至此, **无Agent监控方式**已配置完成. 后续可以根据这些收集到的指标进行**监控面板展示/告警/报告导出**等功能. 监控面板展示示例如下图:

    ![](http://pic.yupoo.com/east4ming_v/da0ed9f8/2bbec94e.png)

## 监控指标

1. 主机信息(物理内存和CPU. 需要JDK支持)
2. 内存使用相关信息(如: heap, perm, new区, old区等)
   1. 类加载相关信息
   2. GC相关信息
3. 线程相关信息(总线程,peak线程, 当前线程)
4. JAVA软件特定JMX信息(如:jboss的jboss相关信息, ActiveMQ的队列信息, Mule ESB的处理能力相关信息)
