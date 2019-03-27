Title: Oracle WebLogic Server 11.1.1.9发布说明
Date: 2019-03-14 22:06
Category: Java
Tags: WebLogic, 译文, java
Slug: oracle-webLogic-server-11.1.1.9-release-notes
Authors: HelloWorDomain
Summary: 这是Oracle WebLogic Server 11.1.1.9发布说明

[参照链接](https://docs.oracle.com/middleware/11119/wls/WLSRN/issues.htm#WLSRN114)

## Oracle WebLogic Server问题
本章节描述了Oracle WebLogic Server相关的问题。它包含以下主题。
一般性问题和解决办法
管理控制台问题和解决办法
Apache Beehive支持问题和解决办法
集群问题和解决办法
配置问题和解决办法
连接器（资源适配器）问题和解决办法
控制台扩展问题和解决办法
核心服务器和核心工作管理器问题和解决办法
部署问题和解决办法
EJB问题和解决办法
示例问题和解决办法
HTTP问题发布/订阅服务器问题和解决办法
安装问题和解决办法
JavaEE问题和解决办法
JDBC问题和解决办法
JMS问题和解决办法
JBDI问题和解决办法
JSP和Servlet问题和解决办法
JTA问题和解决办法
Java虚拟机（JVM）和解决办法
监测问题和解决办法
节点管理器问题和解决办法
操作、管理和受管理问题及解决办法
Oracle Kodo问题和解决办法
插件问题和解决办法
协议问题和解决办法
RMI-IIOP问题和解决办法
安全问题和解决办法
SNMP问题和解决办法
WebLogic Server上Spring框架的问题和解决办法
系统组件体系解救（SCA）问题和解决办法
升级问题和解决办法
Web应用程序问题和解决办法
WebLogic Server脚本工具（WLST）问题及解决办法
!!!
Web服务器插件问题和解决方法
Web服务和XML问题及解决办法
文件 Errata
>注：
>获取WebLogic Server 11g（10.3.6）修复的Bug列表，请在直属库字段中输入以下文档ID 1302753.1
### 一般性问题和解决办法
本章节介绍以下问题和解决办法

* 使用Safari时，多字节字符在文件名中显示错误
* Oracle WebLogic的版本号
* Oracle ojdbc14.jar文件更改为ojdbc6.jar
* 强密码强制执行可能导致WLST离线脚本出现问题
* 在土耳其地区，mds初始化失败
* 管理服务器在EM控制台上报告“太多打开文件”消息
* 适用于10.3.5.0 Oracle WLS通用安装的Sun JDK 6 U35-B52的可用性。
* IBM JDK SR16 FP3或 JDK 7.0 SR8 FP10修复程序的可用性
#### 使用Safari时，多字节字符在文件名中显示错误
**平台：** 全部
当使用Safari浏览器下载内容时，如果文件名包含多字节字符，则这些字符在文件中显示为乱码
**解决方案**
在受管服务器上设置` UserHeaderEncoding` 为 `true` .
使用如下WLST命令实现：
```
connect("admin_name", "admin_password", "t3://localhost:port")
edit()
startEdit()
cd("Servers/server_name/WebServer/server_name")
set("UseHeaderEncoding", "true")
save()
activate()
exit()
```
#### Oracle WebLogic Server 版本号
**平台：** 全部
Oracle融合中间件11g包含Oracle WebLogic Server 11g. Oracle WebLogic Server版本为10.3.6.
#### Oracle ojdbc14.jar文件更改为ojdbc6.jar
**平台：** 全部
Oracle ojdbc14.jar 更改为为ojdbc6.jar，使用JDK 5或者JDK 6，因此，您对ojdbc14.jar的任何显示引用都必须更改为ojdbc6.jar
#### 强密码强制执行可能导致WLST离线脚本出现问题
**平台：** 全部
在此版本的WebLogic Server中实施强密码实施（最少8个字符，带有一个数字或特殊字符），现有脚本可能遇到问题。
**解决方案**
* 将`ACKWARD_COMPAT_PW_CHECK`境变量设置为`ture`.
* 使用WLST时，引用参数`-Dbackward.compat.pw.check=true`
<未完待续>
Oracle建议您更改密码以复核新的密码要求，因为此变量和选项将在未来的WebLogic Server版本中删除。
#### 在土耳其地区，mds初始化失败
**平台：** 全部
