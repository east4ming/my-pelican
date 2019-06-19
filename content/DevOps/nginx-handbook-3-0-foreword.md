Title: NGINX 实战手册-运维-前言和介绍
Category: DevOps
Date: 2019-06-19 20:28
Tags: nginx, devops, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的运维部分. 这是前言部分.
Image: /images/docker_nginx-750x410.png

## 3.0 前言和介绍

在NGINX CookBook的第一部分, 主题是负载均衡和缓存. 第二部分是NGINX的安全功能, 如认证和加密. 第三部分集中于NGINX的运维问你, 包括部署, 性能调优和解决问题.

在这部分, 你会看到基于三个大型公有云的NGINX部署实践: Amazon Web Services(AWS), Google Cloud Platform(GCP), 和微软Azure, 包括如何自动化在AWS上部署. 如果你计划使用Docker, 也有相关内容.

安装也会深入讨论使用Puppet, Chef, Ansible和SaltStack的自动化配置管理. 也介绍了使用NGINX Plus API来实施重配置, 使用Consul进行服务发现和模版配置.

默认情况下, 大部分系统配置是基于兼容性而不是性能. 然后你要根据你的特定需求进行性能调优. 在本书中, 你会找到在保持兼容性的前提下, 详细的最大化NGINX性能的方法.

当我碰到部署问题, 我首先会看日志文件, 是很多调试信息的来源. NGINX有维护详细的, 高度配置化的日志来帮助你定位问题. 本书中包含NGINX日志的详细内容.

它会帮助你安装, 监控, 维护NGINX应用交付平台.
