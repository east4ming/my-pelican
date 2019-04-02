Title: Dynatrace AppMon 实战手册 - 4.Dynatrace组件Linux系统配置为服务
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第四篇, 主要是将Dynatrace组件配置为系统服务.

配置为服务，可以在主机启动的时候自启动。

1. 复制Dynatrace相关脚本（$DT_HOME/init.d）到 /etc/init.d
2. 在脚本中定义**DT_RUNASUSER**及其他变量（如有必要，修改**DT_OPTARGS**和**DT_FE_OPTARGS**等）(**必需**)
3. 使用`chkconfig --add dynaTraceServer`  (如果是其他Linux版本，如Debian(Ubuntu,...)使用`sudo update -rc.d dynaTraceServerNonRoot defaults`)
4. 如果Analysis Server和Server位于同一台，则先启动Analysis Server，过10s左右，再启动Server。（可以再Sever的脚本前加入sleep 10）
