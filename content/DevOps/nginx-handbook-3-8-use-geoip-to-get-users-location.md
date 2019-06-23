Title: NGINX 实战手册-运维-使用GeoIP模块通过IP地址定位用户
Category: DevOps
Date: 2019-06-19 20:39
Tags: nginx, devops, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的运维部分. 本文主要介绍如何使用GeoIP模块通过IP地址定位用户.
Image: /images/docker_nginx-750x410.png

## 3.8 使用GeoIP模块通过IP地址定位用户

### 3.8.0 介绍

跟踪, 分析, 和利用你的应用或度量的客户端的位置信息可以帮助你加深对客户的理解. 有很多方法获取你的客户的位置信息, NGINX通过使用GeoIP模块和几个指令很容易地定位他们. 该模块让基于客户位置信息记录位置, 控制访问, 或者基于客户位置做决定变得很容易.  它也允许客户的位置信息被内部查找只要请求被传输到upstream应用, 而不需要再进行查找. 该NGINX模块默认不安装, 可以从源码静态编译, 动态导入, 或通过在Ubuntu安装`nginx-full`或`nginx-extras`来安装. 在RHEL发行版, 如CentOS, 你可以安装`nginx-mod-http-geoip`包并通过`load_module`动态导入. 本章会覆盖

- 导入GeoIP动态模块,
- 安装GeoIP数据库,
- 该模块可用的内建变量,
- 控制访问,
- 和代理一起使用.

### 3.8.1 使用GeoIP模块和数据库

#### 问题

你需要安装GeoIP数据库, 并启用在NGINX的内建命令, 来记录和告诉你的应用你的客户端的地理位置.

#### 解决方案

下载GeoIP国家和城市数据库, 并unzip它们:

```shell
# mkdir /etc/nginx/geoip
# cd /etc/nginx/geoip
# wget "http://geolite.maxmind.com/\
download/geoip/database/GeoLiteCountry/GeoIP.dat.gz"
# gunzip GeoIP.dat.gz
# wget "http://geolite.maxmind.com/\
download/geoip/database/GeoLiteCity.dat.gz"
# gunzip GeoLiteCity.dat.gz
```

这些命令在*/etc/nginx*下创建一个*geoip*目录, 跳转到新目录, 并下载和解压包.

通过在本地磁盘上的 国家和城市的GeoIP数据库, 我们可以构建NGINX GeoIP模块并使用它们来暴露出给予客户端IP地址的内建指令:

```nginx
load_module "/usr/lib64/nginx/modules/ngx_http_geoip_module.so";
http {
    geoip_country /etc/nginx/geoip/GeoIP.dat;
    geoip_city /etc/nginx/geoip/GeoLiteCity.dat;
...
}
```

`geoip_country`指令指定到*GeoIP.dat*文件的路径, *GeoIP.dat*包含IP地址到国家代码的映射, 只能在HTTP上下文中使用.

### 讨论

模块的`geoip_country`和`geoip_city`暴露一系列可用变量. `geoip_country`指令允许你去本你的客户的国家. 这些变量包括`$geoip_country_code`, `geoip_country_code3`和`geoip_country_name`. 国家代码变量返回一个2位国家字母. `geoip_country_code3`返回3位国家字母. 国家名变量返回国家的全名.

`geoip_city`指令也会启用几个变量. 和`geoip_country`类似. 有`$geoip_city_country_code` `geoip_city_country_code3` `geoip_city_contry_name`. 其他变量有`$geoip_city` `$geoip_city_continent_code` `$geoip_latitude` `$geoip_longitude`和`$geoip_postal_code`. `$geoip_region` `$geoip_region_name`描述区域, 领域, 州, 省, 联邦政府地等. 区域是一个两字符代码, 区域名是全名. `geoip_area_code`, 只在美国有效, 返回3位数字电话区域码.

通过这些变量, 你能够记录你的客户端的信息. 你可以选择传递信息到你的应用作为一个header或变量, 或使用NGINX来以特定方式route流量.

#### 参见

[GeoIP 升级](https://github.com/maxmind/geoipupdate)

### 3.8.2 基于国家限制访问

#### 问题

根据合约或应用需求, 你需要限制来自特定国家的访问.

#### 解决方案

映射你想要屏蔽或允许的国家代码到一个变量

```nginx
load_module
  "/usr/lib64/nginx/modules/ngx_http_geoip_module.so";
http {
    map $geoip_country_code $country_access {
        "US"    0;
        "RU"    0;
        default 1;
    }
    ...
}
```

这个映射会设置新的变量`$country_access`为1或0. 如果客户端IP地址来自美国或俄罗斯, 变量会被设置为0, 其他国家会设置为1.

然后, 在`server`快, 使用`if`声明来拒绝不是来自美国和俄罗斯的用户访问:

```nginx
server {
    if ($country_access = '1') {
      return 403;
    }
    ...
}
```

当条件判断为True时, 会返回403 未认证. 否则正常访问.

#### 讨论

这是一个简短的例子, 来说明如何允许特定国家访问. 这个例子可以被扩展, 以符合你的需要.

### 3.8.3 找到源客户端

#### 问题

你需要找到客户源IP, 因为在NGINX server前边有代理.

#### 解决方案

使用`geoip_proxy`指令来定义你的代理IP地址范围, `geoip_proxy_recursive`指令来查找源IP:

```nginx
load_module "/usr/lib64/nginx/modules/ngx_http_geoip_module.so";
http {
    geoip_country /etc/nginx/geoip/GeoIP.dat;
    geoip_city /etc/nginx/geoip/GeoLiteCity.dat;
    geoip_proxy 10.0.16.0/26;
    geoip_proxy_recursive on;
...
}
```

`geoip_proxy`指令定义我们的代理服务器的CIDR范围, 指示NGINX利用`X-Forwarded-For`头来查找客户端IP地址. `geoip_proxy_recursive`指令指示NGINX来递归地查找上个知道的客户端IP的`X-Forwarded-For` header.

#### 讨论

你可能会发现你在NGINX前边使用了代理, NGINX会选择代理的IP地址而不是客户端的. 对于这种情况你可以使用`geoip_proxy`指令来指示在给定的范围内, NGINX使用`X-Forwarded-For` header. `geoip_proxy`指令配置一个地址或CIDR范围. 当NGINX前边有多个代理, 可以使用`geoip_proxy_recursive`指令来递归地查找`X-Forwarded-For`指令, 来找到源客户端. 你可能会在如在NGINX前边使用AWS ELB, 谷歌的负载均衡, 或Azure的负载均衡时用到这些.
