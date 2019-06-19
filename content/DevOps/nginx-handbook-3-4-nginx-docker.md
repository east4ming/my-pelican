Title: NGINX 实战手册-运维-在Docker 上部署
Category: DevOps
Date: 2019-06-19 20:28
Tags: nginx, devops, 译文, 最佳实践, docker
Summary: NGINX 实战手册系列文章的运维部分. 本文主要介绍如何在Docker 上部署.
Image: /images/docker_nginx-750x410.png

## 3.4 在Docker上部署

### 3.4.0 介绍

Docker是个开源项目, 会自动把Linux应用部署到软件容器中. Docker提供一个额外的抽象层, 在linux上自动化操作系统级别的虚拟化. 容器化环境已经对生产世界造成了巨大的变革. Docker和其他容器平台允许快速, 可靠, 跨平台的应用部署. 本章中, 我们会讨论NGINX官方NGINX Dockerjingxiang,创建你自己的Docker文件来运行NGINX, 在NGINX中使用环境变量, 通用Docker实践.

### 3.4.1 使用NGINX镜像快速运行

#### 问题

你需要使用Docker Hub中的NGINX镜像快速启动和运行.

#### 解决方案

```shell
$ docker pull nginx:latest
$ docker run -it -p 80:80 -v $PWD/nginx-conf:/etc/nginx \
                                   nginx:latest
```

#### 讨论

NGINX已经在Docker Hub上制作了一个官方Docker镜像. 官方Docker镜像很容易在Docker中启动和快速运行. 在本节中我们通过2个命令就能启动和运行NGINX 容器. 官方镜像是基于Debian Jessie Docker镜像. 但是你也可以选择基于Alpine Linux构建的官方镜像. 这些官方镜像的Dockerfile和源码可以在GitHub中找到.

#### 参见

[Official NGINX Docker image, NGINX](https://hub.docker.com/_/nginx/)

[Docker repo on GitHub](https://github.com/nginxinc/docker-nginx/)

### 3.4.2 创建一个NGINX Dockerfile

#### 问题

你需要创建一个NGINX Dockerfile, 用Dockerfile创建Docker镜像.

#### 解决方案

使用`CMD`来在镜像实例化为容器时启动NGINX. 你需要在前台运行NGINX. 要这么做, 需要启动NGINX使用`-g "daemon off;"`或增加`daemon off;`到配置. 本例中稍后使用`daemon off;`加到main context. 你也想调节你的access日志输出到`/dev/stdout`, 错误日志输出到`/dev/stderr`.

```dockerfile
FROM centos:7
# Install epel repo to get nginx and install nginx
RUN yum -y install epel-release && \
    yum -y install nginx
# add local configuration files into the image
ADD /nginx-conf /etc/nginx
EXPOSE 80 443
CMD ["nginx"]
```

目录结构如下所示:

```
.
├── Dockerfile
└── nginx-conf
    ├── conf.d
    │   └── default.conf
    ├── fastcgi.conf
    ├── fastcgi_params
    ├── koi-utf
    ├── koi-win
    ├── mime.types
    ├── nginx.conf
    ├── scgi_params
    ├── uwsgi_params
    └── win-utf
```

在本例中, 我选择直接吧nginx-conf目录下所有我的NGINX配置都添加到Dockerfile中.

#### 讨论

当你需要完全控制包的安装和升级, 你会发现创建自己的Dockerfile很有用. 常见操作是保存在你自己的镜像仓库中, 这样你会知道你的基础镜像在上生产之前是可靠的, 经过团队测试的.

### 3.4.3 构建NGINX Plus镜像

> 略

### 3.4.4 在NGINX中使用环境变量

#### 问题

为了在不同的环境中使用相同的容器镜像, 你需要在NGINX配置文件中使用环境变量.

#### 解决方案

使用`ngx_http_perl_module`来从你的环境的NGINX中设置变量.

```nginx
daemon off;
env APP_DNS;
include /usr/share/nginx/modules/*.conf;
...
http {
  perl_set $upstream_app 'sub { return $ENV{"APP_DNS"}; }';
  server {
    ...
    location / {
      proxy_pass https://$upstream_app;
    }
  }
}
```

要使用`perl_set`, 你必须安装`ngx_http_perl_module`; 你可以通过动态模块加载或从源码静态构建. NGINX默认从环境中擦除环境变量; 你需要在`env`指令中声明任何你不想移除的变量. `perl_set`指令有2个参数: 你想要设置的变量名和渲染结果的perl字符串.

下面是一个Dockerfile, 会动态加载`ngx_http_perl_module`, 从包管理工具安装该模块. 当从CentOS的包管理中安装模块, 他们被放在`/usr/lib64/nginx/modules/`目录, 配置文件会动态加载在`/usr/share/nginx/modules/`目录的模块. 这就是为什么上面的配置块中, 要包含完整的路径.

```dockerfile
FROM centos:7
# Install epel repo to get nginx and install nginx
RUN yum -y install epel-release && \
    yum -y install nginx nginx-mod-http-perl
# add local configuration files into the image
ADD /nginx-conf /etc/nginx
EXPOSE 80 443
CMD ["nginx"]
```

#### 讨论

当使用Docker, 典型实践就是利用环境变量来修改容器操作的方式. 你可以在NGINX配置文件中使用环境变量, 这样NGINX可以用于多个, 不同的环境.
