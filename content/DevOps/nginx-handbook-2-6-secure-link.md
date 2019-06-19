Title: NGINX 实战手册-安全-安全链接
Category: DevOps
Date: 2019-06-19 20:15
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX的安全链接功能.
Image: /images/nginx-ssl-certificate.jpg

## 2.6 安全链接

### 2.6.0 介绍

安全链接(secure links)是一种使用*md5*哈希算法保证静态资源安全的方式. 使用这个模块, 你也可以限制该链接接收请求的时长. 使用安全链接使NGINX应用程序服务器确保静态内容安全而无需应用服务器承担这种责任. 这个模块包含在免费开源的NGINX里. 但是, 它没有打进标准的NGINX包, 而是放到了`nginx-extras`包里. 当从源码构建NGINX时, 可以选择使用配置参数`--with-http_secure_link_module`来启用.

### 2.6.1 加密Location

#### 问题

你需要使用一个密钥来加密一个location块.

#### 解决方案

使用安全链接模块, `secure_link_secret`指令来限制对资源的访问的用户有一个安全的链接:

```nginx
    location /resources {
        secure_link_secret mySecret;
        if ($secure_link = "") { return 403; }
        rewrite ^ /secured/$secure_link;
    }
    location /secured {
        internal;
        root /var/www;
    }
```

该配置创建了一个内部和一个外部的location块. 外部的location块`/resources`会返回403 Forbidden, 除非请求URI包含一个*md5*哈希字符串, 这个字符串可以被`secure_link_secret`指令提供的secret验证. `$secure_link`变量是一个空字符串, 除非在URI的哈希被验证.

#### 讨论

使用secret加密资源是一个很好的确保你的文件受保护的方法. 该secret用于和URI串联 . 该字符串然后会被`md5`哈希, `md5`哈希后的16禁止数字被用在该URI中. 该哈希被放到链接中, 由NGINX计算. NGINX会知道URI想要访问的路径, 因为哈希后就在URI中 . NGINX也会直到你的secret, 因为指令`secure_link_secret`会提供. NGINX能够迅速验证`md5`哈希, 并存储在URI的`$secure_link`变量中. 如果哈希无法验证, 该变量就是空字符串. 需要注意, 传给`secure_link_secret`的参数必须是一个静态字符串, 不能是变量.

### 2.6.2 使用secret生成一个安全链接

#### 问题

你需要使用secret从你的应用生成一个安全链接.

#### 解决方案

NGINX的安全链接模块接收一个md5哈希(URI路径和secret的联接)过的16进制字符串. 基于上一节, 我们会创建安全的连接, 可以工作在上个配置, 比如`/var/www/secured/index.html`. 要生成md5哈希的16进制字符串, 我们可以使用Unix openssl命令:

```shell
$ echo -n 'index.htmlmySecret' | openssl md5 -hex
(stdin)= a53bee08a4bf0bbea978ddf736363a12
```

保护的URI: *index.html*; secret: *mySecret*.

下边是使用Python 2.7和*md5*库生成的:

```python
import md5
md5.new('index.htmlmySecret').hexdigest()
'a53bee08a4bf0bbea978ddf736363a12'
```

那么我们访问的地址应该是如下所示, 要访问`/var/www/secured/index.html`

```
www.example.com/resources/a53bee08a4bf0bbea978ddf736363a12/\
index.html
```

#### 讨论

要生成这个数字可以由很多种方式, 很多语言都可以实现. 要记住的是: URI路径在secret之前, 字符串中没有回车, 并且使用*md5*哈希的16进制数字.

### 2.6.3 使用Expire Date加密Location

#### 问题

你需要生成一个在一段时间后过期的链接.

#### 解决方案

利用在安全链接模块的其他指令来在你的加密链接中设置过期日志和使用变量:

```nginx
location /resources {
    root /var/www;
    secure_link $arg_md5,$arg_expires;
    secure_link_md5 "$secure_link_expires$uri$remote_addr
   mySecret";
    if ($secure_link = "") { return 403; }
    if ($secure_link = "0") { return 410; }
}
```

`secure_link`指令有2个用逗号隔开的字段. 第一个字段是*md5*哈希的变量. 这个例子使用一个HTTP参数的md5。第二个字段是放置以Unix元年时间格式的链接过期时间的变量. `secure_link_md5`指令占用一个单独的字段, 声明用于构造*md5*哈希的的格式的字符串. 和其他配置一样, 如果hash没有通过验证, `$secure_link`变量设置为空字符串. 或者, 如果哈希匹配但是时间过期, `$secure_link`变量设置为0.

#### 讨论

这种用法比之前2.6.1中的更灵活, 看起来更干净. 使用这些指令, 你可以使用可以用在NGINX哈希字符串中的任意数量的变量. 在哈希字符串中使用用户相关的变量会加强安全性, 因为用户不能够得到加密的资源. 推荐使用像是`$remote_addr`或`$http_x_forwarded_for`或由应用生成的会话cookie作为变量. `secure_link`的参数可以来自你喜欢的任何变量, 他们可以被命名为任意合适的名字. 在`$secure_link`变量中的条件可以被设置返回已知的Forbidder和Gone的HTTP代码. HTTP 410, Gone, 对于过期链接非常适用, 因为这个条件被认为是永久的.

### 2.6.4 生成一个有过期时间的链接

#### 问题

你需要生成一个有过期时间的链接.

#### 解决方案

用Unix时间戳格式生成一个过期时间戳. 在Unix系统上, 你可以这样操作:

```shell
$ date -d "2020-12-31 00:00" +%s
1609390800
```

接下来你需要连接用在`secure_link_md5`指令中的哈希字符串. 在本例中, 使用`1293771600/resources/index.html127.0.0.1  mySecret`. md5哈希和刚刚的16进制数字有一些不同. 它是一个二进制格式的md5哈希, 采用base64加密, 用加号(+)转换为连接符(-), 斜杠(/)转换为下划线(_), 等号(=)被移除. 如下所示:

```shell
$ echo -n '1609390800/resources/index.html127.0.0.1 mySecret' \
  | openssl md5 -binary \
  | openssl base64 \
  | tr +/ -_ \
  | tr -d =
81CYyxXFADhLHaQD36_BK
```

就得到了哈希, 我们可以用它后边跟着过期日期作为参数.

`/resources/index.html?md5=81CYyxXFADhLHaQD36_BK&expires=1609390800'`

以下是使用Python 2.7的标准库的例子:

```python
from datetime import datetime
from base64 import b64encode
import md5
resource = '/resources/index.html'
remote_addr = '127.0.0.1'
host = 'www.example.com'
expire = datetime(2020,12,31,0,0).strftime('%s')
uncoded = expire + resource + remote_addr + ' mySecret'
md5hashed = md5.new(uncoded).digest()
b64 = b64encode(md5hashed)
hash = b64.replace('+', '-').replace('/', '_').replace('=', '')
linkformat = "{}{}?md5={}?expires{}"
securelink = linkformat.format(host,resource,hash,expire)
```

#### 讨论

使用这种方式, 我们能生成用于URL中的特殊格式的加密链接. 提供安全保障的secret绝不会发给客户端. 你可以用尽可能的你需要的其他变量来加密location. md5哈希和base64加密很常见, 轻量, 几乎在所有语言中都可用.
