Title: 腾讯云申请免费SSL证书
Status: published
Tags: SSL, 腾讯云, 云, 安全
Author: 东风微鸣
Summary: 在腾讯云上申请免费的SSL证书
Image: /images/SSL-Certificate.png
Related_posts: initialize-my-tencentyun-server, build-ide-on-tencentyun, nginx-conf-add-ssl-support

## 前言

现在申请SSL证书的门槛和费用都大大降低了. 出现了很多免费提供加密证书的机构, 比较知名的是国外的[Let’s Encrypt](https://letsencrypt.org/), 免费, 自动化, 开放. 国内的云服务商也会提供免费的SSL证书. 下面是我在腾讯云上申请SSL证书的步骤.

![SSL](./images/SSL-Certificate.png)

## 步骤

1. 进入腾讯云[SSL证书管理页面](https://console.cloud.tencent.com/ssl), 点击 **申请免费证书**, 如下图:

   ![申请免费证书](./images/tencentyun_app_ssl_1.png)

2. 目前腾讯云上提供的免费证书是 **TRUSTAsia**家的, 选择并确定. 如下图:

   ![TRUSTAsia](./images/tencentyun_app_ssl_2.png)

3. 接下来就填写证书需要的相关信息, 很简单, 只有2项必填项:

   1. 通用名称, 具体的**单域名**. (:exclamation: 如: www.ewhisper.cn, blog.ewhisper.cn. 不能是*.ewhisper.cn 这种通用域名.)
   2. 申请邮箱

   ![证书信息](./images/tencentyun_app_ssl_3.png)

4. 接下来是域名身份验证. 腾讯云一套的话, 直接选择 **自动DNS验证**. 

   ![域名身份验证](./images/tencentyun_app_ssl_4.png)

5. 这样就完成申请了, 接下来就是等待审核了. 我的ssl审核的非常快, 也就十几分钟就下来了. 如下图:

   ![等待审核](./images/tencentyun_app_ssl_5.png)

6. 证书详情如下:

   ![证书详情](./images/tencentyun_app_ssl_6.png)

7. 证书信息列表如下, 证书有效期一年. 可以选择部署到CDN和负载均衡上. (如果有的话) 也可以下载部署到nginx上.

   ![证书信息列表](./images/tencentyun_app_ssl_7.png)

8. 下载的是个证书压缩包. 包括各类web server的证书类型:

   1. Apache: key, crt, 和bundle.crt
   2. IIS: pfx
   3. Nginx: crt, key
   4. Tomcat: jks

9. 接下来就是NGINX配置的事情了. :tada::tada::tada: