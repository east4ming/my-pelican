Title: NGINX 学习笔记-安装部署-基础配置
Category: DevOps
Date: 2019-06-23 15:30
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的安装部署部分. 本文介绍NGINX 的基础配置.
Image: /images/nginx-logo.png

## 3 Nginx 基础配置

```nginx
#user  nobody;
worker_processes  1;                        # 全局块

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;

events {                                    # events块
    worker_connections  1024;
}

http {                                        # http块
    include       mime.types;                # 引用mime.types这个文件

    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;
    #keepalive_timeout  0;
    keepalive_timeout  65;

    # nginx允许的客户端请求头部的缓冲区大小
    client_header_buffer_size 4k;

    #gzip  on;
    # proxy buffer
    proxy_buffers 8 4k;
    proxy_buffer_size 4k;
    proxy_temp_file_write_size 4k;
    proxy_temp_path proxy_temp;
    # proxy cache
    proxy_cache_path NGINX_cache/ keys_zone=cache_all:10m;

    # 128.236.160.5 CONF
    include conf.d/128_236_160_5.conf;

    #server {                                # server块
    #   listen       80;
    #   server_name  localhost;
    #   charset koi8-r;
    #   access_log  logs/host.access.log  main;

    #   location / {                        # location块
    #        root   html;
    #        index  index.html index.htm;
    #   }

        #error_page  404              /404.html;
        # redirect server error pages to the static page /50x.html
    #    error_page   500 502 503 504  /50x.html;
    #    location = /50x.html {
    #        root   html;
    #    }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #location ~ /\.ht {
        #    deny  all;
        #}
    #}

    # another virtual host using mix of IP-, name-, and port-based configuration
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

    # HTTPS server
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;
    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;
    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;
    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}

```

> 如果某个指令在两个不同层级的块中同时出现,则采用**就近原则**,即以较低层级块中的配置为准.

### 错误日志

日志级别由低到高分为debug(需要在编译时使用--with-debug开启debug)、info、notice、warn、error、critical、alert、emerg。

### 引入配置文件

`include file`

### 事件驱动模型

`use method`

> method内容有:select, poll, kqueue, epoll, rtsig, `/dev/poll`, eventport

### 自定义服务日志

```nginx
log_format exampleLog '$remote_addr - [$time_local] $request '
                '$status $body_bytes_sent $http_referer '
                '$http_user_agent';
```

> [Nginx内置变量](http://nginx.org/en/docs/varindex.html)

### 基于名称的虚拟主机配置

`server_name myserver.com www.myserver.com;`

`server_name *.myserver.com www.myserver.*;`  (通配符'*'只能用于三段字符串的首段或尾段)

`server_name ~^www\d+\.myserver\.com$;`  ("~"为使用正则的标记)

**匹配优先度**:

1. 对于匹配方式不同的,按照以下优先级:

    1. 准确匹配 server_name
    2. 通配符在开始时匹配 server_name成功
    3. 通配符在结尾时匹配 server_name成功
    4. 正则表达式匹配server_name成功

2. 如果server_name处于同一优先级的匹配方式多次匹配成功,则首次匹配成功的虚拟主机处理请求

### 配置location

```

Syntax:    location [ = | ~ | ~* | ^~ ] uri { ... }

        location @name { ... }

Default:    —

Context:    server, location

```

标识含义:

- `=` 用于**标准uri**前,要求请求字符串与uri**严格匹配**
- `~` 用于表示uri包含**正则表达式**, 并且**区分大小写**
- `~*` 用于表示uri包含**正则表达式**, 并且**不区分大小写**
- `^~` 用于**标准uri**前, 要求Nginx服务器找到标识uri和请求字符串匹配度最高的location后, 立即使用此location处理请求, 而不再使用location块中的正则uri和请求字符串做匹配.

### 配置请求的根目录

```nginx
location /data/
{
    root /locationtest1;
}
```

当location块接收到`/data/index.htm` 的请求时, 将在`/locationtest1/data/` 目录下找到index.htm 响应请求.

### alias指令

```nginx
location ~ ^/data/(.+\.(htm|html))$
{
    alias /locationtest1/other/$1;
}
```

当收到`/data/index.htm`时, 匹配成功, 之后根据alias指令的配置, 将到 `/locationtest1/other` 目录下找到对应请求. 可以看到, 通过alias指令的配置, 跟路径已经从`/data` 更改为 `/locationtest1/other` 了.

### 设置网站默认首页

```nginx
location ~ ^/data/(.+)/web/$
{
    index index.$1.html index.my1.html index.html;
}
```

当location块接收到`/data/locationtest/web/` 时, 匹配成功, 它首先将预置变量$1置为*locationtest*, 然后在`/data/locationtest/web/` 路径下按照index的配置次序依次寻找 index.locationtest.html index.my1.html 和 index.html , 首先找到哪个页面, 就使用哪个页面响应请求.

### 错误页面

一般来说,HTTP **2XX 代表请求正常完成**, **3XX 代表网站重定向**, **4XX代表客户端出现错误**, **5XX代表服务器端出现错误**.

| HTTP消息                   | 代码    | 含义                                                                                                                  |
| -------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------- |
| 已移动                     | 301     | 请求的数据具有新的位置, 并且更改是**永久**的                                                                          |
| 已找到                     | 302     | 请求的数据**临时**具有不同的URI                                                                                       |
| 请参阅其他                 | 303     | 可在另一URI下找到对请求的响应, 并且应使用GET方法检索此响应                                                            |
| 未修改                     | 304     | 未按预期修改文档                                                                                                      |
| 使用代理                   | 305     | 必须通过位置字段中提供的代理来访问请求的资源                                                                          |
| 未使用                     | 306     | 不再使用, 但保留此代码以便将来使用                                                                                    |
| 无法找到网页               | 400     | 可以连接到Web服务器, 但是由于Web地址(URL) 的问题, 无法找到网页                                                        |
| 网站拒绝显示此网页         | 403     | 可以连接到网站, 但没有显示网页的权限                                                                                  |
| 无法找到网页               | 404     | 可以连接到网站, 但找不到网页. 导致此错误的原因有时可能是该网页暂时不可用或网页已被删除.                               |
| 网站无法显示该页面         | 405     | 可以连接到网站, 但网页内容无法下载到用户的计算机. 这通常是由网页编写方式问题引起的.                                   |
| 无法读取此网页格式         | 406     | 能够从网站接收信息, 但不能识别其格式, 因而无法正确地显示消息.                                                         |
| 该网站太忙, 无法显示此网页 | 408 409 | 服务器显示该网页的时间太长, 或对同一网页的请求太多                                                                    |
| 网页不复存在               | 410     | 可以连接到网站, 但无法找到网页. 与404不同, 此错误是永久性的, 而且由网站管理员打开                                     |
| 网站无法显示该页面         | 500     | 正在访问的网站出现了服务器问题. 该问题阻止了此网页的显示. 常见的原因是网站正在维护或使用脚本的交互式网站上的程序出错. |
| 未执行                     | 501     | 没有将正在访问的网站设置为显示浏览器所请求的内容                                                                      |
| 不支持的版本               | 505     | 该网站不支持浏览器用于请求网页的HTTP协议(如HTTP/1.1)                                                                  |
|                            |         |                                                                                                                       |

```
Syntax:    error_page code ... [=[response]] uri;
Default:    —
Context:    http, server, location, if in location
```

示例:

```nginx
error_page 404             /404.html;
error_page 500 502 503 504 /50x.html;
error_page 404 =200 /empty.gif;

#If an error response is processed by a proxied server or a FastCGI/uwsgi/SCGI server, and the server may return different response codes (e.g., 200, 302, 401 or 404), it is possible to respond with the code it returns:
error_page 404 = /404.php;

#If there is no need to change URI and method during internal redirection it is possible to pass error processing into a named location:
location / {
    error_page 404 = @fallback;
}

location @fallback {
    proxy_pass http://backend;
}

#It is also possible to use URL redirects for error processing:
error_page 403      http://example.com/forbidden.html;
error_page 404 =301 http://example.com/notfound.html;
```

### 基于IP配置Nginx的访问权限

```nginx
location / {
    deny  192.168.1.1;
    allow 192.168.1.0/24;
    allow 10.1.1.0/16;
    allow 2001:0db8::/32;
    deny  all;
}
```

```
Syntax:    allow address | CIDR | unix: | all;
Default:    —
Context:    http, server, location, limit_except
```

> address: 客户端IP, 不支持同时设置多个.如果有多个IP需要设置, 需要重复使用allow指令.

Nginx配置在解析的过程中, 遇到deny指令或者allow指令是按照顺序对当前客户端的连接进行访问权限检查的. 如果遇到匹配的设置时, 则停止继续向下搜索相关配置.

### 基于密码的Nginx访问权限

```
Syntax:    auth_basic string | off;
Default:    auth_basic off;
Context:    http, server, location, limit_except
```

```
Syntax:    auth_basic_user_file file;
Default:    —
Context:    http, server, location, limit_except
```

明文密码格式:

```
## comment
name1:password1
name2:password2:comment
name3:password3
```

加密密码可以使用`crypt()` 函数进行密码加密的格式, 在Linux平台上可以使用 `htpasswd` 命令生成. 在PHP和Perl等语言中, 也提供`crypt()`函数. 使用htpasswd命令的一个示例为:

`htpasswd -c -d /nginx/conf/pass_file username`

运行后输入密码即可.
