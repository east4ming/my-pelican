Title: NGINX 实战手册-运维-实用运维Tips和总结
Category: DevOps
Date: 2019-06-19 20:39
Tags: nginx, devops, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的运维部分. 本文主要介绍NGINX运维的实用运维Tips和总结.
Image: /images/docker_nginx-750x410.png

## 3.11 实用运维Tips和总结

### 3.11.0 介绍

最后章节会包括使用运维tips和本书的总结. 通过这三个大部分, 我们讨论了与运维工程师有关的很多想法和概念. 然而, 我认为再多讲一点会有助于理解的更加全面. 在本章, 我会确保你的配置文件干净和简洁, 以及如何调试配置文件.

### 3.11.1 使用 Includes 来缩减配置

#### 问题

你需要清理大量的配置文件来保证你的配置文件以模块化的配置集分组.

#### 解决方案

使用`include`指令来引用配置文件, 目录或通配符:

```nginx
http {
    include config.d/compression.conf;
    include sites-enabled/*.conf
}
```

#### 讨论

> 略

### 3.11.2 调试配置

#### 问题

从NGINX server , 你得到的非预期的结果.

#### 解决方案

调试配置, 记住以下建议:

1. NGINX进程请求查找最匹配的规则.
2. 你可以打开调试日志. 对于调试日志, 你需要确保你的NGINX包配置了`--with-debug` flag. 大部分常见包都有; 但是如果你构建你自己的包, 或在运行一个最小化的包, 你可能至少需要再次仔细检查. 一旦你确定了你有debug, 你可以设置`error_log`指令的日志级别为`debug`: `error_log /var/log/nginx/error.log debug;`
3. 你可以为特定的连接启用调试. `debug_connection`指令在`events`上下文是合法的, 使用IP或CIDR range作为参数. 该指令可以声明多次来添加多个要调试的IP地址或CIDR ranges. 这在生产环境, 但是调试所有连接会导致性能下降的情况下, 调试一个问题会很有用
4. 你可以调试特定的virtual servers. 因为`error_log`在`main` `http` `mail` `stream` `server` 和`location`上下文都有效. 你可以在你需要调试的上下文设置`debug`日志级别.
5. 你可以启用core dumps, 来从中获取backtraces. Core dumps可以通过操作系统启用, 或通过NGINX配置文件.
6. 你可以使用`rewrite_log`记录rewrite 声明的日志: `rewrite_log on;`

#### 讨论

NGINX能做很多神奇的配置, 但是也有性能下降的风险. 调试时, 确保你知道如何通过你的配置来追踪你的请求; 如果有问题, 增加调试日志级别来帮助分析. debug日志时相当详细, 找出NGINX对你的请求做了什么以及你的配置在哪儿出错了很有帮助.

#### 参见

[NGINX如何处理请求](http://bit.ly/2crNKVM)

[管理员调试向导](http://bit.ly/2iQYNsZ)

[Rewrite log](http://bit.ly/2j96jAH)

### 3.11.3 总结

这本书的三个部分集中于高性能负载均衡, 安全, 以及部署和维护NGINX和NGINX Plus servers. 这本书展示了NGINX应用交付平台的一些最强大的功能. NGINX会继续开发神奇的功能, 保持赛道领先.

这本书展示了很多"简短食谱", 允许你对指令和模块(这些让NGINX成为当今网络之心)有更好的理解. NGINX server不仅仅是web server, 不仅仅时反向代理, 而是一个完整的应用交付平台, 完全有能力通过认证, 并在未来环境中使用.  请知悉.
