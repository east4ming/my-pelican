Title: 如何在 OpenShift 中运行 Collabora Office
Status: published
Tags: k8s, openshift, containers, 安全, 
Date: 2019-10-03 18:00
Author: 东风微鸣
Slug: how-to-run-container-with-su-in-openshift
Summary: 近期在尝试 office 文档在线编辑和预览的一些解决方案, 目前在使用Collabora Office, 但是在OpenShift中运行不起来, 快看看是怎么解决的吧.
Image: /images/too-hard.png

[TOC]

## 前言

近期在尝试 office 文档在线编辑和预览的一些解决方案, 目前在使用Collabora Office, 但是[Collabora的docker镜像](https://hub.docker.com/r/collabora/code)在OpenShift中运行不起来, 一直提示`Operation not permitted`.

### Collabora Office 简介

[Collabora Office](https://www.collaboraoffice.com/) 提供强大的Office 套件, 使您能够访问文档、编写新内容并协同工作。

![Collabora Office](./images/Collabora-Office.png)

- 可以在自己的服务器上安装套件
- 可以和其他应用（如：nextcloud owncloud等）或你自己的应用进行整合
- i18n级别的兼容性
- 协同编辑
- 可以完美融入进自己的解决方案

## 分析 - 需要哪些特权

[Collabora的docker镜像](https://hub.docker.com/r/collabora/code)在OpenShift中运行不起来, 一直提示`Operation not permitted`. 其实原因权限不允许, 它需要做的一些操作在OpenShift中是被禁止的(出于企业级安全的考虑). 所以我们将它需要的权限一项一项加上就好了.

要搞清楚它需要哪些权限, 我们可以看一下它的[`Dockerfile`](https://github.com/CollaboraOnline/Docker-CODE)及其相关内容:

```Dockerfile
FROM ubuntu:16.04

# Environment variables
ENV domain localhost
ENV LC_CTYPE en_US.UTF-8

# Setup scripts for LibreOffice Online
ADD /scripts/install-libreoffice.sh /
ADD /scripts/start-libreoffice.sh /
RUN bash install-libreoffice.sh

EXPOSE 9980

# Entry point
CMD bash start-libreoffice.sh
```

`dockerfile`中如上所示, 这个文件虽然简单, 但是我们可以得到2个信息:

1. 没有`USER` 指令, 那么这个镜像可能是需要`root`权限才能运行的.
2. 加入了2个脚本. 其中 `start-libreoffice.sh`是在容器启动的时候运行的, 所以主要来看一下这个脚本的内容:

```shell
#!/bin/sh

# Fix domain name resolution from jails
cp /etc/resolv.conf /etc/hosts /opt/lool/systemplate/etc/

if test "${DONT_GEN_SSL_CERT-set}" == set; then
# Generate new SSL certificate instead of using the default
mkdir -p /opt/ssl/
cd /opt/ssl/
mkdir -p certs/ca
openssl genrsa -out certs/ca/root.key.pem 2048
openssl req -x509 -new -nodes -key certs/ca/root.key.pem -days 9131 -out certs/ca/root.crt.pem -subj "/C=DE/ST=BW/L=Stuttgart/O=Dummy Authority/CN=Dummy Authority"
mkdir -p certs/{servers,tmp}
mkdir -p "certs/servers/localhost"
openssl genrsa -out "certs/servers/localhost/privkey.pem" 2048 -key "certs/servers/localhost/privkey.pem"
if test "${cert_domain-set}" == set; then
openssl req -key "certs/servers/localhost/privkey.pem" -new -sha256 -out "certs/tmp/localhost.csr.pem" -subj "/C=DE/ST=BW/L=Stuttgart/O=Dummy Authority/CN=localhost"
else
openssl req -key "certs/servers/localhost/privkey.pem" -new -sha256 -out "certs/tmp/localhost.csr.pem" -subj "/C=DE/ST=BW/L=Stuttgart/O=Dummy Authority/CN=${cert_domain}"
fi
openssl x509 -req -in certs/tmp/localhost.csr.pem -CA certs/ca/root.crt.pem -CAkey certs/ca/root.key.pem -CAcreateserial -out certs/servers/localhost/cert.pem -days 9131
mv certs/servers/localhost/privkey.pem /etc/loolwsd/key.pem
mv certs/servers/localhost/cert.pem /etc/loolwsd/cert.pem
mv certs/ca/root.crt.pem /etc/loolwsd/ca-chain.cert.pem
fi

# Replace trusted host and set admin username and password
perl -pi -e "s/localhost<\/host>/${domain}<\/host>/g" /etc/loolwsd/loolwsd.xml
perl -pi -e "s/<username (.*)>.*<\/username>/<username \1>${username}<\/username>/" /etc/loolwsd/loolwsd.xml
perl -pi -e "s/<password (.*)>.*<\/password>/<password \1>${password}<\/password>/" /etc/loolwsd/loolwsd.xml
perl -pi -e "s/<server_name (.*)>.*<\/server_name>/<server_name \1>${server_name}<\/server_name>/" /etc/loolwsd/loolwsd.xml
perl -pi -e "s/<allowed_languages (.*)>.*<\/allowed_languages>/<allowed_languages \1>${dictionaries:-de_DE en_GB en_US es_ES fr_FR it nl pt_BR pt_PT ru}<\/allowed_languages>/" /etc/loolwsd/loolwsd.xml

# Restart when /etc/loolwsd/loolwsd.xml changes
[ -x /usr/bin/inotifywait -a /usr/bin/killall ] && (
	/usr/bin/inotifywait -e modify /etc/loolwsd/loolwsd.xml
	echo "$(ls -l /etc/loolwsd/loolwsd.xml) modified --> restarting"
	/usr/bin/killall -1 loolwsd
) &

# Start loolwsd
su -c "/usr/bin/loolwsd --version --o:sys_template_path=/opt/lool/systemplate --o:lo_template_path=/opt/collaboraoffice6.0 --o:child_root_path=/opt/lool/child-roots --o:file_server_root_path=/usr/share/loolwsd ${extra_params}" -s /bin/bash lool
```

仔细分析下脚本:

1. 第一句`cp /etc/resolv.conf /etc/hosts /opt/lool/systemplate/etc/` 很明显就是需要`root`权限的.
2. 之后会进行生成证书的操作
3. 然后会进行相关的变量替换操作
4. 接下来是当`/etc/loolwsd/loolwsd.xml`这个配置文件发生变化时进行重启, 注意这边又来了好几个特权操作:
    1. `/usr/bin/inotifywait`
    2. `/usr/bin/killall`
5. 启动`loolwsd` 又是一个特权操作: `su -c`

### 需要的特权

初步总结一下需要的特权:

- `root` 用户
- `inotifywait`
- `killall`
- `su -c`

## 解决方案

### 在 OpenShift 中启用镜像 ROOT

> :notebook: 备注:
>
> [官方OpenShift文档: Enable Container Images that Require Root](https://docs.openshift.com/container-platform/3.9/admin_guide/manage_scc.html#enable-dockerhub-images-that-require-root)
>
> 这里就不详细的一步步介绍了, 具体步骤可以参考我的另一篇文章: [OpenShift企业测试环境应用部署实战]({filename}./deploy-app-with-openshift-in-enterprise-env.md)

有些容器镜像(如: `postgres`和`redis`和这次的`collabora`)需要root权限, 并且对卷属于谁有明确期望. 对于这类镜像, 需要给其对应的service account(服务账户, 一种特殊账户, 用于系统执行某些操作)加上`anyuid` SCC(Security Context Constraints: 安全上下文约束):

`oc adm policy add-scc-to-user anyuid system:serviceaccount:myproject:mysvcacct`

### 在 OpenShift 中提供其他 Capabilities

> :notebook: 备注:
>
> [Docker官方文档: Runtime privilege and Linux capabilities](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)

默认情况下，Docker容器是“无特权的”(unprivileged)，例如，不能在Docker容器内运行Docker守护进程。这是因为在默认情况下，容器不允许访问任何设备，但是一个"privileged"(“特权”)容器可以访问所有设备。

除了"privileged"之外，操作员还可以使用`--cap-add`和`--cap-drop`对capabilities(功能)进行细粒度控制。默认情况下，Docker有一个保留的默认capabilities列表。下表列出了Linux capabilities选项，这些选项是默认允许的。

| Capability Key   | 用途                                                         |
| :--------------- | :----------------------------------------------------------- |
| SETPCAP          | 修改进程的 capabilities.                                     |
| MKNOD            | 通过mknod创建特殊(如设备)文件                                |
| AUDIT_WRITE      | 将记录写入内核审计日志。                                     |
| CHOWN            | 任意更改文件UID和GID                                         |
| NET_RAW          | 使用RAW 和PACKET的 sockets.                                  |
| DAC_OVERRIDE     | 绕过文件的读、写和执行权限检查。                             |
| FOWNER           | Bypass permission checks on operations that normally require the file system UID of the process to match the UID of the file.对通常需要进程的文件系统UID与文件的UID匹配的操作进行绕过权限检查。 |
| FSETID           | Don’t clear set-user-ID and set-group-ID permission bits when a file is modified.当文件被修改时，不清除set-user-ID和set-group-ID权限位。 |
| KILL             | Bypass permission checks for sending signals.绕过发送信号的权限检查。 |
| SETGID           | 对进程GID进行任意操作; 向用户的命名空间中写入GID映射         |
| SETUID           | 对进程UID进行任意操作; 向用户的命名空间中写入UID映射         |
| NET_BIND_SERVICE | 为低于1024以下的端口绑定sockets                              |
| SYS_CHROOT       | 使用chroot, 修改root目录                                     |
| SETFCAP          | 为文件设置任意的capabilities.                                |

下表显示了默认情况下未授予的功能，可以添加这些功能。

| Capability Key  | 用途                                                         |
| :-------------- | :----------------------------------------------------------- |
| SYS_MODULE      | 加载和卸载内核modules.                                       |
| SYS_RAWIO       | 执行I/O port操作(iopl和ioperm).                              |
| SYS_PACCT       | 使用 acct, 开启或关闭进程accounting                          |
| SYS_ADMIN       | Perform a range of system administration operations. 执行一系列系统管理员操作 |
| SYS_NICE        | 提高进程的nice value(nice， setpriority，并改变任意进程的nice value。 |
| SYS_RESOURCE    | 覆盖资源数限制                                               |
| SYS_TIME        | 设置系统时钟 (settimeofday, stime, adjtimex; 设置real-time (硬件) clock. |
| SYS_TTY_CONFIG  | 使用vhangup ;在虚拟终端上使用各种特权ioctl操作。             |
| AUDIT_CONTROL   | 启用和禁用内核审计;更改审计过滤规则;检索审计状态和过滤规则。 |
| MAC_ADMIN       | Allow MAC configuration or state changes. Implemented for the Smack LSM. |
| MAC_OVERRIDE    | Override Mandatory Access Control (MAC). Implemented for the Smack Linux Security Module (LSM). |
| NET_ADMIN       | 执行各种网络相关的操作                                       |
| SYSLOG          | 执行privileged syslog操作.                                   |
| DAC_READ_SEARCH | 绕过文件读权限检查和目录读和执行权限检查。                   |
| LINUX_IMMUTABLE | Set the FS_APPEND_FL and FS_IMMUTABLE_FL i-node flags.       |
| NET_BROADCAST   | 启用套接字广播，监听多播。                                   |
| IPC_LOCK        | 锁内存 (mlock, mlockall, mmap, shmctl).                      |
| IPC_OWNER       | 对System V IPC对象上的操作进行绕过权限检查。                 |
| SYS_PTRACE      | 使用ptrace跟踪任意进程。                                     |
| SYS_BOOT        | 使用reboot和kexec_load，重新启动并加载一个新的内核供以后执行。 |
| LEASE           | 对任意文件建立租约(参见fcntl)。                              |
| WAKE_ALARM      | 触发唤醒系统。                                               |
| BLOCK_SUSPEND   | 使用可以阻止系统挂起的特性。                                 |

更多参考资料见: [capabilities(7) - Linux man page](http://man7.org/linux/man-pages/man7/capabilities.7.html)



> :notebook: 备注:
>
> [OpenShift官方文档: Provide Additional Capabilities](https://docs.openshift.com/container-platform/3.9/admin_guide/manage_scc.html#provide-additional-capabilities)

有时候, 镜像会需要Docker默认没有提供的capabilities(功能). 那么你可以在pod的描述文件 specification中请求这些额外的capabilities, 这些capabilities将根据SCC进行验证.

> :heavy_exclamation_mark: 注意:
>
> 这允许镜像以提权后的功能运行，**应该仅在必要时使用**。不应编辑默认的受限SCC以启用其他功能。

当与非根用户一起使用时，还必须确保使用`setcap`命令为需要附加功能的文件授予capabilities。例如，在镜像的Dockerfile中:

`setcap cap_net_raw,cap_net_admin+p /usr/bin/ping`

此外，如果Docker中默认提供了功能，则不需要修改pod specification来请求它。例如，`NET_RAW`是默认提供的，应该已经在ping上设置了此功能，因此运行ping不需要特殊的步骤。

要提供额外的功能:

提供额外功能:

1. 创建一个新的SCC
2. 使用`allowedabilities`字段添加允许的功能。
3. 创建pod时，在`securityContext.capabilities.add`中添加请求该功能的字段。

针对这个Collabora镜像, 仔细分析后, 要快速解决, 其实在容器的spec中给它授予"privileged" 就可以了. **注意: 之前关于root的权限是在`deployment`下配置的. 这个是在`containers`下配置的.**

具体配置如下:

![container spec cap](./images/container_spec_scc.png)

说明如下:

- `allowPrivilegeEscalation: true` - 允许权限提升. 其实就是给了这个容器"privileged".
- 用privileged的scc，需要相应的capabilities. 所以又添加了`MKNOD`这个capability.

## 总结

在OpenShift中:

1. 容器需要root用户, 给它对应的deployment添加Service Account, 并添加`anyuid`的SCC.
2. 容器需要其他capabilities, 简单的方式就是给它"privileged" 这个特权.

*最后顺便吐槽一下, SCC和linux capabilities实在是太难了, 对安全一知半解的我一脸懵逼. :joy::joy::joy:* 

![](./images/too-hard.jpg)