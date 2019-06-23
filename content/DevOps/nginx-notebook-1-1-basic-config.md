Title: NGINX 学习笔记-安装部署-基本配置
Category: DevOps
Date: 2019-06-23 15:10
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的安装部署部分. 本文介绍NGINX 安装部署的基本配置.
Image: /images/nginx-logo.png

# 基本配置

## 依赖

- GCC编译器
- Automake工具
- pcre库(支持rewrite模块)
- zlib库(支持gzip模块)
- openssl库(支持ssl模块)

**参考指令**

`yum -y install gcc gcc-c++ automake pcre pcre-devel zlib zlib-devel openssl openssl-devel`

## 目录结构

### nginx解压后软件包

- **src**: 源代码
- **man**: 帮助文件(可以通过`man nginx`查看)
- **html**: html文件
- **conf**: 配置文件
- **auto**: 脚本文件,和configure
- **configure**: 自动脚本程序

> :notebook:备注:
>
> configure 2项工作
>
> 1. 检查环境,根据环境检查结果生成C代码;
> 2. 生成编译代码需要的Makefile文件.
>

### nginx服务器软件目录

- **conf**: Nginx的所有配置文件
- **html**: Nginx服务器在运行过程中调用的一些html网页文件.
- **logs**: 日志
- **sbin**: nginx一个文件,即启动的主程序

> **可以在html目录下自定义一些网页文件,并在配置文件中配置发生什么情况时转到相应的文件**

## configure 脚本支持的常用选项

```
--prefix=<path>  指定安装路径,默认/usr/local/nginx

--user=<user>  未指定,默认nobody

--with-debug  启用Nginx的调试日志

--add-module=<path>  声明第三方模块的路径,用以编译刀Nginx服务器中

--with-poll_module  声明启用poll模块.poll模块是信号处理的一种方法.

--with-http_ssl_module  启用HTTP的ssl模块.

--with-http_stub_status_module  启用Server Status页.默认不启用

--http-proxy-temp-path=<path>  指定存放HTTP代理临时文件的路径

--without-http  声明禁用HTTP Server

--with-pcre=<dir>  指定pcre库源代码的路径.这样可以在**编译Nginx源代码的同时编译pcre库**,不需要提前安装pcre库

--with-zilb=<dir>  指定zlib库源代码的路径.同pcre

--with-openssl=<dir>  指定OpenSSL库源代码的路径.

```

> 清除上次编译的遗留文件 `make clean`

```shell
./configure

    --sbin-path=/usr/local/nginx/nginx

    --conf-path=/usr/local/nginx/nginx.conf

    --pid-path=/usr/local/nginx/nginx.pid

    --with-http_ssl_module

    --with-pcre=../pcre-8.40

    --with-zlib=../zlib-1.2.11

```
