Title: NGINX 实战手册-运维-自动化
Category: DevOps
Date: 2019-06-19 20:33
Tags: nginx, devops, 译文, 最佳实践, docker
Summary: NGINX 实战手册系列文章的运维部分. 本文主要介绍如何使用其自动化.
Image: /images/docker_nginx-750x410.png

## 3.6 自动化

### 3.6.0 介绍

有很多方式来自动化NGINX和NGINX Plus的配置文件, 如: 使用配置管理工具或定时任务来从模板配置文件配置. 随着动态环境的增加, 自动化配置的需求变得更急需. 在上一章, 我们确信NGINX配置文件被配置后需要reload.在本章, 我们会讨论更进一步的使用NGINX Plus API和**Consul Template**的实时(on-the-fly)NGINX配置文件重配置.

### 3.6.1 使用NGINX Plus自动化

#### 问题

你需要为动态环境重实时配置NGINX Plus的load balance.

#### 解决方案

使用NGINX Plus API来重配置NGINX Plus upstream 池:

```shell
$ curl 'http://nginx.local/upstream_conf?\
  add=&upstream=backend&server=10.0.0.42:8080'
```

`curl`调用到NGINX Plus的请求, 请求一个把一个新的server加到`backend` upstream配置.

#### 讨论

更多第一次安装的细节见 3.8 章节, NGINX Plus提供一个API来重新实时配置NGINX Plus. NGINX Plus API允许从upstream 池中添加和移除server, 同时draining 连接. 你可以使用该API来自动化NGINX Plus的应用服务器的创建和释放的配置.

### 3.6.2 使用Consul Templating 自动化配置

#### 问题

你需要自动化NGINX配置来通过使用Consul在环境中做出变更.

#### 解决方案

使用`consul-template` daemon和一个模板文件来模板化NGINX配置文件:

```
upstream backend { {{range service "app.backend"}}
    server {{.Address}};{{end}}
}
```

这个例子是Consul模板文件的一个upstream配置块模板. 这个模板会遍历在Consul上标记为`app.backend`的节点. 对于Consul上的每个节点, 这个模板会使用那个节点的IP地址产生一条server指令.

这个`consul-template` daemon通过命令行运行, 可以被用于在每次配置文件被模板化变更后reload NGINX:

```shell
# consul-template -consul consul.example.internal -template \
template:/etc/nginx/conf.d/upstream.conf:"nginx -s reload"
```

该指令指示`consul-template` daemon 来连接到一个位于`consul.example.internal`的Consul 集群, 并使用在当前工作目录的名为`template`的文件来模板化该文件, 并输出生成的内容到`/etc/nginx/conf.d/upstream.conf`中, 然后在每次模板化文件变更时reload NGINX. `-template` 标志接受一个字符串,包括: 模板文件,输出位置,和运行模板过程后执行的命令; 这3个变量以冒号分隔. 如果运行的命令由空格, 确保使用双引号包裹. `-consul`标志指示要连接的Consul集群.

#### 讨论

Consul是一个强大的服务发现工具和配置仓库. Consul以key-value 对以类似目录的结构存储节点信息, 允许restful API交互.Consul也在每个客户端上提供一个DNS界面, 允许进行连接到集群的节点的域名查找. 一个单独的, 利用Consul集群的项目是`consul-template` daemon; 这个工具模板化在Consul 节点, 服务或 key-value对的文件变化. 这让Consul成为一个自动化NGINX的非常强大的选择. 使用`consul-template`你也可以指示该daemon在模板替换变更后来运行一个命令. 通过这样, 可以reload NGINX配置, 并允许NGINX配置在环境中生效. 通过Consul, 你可以在每个客户端上设置健康检查来检查关注的服务的监控状况. 通过失败检测, 你能够通过模板化你的NGINX配置来只给健康的主机发送流量.

#### 参见

[Consul home page](https://www.consul.io/)

[Introduction to Consul Template](http://bit.ly/2iosmkV)

[Consul template GitHub](https://github.com/hashicorp/consul-template)
