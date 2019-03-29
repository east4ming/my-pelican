Title: Docker 学习笔记 - 镜像
Status: published
Category: DevOps
Tags: docker
Author: 东风微鸣
Summary: 我的docker学习笔记, 本次集中于docker镜像的相关操作.
Image: /images/Docker_logo.png
Related_posts: build-ide-on-tencentyun, monitoring-docker-app-with-dynatrace

## 获取镜像

`docker pull`

## 查看镜像信息

`docker images`

`docker inspect <images id>  # 获取镜像的详细信息`

## 搜寻镜像

`docker search`

## 删除镜像

`docker rmi`

> 当一个镜像拥有多个标签，`docker rmi`只是删除该镜像指定的标签，并不影响镜像文件
> 当镜像只剩下一个标签时，再使用会彻底删除该镜像
> 先删除该镜像的所有容器，再删除镜像

## 创建镜像

3种方法：
- 基于已有镜像的**容器**创建
- 基于本地模板导入
- 基于Dockerfile创建

### 基于已有镜像的容器创建
 
`docker commit `

> -a: 作者信息
> -m: 提交信息
> -p 提交时暂停容器运行
> -c changelist

### 基于本地模板的导入 

推荐使用OpenVZ 提供的模板来创建。下载地址：https://openvz.org/Download/template/precreated
`sudo cat ubuntu-16.04-x86_64.tar.gz | docker import - ubuntu:16.04`

## 导出和载入镜像

**导出**：`sudo docker save -o ubuntu_16.04.tar ubuntu:16.04`
**载入**：`sudo docker load --input ubuntu_16.04.tar` 或者 `sudo docker load < ubuntu_16.04.tar`

> 该指令会载入镜像，以及其相关的元数据信息（包括标签等）. 关于`docker load`和`docker import`指令的区别见下一章.
