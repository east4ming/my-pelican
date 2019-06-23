Title: NGINX 学习笔记-高级配置-IPv4 的内核7个参数的配置优化
Category: DevOps
Date: 2019-06-23 16:15
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的NGINX服务器高级配置部分. 本文介绍NGINX IPv4 的内核7个参数的配置优化.
Image: /images/nginx-logo.png

## 1 IPv4 的内核7个参数的配置优化

> Linux 内核参数. 可以将这些内核参数值追加到Linux的/etc/sysctl.conf文件中.并使用下列命令生效:
>
> `# /sbin/sysctl -p`

1. net.core.netdev_max_backlog

   表示当每个网络接口接收数据包的速率比内核处理这些包的速率快时, 允许发送到队列的数据包的最大数目. 一般默认为128. Nginx定义的NGX_LISTEN_BACKLOG 默认为511. 将该参数调整为:

   `net.core.netdev_max_backlog = 262144`

2. net.core.somaxconn

   用于调节系统同时发起的TCP连接数, 一般默认为128. 在存在高并发的情况下, 该默认值较小, 可能导致链接超时或重传问题, 可以根据实际需要结合并发请求数来调节此值. 如:

   `net.core.somaxconn = 262144`

3. net.ipv4.tcp_max_orphans

   用于设定系统中最多允许存在多少TCP套接字不被关联到任何一个用户文件句柄上. 如果超过这个数字, 没有与用户文件句柄关联的TCP套接字将立即被复位, 同时给出警告信息. 这个限制只是为了防止简单的DoS攻击. 一般在系统内存充足的情况下, 可以增大该值:

   `net.ipv4.tcp_max_orphans = 262144`

4. net.ipv4.tcp_max_syn_backlog

   用于记录尚未收到客户端确认信息的连接请求的最大值. 对于128MB内存的系统, 默认值为1024. 在系统内存充足的情况下, 可以增大该值.

   `net.ipv4.tcp_max_syn_backlog = 262144`

5. net.ipv4.tcp_timestamps

   用于设置时间戳, 可以避免序列号的卷绕. 在一个1Gb/s的链路上, 遇到以前用过的序列号的概率很大. 当此值为0时, 禁用对于TCP时间戳的支持. 在默认情况下, TCP会接受这种"异常"的数据包. 建议将其关闭.

   `net.ipv4.tcp_timestamps = 0`

6. net.ipv4.tcp_synack_retries

   用于设置内核放弃TCP连接之前向客户端发送SYN+ACK包的数量.一般赋值为1, 即内核放弃连接之前发送一次SYN+ACK包.

   `net.ipv4.tcp_synack_retries = 1`

7. net.ipv4.tcp_syn_retries

   `net.ipv4.tcp_syn_retries = 1`
