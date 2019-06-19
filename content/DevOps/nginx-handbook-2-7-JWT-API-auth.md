Title: NGINX 实战手册-安全-使用JWT API的安全认证
Category: DevOps
Date: 2019-06-19 20:15
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX的安全链接功能.
Image: /images/nginx-ssl-certificate.jpg

## 2.7 使用JWT的API认证

### 2.7.0 介绍

JSON Web Tokens (JWTs)迅速成为一种广为使用和受欢迎的认证方式. 这些认证tokens有能力存储一些用户和用户的认证信息到token里. 这些tokens也可以异步验证, 这意味着负载均衡和代理可以使用公钥来验证该token, 而不需要用于签发token的私钥, 以此提高安全和灵活性.

> NGINX Plus的功能, 略过.
