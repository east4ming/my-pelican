Title: NGINX 实战手册-运维-使用`split_clients`进行A-B测试
Category: DevOps
Date: 2019-06-19 20:39
Tags: nginx, devops, 译文, 最佳实践, docker
Summary: NGINX 实战手册系列文章的运维部分. 本文主要介绍如何使用`split_clients`进行A-B测试.
Image: /images/docker_nginx-750x410.png

## 3.7 使用`split_clients`进行A-B测试

### 3.7.0 介绍

NGINX有一个叫做`split_clients`的模块, 允许你来系统地给予某一个变量key来拆分用户. NGINX通过使用轻量的哈希算法来哈希一个给定的字符串来拆分用户. 然后数学地通过百分比拆分, 映射预定义的值到一个变量, 这个值可以用来改变服务器的响应。

### 3.7.1 A/B 测试

#### 问题

你需要拆分两个或更多版本的文件或程序的用户来测试接受度.

#### 解决方案

使用`split_clients`模块来直接为你的客户端设置不同的upstream pool:

```nginx
split_clients "${remote_addr}AAA" $variant {
    20.0%    "backendv2";
    *        "backendv1";
}
```

`split_clients`指令哈希由你提供的字符串作为第一个参数, 并且将散列的百分比提供映射一个变量的值作为第二个参数提供。第三个参数是一个包含key-value对的对象, key是百分比权重, 值是要被分配的值. key可以是一个百分比或一个星号. 星号就是剩下的百分比. 变量`$variant`的值将是20%的客户端IP是`backendv2`, 剩下的80%是`backendv1`.

在本例中, `backendv1`和`backendv2`代表upstream server池, 可以被用于`proxy_pass`指令, 如下:

```nginx
location / {
    proxy_pass http://$variant
}
```

使用变量`$variant`, 我们的流量会被分为2个不同的应用server池.

另一个案例:

```nginx
http {
 split_clients "${remote_addr}AAA" $variant {
                0.5%               .one;
                2.0%               .two;
                   *                  "";
 }
 server {
     location / {
         index index${variant}.html;
```

#### 讨论

A/B测试的类型很有用, 如测试不同类型的市场和前端功能的电商网站转化率. 对于应用, 使用金丝雀发布很常见. 这种部署中, 流量被缓慢地切换到新的版本. 拆分不同应用版本的客户端是很有用的, 当回滚新版本的代码, 限制因为一个错误导致的爆炸半径. 不论是因为什么原因要拆分两个不同应用集的客户端, NGINX通过使用`split_client`模块都能很容易实现.

#### 参见

[split_client documentation](http://bit.ly/2jsdkw4)
