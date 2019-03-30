# 苹果ATS合规对Web服务器的影响

Title: 苹果ATS合规对Web服务器的影响
Author: 东风微鸣
Category: DevOps
Tags: ATS, apple, ssl, nginx, apache, tls, openssl
Image: /images/green_apple.png
Summary: 苹果ATS合规对Web服务器的影响. 为保证合规, Apache httpd, NGINX和WebLogic应该如何配置.
Related_posts: tencentyun-apply-ssl-certificate, nginx-conf-add-ssl-support

## 一 前言

> :notebook: 说明:
>
> 这篇文章是在太平保险期间, 我和同时Huang Wentao一起收集资料并实验后协作完成的.
>
> 本文写于2年前, 时至今日可能规范, 软件版本或配置项都发生变化. 如果要应用, 请应用前进行完善测试.

### 1.1 ATS要求

1. 协商的传输层安全（TLS）版本必须为TLS 1.2;
2. 连接必须使用AES-128或AES-256对称密码，协商的秘钥交换协议必须是以下之一：

    1. TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
    2. TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
    3. TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384
    4. TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
    5. TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
    6. TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
    7. TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    8. TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
    9. TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
    10. TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
    11. TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
3. Leaf server（设备服务器）证书必须使用以下类型的密钥之一签名
    1. Rivest-Shamir-Adleman (RSA)秘钥，长度至少为2048位
    2. Elliptic-Curve Cryptography (ECC) 秘钥，长度至少为256位
    3. 此外，leaf server证书散列算法必须是具有至少256（即SHA-256或更大）的摘要长度（有时称为“指纹”）的安全散列算法2（SHA-2）。

## 二 检查项

### 2.1 Apache 检查项

1. OpenSSL版本: 需要大于 [1.0.1](https://www.openssl.org/news/changelog.txt) (OpenSSL从1.0.1以后开始支持TLS 1.2)
2. 当前加密套件使用的密钥交换协议.
    1. 查看当前加密套件支持的协议. 要保证支持的协议中有以上ATS 中所要求的.
3. 当前密钥长度/指纹算法是否满足:
    1. 如果是RSA密钥, 则至少要为2048位;
    2. 如果是ECC密钥, 则至少为256位.
    3. 指纹安全散列算法要为 SHA-2
4. Apache版本:
    1. [Apache 2.2.23](http://svn.apache.org/repos/asf/httpd/httpd/branches/2.2.x/CHANGES) 或[2.4.0](http://svn.apache.org/repos/asf/httpd/httpd/branches/2.4.x/CHANGES) 以上版本都是支持的.

### 2.2 NGINX检查项

1. OpenSSL 版本: 需要大于1.0.1
2. 当前加密套件使用的密钥交换协议.
    1. 查看当前加密套件支持的协议. 要保证支持的协议中有以上ATS 中所要求的.
3. 当前密钥长度/指纹算法是否满足:
    1. 如果是RSA密钥, 则至少要为2048位;
    2. 如果是ECC密钥, 则至少为256位.
    3. 指纹安全散列算法要为 SHA-2
4. NGINX版本: 建议使用[1.1.13](http://nginx.org/en/CHANGES-1.12)以上版本.

### 2.3 WebLogic 检查项

1. JDK版本: 需要版本为JDK 7 以上.

## 三 修改配置项

> :notebook: 说明:
>
> 除了以上检查项中版本不符合的需要升级、证书的算法、秘钥长度需要达到要求外，还有其他配置项要进行配置.

### 3.1 Apache 配置项

示例: Apache版本2.2.23(~~待确定~~)，OpenSSL版本1.0.1e. (最大兼容性配置)

```httpd
<VirtualHost *:443>
    ...
    SSLEngine on
    SSLCertificateFile      /path/to/signed_certificate
    SSLCertificateChainFile /path/to/intermediate_certificate
    SSLCertificateKeyFile   /path/to/private/key

    # Uncomment the following directive when using client certificate authentication
    #SSLCACertificateFile    /path/to/ca_certs_for_client_authentication


    # HSTS (mod_headers is required) (15768000 seconds = 6 months)
    Header always set Strict-Transport-Security "max-age=15768000"
    ...
</VirtualHost>

# old configuration, tweak to your needs
SSLProtocol             all -SSLv2
SSLCipherSuite          ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-ECDSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:DES-CBC3-SHA:HIGH:SEED:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!RSAPSK:!aDH:!aECDH:!EDH-DSS-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA:!SRP
SSLHonorCipherOrder     on

```

### 3.2 NGINX 配置项

举例：Nginx版本1.11.0，OpenSSL版本1.0.1e (最大兼容性配置)

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    # Redirect all HTTP requests to HTTPS with a 301 Moved Permanently response.
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    # certs sent to the client in SERVER HELLO are concatenated in ssl_certificate
    ssl_certificate /path/to/signed_cert_plus_intermediates;
    ssl_certificate_key /path/to/private_key;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # Diffie-Hellman parameter for DHE ciphersuites, recommended 2048 bits
    ssl_dhparam /path/to/dhparam.pem;

    # old configuration. tweak to your needs.
    ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-ECDSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:DES-CBC3-SHA:HIGH:SEED:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!RSAPSK:!aDH:!aECDH:!EDH-DSS-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA:!SRP';
    ssl_prefer_server_ciphers on;

    # HSTS (ngx_http_headers_module is required) (15768000 seconds = 6 months)
    add_header Strict-Transport-Security max-age=15768000;

    # OCSP Stapling ---
    # fetch OCSP records from URL in ssl_certificate and cache them
    ssl_stapling on;
    ssl_stapling_verify on;

    ## verify chain of trust of OCSP response using Root CA and Intermediate certs
    ssl_trusted_certificate /path/to/root_CA_cert_plus_intermediates;

    resolver <IP DNS resolver>;

    ....
}

```

### 3.3 WebLogic 配置项

需要在Oracle官网下载java 7相关的policyfile
解压后，替换`JAVA_HOME/jre/lib/security`下的`local_policy.jar`、`US_export_policy.jar`文件。

## 四 注意项

1. :exclamation:升级OpenSSL，可能会影响sftp、ssh等和ssl有关的协议，需谨慎操作。
2. 考虑到旧的ssl版本漏洞，以及兼容性，建议都要禁用掉ssl V2及以下版本协议。(最新的建议是SSL v3也禁用)
