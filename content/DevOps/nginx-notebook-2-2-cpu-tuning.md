Title: NGINX 学习笔记-高级配置-针对CPU的调优指令
Category: DevOps
Date: 2019-06-23 16:22
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的NGINX服务器高级配置部分. 本文介绍NGINX 针对CPU调优的常用指令.
Image: /images/nginx-logo.png

## 2 针对CPU的优化指令

1. worker_processes

   最好是赋值为机器CPU的倍数.

2. worker_cpu_affinity

   默认的`auto`就行.
   `worker_cpu_affinity 0001 0010 0100 1000;`
