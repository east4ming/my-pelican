Title: Dynatrace AppMon 实战手册 - 23.相关网络权限
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第二十三篇, 主要介绍Dynatrace实际使用过程中需要开通哪些网络权限.

## 网络

1. 建议Dynatrace的Agent与Collector放在同一网段或2者间无防火墙。
2. 建议Dynatrace Server与数据库放在同一网段，2者间无防火墙。
3. Dynatrace Server和Dynatrace Collector间可以有防火墙，需要开通对应的权限。

| From                | To                               | Port | 备注                                           | 协议 |
| ------------------- | -------------------------------- | ---- | ---------------------------------------------- | ---- |
| dynaTrace Agent     | dynaTrace Collector              | 9998 | 建议同一网段，无防火墙。则次端口权限无需开通。 | TCP  |
| dynaTrace Collector | dynaTrace Server                 | 6698 | **需要开通**                                   | TCP  |
| dynaTrace Server    | dynaTrace Memory Analysis Server | 7788 | 同一台机器或同一网段则无需开通。               | TCP  |
| dynaTrace Client    | dynaTrace Server                 | 2021 |                                                | TCP  |
| dynaTrace Server    | 数据库（以Oracle为例）           | 1521 | 其他DB开通对应端口                             | TCP  |

| Components to Connect                             | Port non-SSL | PortSSL or e. HTTP | Protocol | Comment                                                                                                                                                                                                                       |
| ------------------------------------------------- | ------------ | ------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent to Collector                                | 9998         |                    | TCP      | Or Agent to Server-embedded Collector if enabled for demo scenarios                                                                                                                                                           |
| Agent to Collector                                | 8042         | 8043               | HTTP(S)  | For AppMon 6.2 and later, the node.js Agent uses this connection. 1)                                                                                                                                                          |
| AppMon Web toFrontend Server                      |              | 9911               | HTTPS    | Port on which browser-based dashboardsget their data.                                                                                                                                                                         |
| Browser to Server                                 | 8020         | 8021               | HTTP(S)  | Web interface for RESTful Server administration, to start the Webstart Client.                                                                                                                                                |
| Client to Frontend Server                         |              | 2021               | TCP      | For AppMon 6.5and later, non-SSL connections are no longer supported.                                                                                                                                                         |
| Client to Frontend Server                         |              | 8023               | HTTP     | Tunnel via HTTP. Sent data is by default encrypted using the AES algorithm                                                                                                                                                    |
| Collector to Server                               | (6698)       | 6699               | TCP      | For AppMon 6.5 and later, non-SSL connections are no longer supported. For compatibility reasons with pre-6.5 collectors the 6698 plain port is still available and must be activated using the Client running in debug mode. |
| Collector to Server                               |              | 8033               | HTTP     | Tunnel via HTTP. Sent data is by default encrypted.                                                                                                                                                                           |
| Collector to Server                               | 8040         | 8041               | HTTP(S)  | For HTTP-based Agent connections 1)                                                                                                                                                                                           |
| Frontend Server to Server                         |              | 2031               | TCP      | The communication port between the Frontend Server and the backend server.                                                                                                                                                    |
| Memory Analysis Server to Server                  |              | 7788               | TCP      | For AppMon 6.5 and later, non-SSL connections are no longer supported.                                                                                                                                                        |
| Slave Web Server agent to master Web Server agent | 8001         |                    | UDP      | The UDP port on which the master Web Server Agent should listen for data packets of the slave Web Server Agent                                                                                                                |

> Important
>
> For performance reasons, do not pass communication between the AppMon Agent and the Collector through firewalls. Place a Collector as close as possible to the Agents.

## Set up E-Mail Communication

For more information, see [Email configuration](https://community.dynatrace.com/community/display/DOCDT65/Email).

## Set up AppMon Memory Analysis Server Communication

| [![img](https://community.dynatrace.com/community/download/thumbnails/221381541/ManageServersServicesAnalysisServer.png?version=1&modificationDate=1398370369357&api=v2)](https://community.dynatrace.com/community/download/attachments/221381541/ManageServersServicesAnalysisServer.png?api=v2) |
| ---------------------------------------- |
|                                          |

Use this page to configure the connection settings to the AppMon Memory Analysis Server. For more information, see [Set up a Memory Analysis Server](https://community.dynatrace.com/community/display/DOCDT65/Set+up+a+Memory+Analysis+Server).
