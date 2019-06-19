Title: NGINX 实战手册-安全-HTTP 基本认证
Category: DevOps
Date: 2019-06-19 20:08
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX的HTTP基本认证功能.
Image: /images/nginx-ssl-certificate.jpg

## 2.4 HTTP基本认证

### 2.4.0 介绍

基本认证是一个保护私有内容的简单方法. 这个认证方法可以很容易的用于隐藏**开发网站**或者隐藏特权的内容. 推荐在需要基本认证的locations或servers上设置一个速率限制来组织暴力攻击. 也推荐如上章那样, 使用HTTPS, 因为每个认证请求, 用户名和密码是通过base64加密字符串, 作为一个header发送到server的. 如果使用HTTP, 意味着用户名和密码都可以被捕获.

### 2.4.1 创建一个User File

#### 问题

你需要一个HTTP基本认证用户文件来存储用户名和密码.

#### 解决方案

生成一个下列格式的文件, 密码可以通过以下允许的格式来加密或哈希:

```
# comment
name1:password1
name2:password2:comment
name3:password3
```

NGINX可以理解几种格式的密码, 其中一种加密是用C函数`crypt()`. 该函数被暴露给`openssl passwd`命令, 可以用如下方式生成加密字符串:

`$ openssl passwd MyPassword1234`

会输出一个字符串, NGINX可以用在密码文件里.

#### 讨论

也可以用Apache的`htpasswd`来生成密码. `htpasswd`和`openssl` 都会生成*apr1* 算法的密码. 密码也可以用LDAP和Dovecot使用的加盐sha-1 格式. NGINX支持更多的格式和哈希算法, 但是, 大部分都被认为不安全, 因为可以被轻易破解.

### 2.4.2 使用基本认证

#### 问题

你需要用基本认证来保护NGINX location或server.

#### 解决方案

```nginx.conf
location / {
    auth_basic          "Private site";
    auth_basic_user_file conf.d/passwd;
}
```

`auth_basic`指令可以用于HTTP, server, 或location块里. 当未认证用户访问, `auth_basic`指令会把字符串显示到基本认证的弹出窗口.

#### 讨论

基本认证通过server返回一个带有`WWW-Authenticate`的401未认证HTTP code. 该header会有一个值`Basic realm="your string."`. 该响应会导致浏览器提示输入用户名和密码. 输入的用户名和密码会通过base64加密, 通过一个叫做`Authorization`的请求头发送. Server会机密密码, 并根据`auth_basic_user_file`提供的密码做验证. 因为用户名密码仅仅是通过base64加密. 所以推荐使用HTTPS传输.
