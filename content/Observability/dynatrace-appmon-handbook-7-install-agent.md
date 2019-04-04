Title: Dynatrace AppMon 实战手册 - 7.Dynatrace agent安装
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第七篇, 主要是Dynatrace agent的安装.

[TOC]

## Server 端配置

1. 编辑系统配置文件
    ![编辑系统配置文件](./images/appmon-install-agent-1.png)
2. 新建Agent组
    ![新建agent组](./images/appmon-install-agent-2.png)
3. 设置传感器映射关系
    1. ▽ 与agent名字匹配：
        ![与agent名字匹配](./images/appmon-install-agent-3.png)
    2. ▽ 高级设置：取消自动生成heapdump，将解析度设为最低，降低系统开销：
        ![高级设置](./images/appmon-install-agent-4.png)
4. ▽ 设置放置哪些传感器, 根据实际需要选定传感器种类：
    ![传感器种类](./images/appmon-install-agent-5.png)
5. 配置上一步放置的传感器的属性
    ![传感器属性](./images/appmon-install-agent-6.png)
    1. ▽ JDBC传感器设置：将SQL命令捕获长度设为10240：
        ![jdbc 10240](./images/appmon-install-agent-7.png)
    2. ▽ Java Logging传感器设置，增加几种级别的日志捕获：
        ![java传感器配置](./images/appmon-install-agent-8.png)
    3. ▽ Servlets传感器设置：
        ![servlet传感器设置](./images/appmon-install-agent-9.png)

其他传感器默认设置即可。

## 安装 Agent

> :notebook:说明:
> 此处以**dynatrace appmon 6.2**版本举例, 请根据实际情况换成对应版本的安装包.

1. 上传`dynatrace-agent-6.2.0.1239-unix.jar`.  
2. `java  -jar dynatrace-agent-6.2.0.1239-unix.jar` （java版本必须与app server使用的相同），安装过程中修改安装路
径，eg:`/tpsys/dynatrace/dynatrace-6.2`
3. 将agent嵌入到java中间件(如:weblogic)实例中：在启动脚本的环境变量`USER_MEM_ARGS`中添加，`-agentpath:/tpsys/dynatrace/dynatrace-6.2/agent/lib64/libtagent.so=name=TPLife_wls_lbt_10.94.12.232_8001,server=10.94.21.140:9998`（说明：name表示设置该agent的名字，server表示collector）
4. 重启java中间件生效。

## TIPS

确认agent与哪个collector相连

![](./images/appmon-install-agent-10.png)

![](./images/appmon-install-agent-11.png)
