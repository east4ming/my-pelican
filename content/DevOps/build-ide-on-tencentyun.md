Title: 在云服务器上搭建集成开发环境
Date: 2019-03-27 09:00
Status: published
Category: DevOps
Tags: 腾讯云, 云, python, pipenv, docker
Slug: build-ide-on-tencentyun
Author: 东风微鸣
Summary: 腾讯云服务器初始化操作, 包括: 重装系统; 配置监控; 安全加固; 更新软件; 安装git和安装oh-my-zsh
Image: /images/tencentyun.jpg
Related_posts: initialize-my-tencentyun-server

[TOC]

## python优化配置

安装相关软件:

```shell
sudo yum install -y --setopt=tsflags=nodocs gcc make patch  # 安装编译软件
sudo yum group install -y development  # 安装开发包组
sudo yum install -y --setopt=tsflags=nodocs gdbm-devel openssl-libs openssl-devel openssl-devel ncurses-devel libsqlite3x-devel sqlite-devel readline-devel zlib-devel bzip2-devel python2-bz2file db4-devel libpcap-devel xz-devel libffi-devel sqlite3 sqlite python-ujson  # 安装依赖

sudo yum install -y mariadb mariadb-server redis memcached # 安装mariadb
sudo systemctl enable mariadb.service redis.service  # mariadb redis 开机启动
sudo systemctl start mariadb.service redis.service  # 启动mariadb服务
```

### 安装python 3.6

```shell
sudo yum install -y python36
```

安装pip:

```shell
sudo yum -y install python-pip python34-pip python36-pip
```

pip conf: 

在文件`~/.pip/pip.conf`中添加或修改:

```
[global]
index-url = http://mirrors.tencentyun.com/pypi/simple
trusted-host = mirrors.tencentyun.com
```

> 参考文章:
>
> [腾讯云软件源加速软件包下载和更新](https://cloud.tencent.com/document/product/213/8623)

### 安装pipenv: (主要使用python 3.6)

```shell
pip3.6 install pipenv --user
```

编辑`~/.zshrc`, 加入以下内容:

```shell
export PATH=/home/casey/.local/bin:$PATH
```

后续使用`pipenv`管理文件, 有以下几个要点:
1. 安装时候根据需要, 根据OS现有python指定, 如: `pipenv install --python /usr/bin/python36`
2. 可以修改`Pipfile`的以下配置, 加快依赖下载:
```
[[source]]
url = "http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com"
verify_ssl = false
```

### 编译安装Python 3.7

> 需要先yum安装`libffi-devel`

```shell
# 下载源码包并解压
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
tar -xvzf Python-3.7.2.tgz
cd Python-3.7.2
# configure 
sudo mkdir -p /usr/lib64/python3.7
sudo ./configure --prefix=/usr/lib64/python3.7
# install
sudo make && sudo make install
# 创建软连接
sudo rm -f /usr/bin/python3
sudo ln -s /usr/lib64/python3.7/bin/python3 /usr/bin/python3
# 加入PATH
vi ~/.zshrc
# .zshrc修改为以下内容
export PATH=/usr/lib64/python3.7/bin:/home/casey/.local/bin:$PATH
# 使得配置生效
source ~/.zshrc
# 验证
python3 -V 
# 输出: Python 3.7.2
pip3 -V                     
# 输出: pip 18.1 from /usr/lib64/python3.7/lib/python3.7/site-packages/pip (python 3.7)
```

## Docker 配置

### 安装

```shell
sudo yum install -y --setopt=tsflags=nodocs docker docker-compose docker-distribution docker-logrotate docker-lvm-plugin 
```

### 修改仓库源

适用于 CentOS 7 版本。

修改 Docker 配置文件 `sudo vi /etc/sysconfig/docker`，如下：

```shell
OPTIONS='--registry-mirror=https://mirror.ccs.tencentyun.com'
```

> 参考文章:
>
> [使用 DockerHub 加速器](https://cloud.tencent.com/document/product/457/9113)

### 开机启动

```shell
sudo systemctl enable docker
```

### 使用腾讯云容器的相关服务

1. 控制台, 进入**容器服务** → **镜像仓库** → **我的镜像** , 输入镜像仓库的个人密码. (账号是AppID)

2. (可选): 在**访问管理** → **用户组** → **当前用户组**里 → **关联策略** : [QcloudCCRFullAccess](https://console.cloud.tencent.com/cam/policy/detail/419082&QcloudCCRFullAccess&2) (镜像仓库全读写权限)

3. 云服务器使用如下命令登录:

    `sudo docker login --username=appid ccr.ccs.tencentyun.com`

4. 下载镜像:

    `sudo docker pull ccr.ccs.tencentyun.com/[namespace]/[ImageName]:[镜像版本号]`

   
