Title: NGINX 实战手册-安全-ModSecurity Web应用防火墙
Category: DevOps
Date: 2019-06-19 20:22
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX的Web应用防火墙功能.
Image: /images/nginx-ssl-certificate.jpg

## 2.9 ModSecurity Web应用防火墙

### 2.9.0 介绍

ModSecurity 是一个开源的web应用防火墙(WAF), 首次被构建仅Apache web server. 在2012年, 它作为NGINX的一个模块可供使用, 2016加入NGINX Plus作为一个可选功能. 本章将详细介绍使用NGINX Plus的动态模块功能安装ModSecurity 3.0, 使用开源NGINX安装ModeSecurity 2.9. ModSecurity 3.0比ModSecurity 2.x的安全和性能更出众. 当从开源运行ModSecurity 2.9, 因为它仍然是在Apache上构造, 因此需要比3.0更多的开销, 而3.0是基于NGINX原生设计的.  ModSecurity 3.0 只能用于NGINX Plus订阅.

### 2.9.1 为NGINX Plus安装ModeSecurity

> 略过

### 2.9.2 在NGINX Plus中配置ModSecurity

#### 问题

你需要配置NGINX Plus使用ModSecurity模块.

#### 解决方案

在NGINX Plus配置中启用动态模块, 使用`modsecurity_rules_file`来指向一个ModSecurity规则文件:

`load_module modules/ngx_http_modsecurity.so;`

`load_module`指令适用于主context, 意味着该指令可以在打开HTTP或Stream块之前使用.

开启ModeSecurity, 使用指定规则集:

```nginx
    modsecurity on;
    location / {
        proxy_pass http://backend;
        modsecurity_rules_file rule-set-file;
     }
```

#### 讨论

ModSecurity的规则可以阻止对常见的web servers和应用的漏洞利用. ModSecurity已知可以防御应用层的攻击, 如HTTP violations, SQL注入, 跨站脚本, 应用层, DDoS, 远程和本地文件攻击. 使用ModSecurity, 你可以订阅恶意用于的实时的黑名单, 来帮助在服务被攻击之前阻止问题. ModSecurity模块也可以启用日志帮助识别新的攻击模式和异常.

#### 参见

[OWASP ModSecurity 核心规则集](http://bit.ly/2fdZ7Dd)

[TrustWave ModSecurity 付费规则集](http://bit.ly/2eJYuAx)

### 2.9.3 源码安装ModSecurity

#### 问题

你需要在CentOS或RHEL系统上使用NGINX运行ModSecurity.

#### 解决方案

从源码编译ModSecurity和NGINX来使用ModSecurity模块.

首先升级security并安装依赖:

```shell
$ yum --security update -y && \
    yum -y install automake \
    autoconf \
    curl \
    curl-devel \
    gcc \
    gcc-c++ \
    httpd-devel \
    libxml2 \
    libxml2-devel \
    make \
    openssl \
    openssl-devel \
    perl \
    wget
```

接下来, 下载安装PCRE库:

```shell
$ cd /opt && \
    wget http://ftp.exim.org/pub/pcre/pcre-8.39.tar.gz && \
    tar -zxf pcre-8.39.tar.gz && \
    cd pcre-8.39 && \
    ./configure && \
    make && \
    make install
```

下载zlib源码并安装:

```shell
$ cd /opt && \
    wget http://zlib.net/zlib-1.2.8.tar.gz && \
    tar -zxf zlib-1.2.8.tar.gz && \
    cd zlib-1.2.8 && \
    ./configure && \
    make && \
    make install
```

下载ModSecurity源码并安装:

```shell
$ cd /opt && \
  wget \
  https://www.modsecurity.org/tarball/2.9.1/modsecurity-2.9.1.\
tar.gz&& \
  tar -zxf modsecurity-2.9.1.tar.gz && \
  cd modsecurity-2.9.1 && \
  ./configure --enable-standalone-module && \
  make
```

从源码下载安装NGINX, 并在配置脚本里包含你需要的所有模块. 本次我们的关注点是ModSecurity:

```shell
$ cd /opt && \
    wget http://nginx.org/download/nginx-1.11.4.tar.gz && \
    tar zxf nginx-1.11.4.tar.gz && \
    cd nginx-1.11.4 && \
    ./configure \
        --sbin-path=/usr/local/nginx/nginx \
        --conf-path=/etc/nginx/nginx.conf \
        --pid-path=/usr/local/nginx/nginx.pid \
        --with-pcre=../pcre-8.39 \
        --with-zlib=../zlib-1.2.8 \
        --with-http_ssl_module \
        --with-stream \
        --with-http_ssl_module \
        --with-http_secure_link_module \
        --add-module=../modsecurity-2.9.1/nginx/modsecurity \
    && \
    make && \
    make install && \
    ln -s /usr/local/nginx/nginx /usr/bin/nginx
```

这将会把ModSecurity 2.9.1 模块编译并和NGINX一起安装. 从现在开始, 我们可以使用`ModSecurityEnabled`和`ModSecurityConfig`指令:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    location / {
      ModSecurityEnabled on;
      ModSecurityConfig modsecurity.conf;
    }
}
```

NGINX server的配置会为`location /`启用ModSecurity, 并使用位于NGINX配置目录下的ModSecurity配置文件.

#### 讨论

这一节从NGINX源码编译, 并把ModSecurity编译到NGINX中. 推荐从源码编译NGINX的时候, 总是检查你是否使用了最新的稳定版的包. 通过之前的案例, 你可以使用有ModSecurity的开源版本的NGINX来构建你的开源web应用防火墙.

#### 参见

[ModSecurity源码](https://github.com/SpiderLabs/ModSecurity)

[Updated and maintained ModSecurity Rules from SpiderLabs](http://bit.ly/2eJYuAx)
