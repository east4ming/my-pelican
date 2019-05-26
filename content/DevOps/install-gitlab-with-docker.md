Title: 使用 Docker 安装 Gitlab
Status: published
Tags: docker, openshift, k8s, containers, git
Author: 东风微鸣
Summary: 在个人电脑或公司测试环境使用docker或OpenShift快速搭建 Gitlab.

## Docker 安装

> :notebook: 说明:
>
> 官网链接:[GitLab Docker images](https://docs.gitlab.com/omnibus/docker/)
>
> [官网 Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/docker/Dockerfile)

```bash
sudo docker pull gitlab/gitlab-ce  # 下载
sudo docker run --detach \
  --hostname gitlab.example.com \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab \
  --volume /srv/gitlab/logs:/var/log/gitlab \
  --volume /srv/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest  # 运行容器
```



### 数据存在哪儿:

| 本地位置             | 容器位置          | 用途                   |
| :------------------- | :---------------- | :--------------------- |
| `/srv/gitlab/data`   | `/var/opt/gitlab` | 用于存储应用数据       |
| `/srv/gitlab/logs`   | `/var/log/gitlab` | 用于存储日志           |
| `/srv/gitlab/config` | `/etc/gitlab`     | 用于存储GitLab配置文件 |

### 配置Gitlab:

配置文件位于: `/etc/gitlab/gitlab.rb`

几种配置方式:

- `sudo docker exec -it gitlab /bin/bash` 进入到容器内, 然后通过`vi`编辑保存
- `sudo docker exec -it gitlab editor /etc/gitlab/gitlab.rb` 

编辑完之后, 重启容器:`sudo docker restart gitlab`

### 预配置 Docker 容器

也可以通过将环境变量`GITLAB_OMNIBUS_CONFIG`添加到docker run命令来预配置GitLab Docker映像。此变量可以包含任何`gitlab.rb`设置，并在加载容器`gitlab.rb`文件之前进行加载。

示例如下:

```bash
sudo docker run --detach \
  --hostname gitlab.example.com \
  --env GITLAB_OMNIBUS_CONFIG="external_url 'http://my.domain.com/'; gitlab_rails['lfs_enabled'] = true;" \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab \
  --volume /srv/gitlab/logs:/var/log/gitlab \
  --volume /srv/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest
```

### 启动容器后

可以通过<http://localhost> 进行访问.

可以通过 `sudo docker logs -f gitlab` 查看日志.

### 发布到公网IP

```bash
sudo docker run --detach \
  --hostname gitlab.example.com \
  --publish 198.51.100.1:443:443 \
  --publish 198.51.100.1:80:80 \
  --publish 198.51.100.1:22:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab \
  --volume /srv/gitlab/logs:/var/log/gitlab \
  --volume /srv/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest
```

### 使用docker-compose安装GitLab

1. 安装 docker compose
2. 创建`docker-compose.yml` 文件（或[下载示例](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/docker/docker-compose.yml)）: 

```yaml
 web:
   image: 'gitlab/gitlab-ce:latest'
   restart: always
   hostname: 'gitlab.example.com'
   environment:
     GITLAB_OMNIBUS_CONFIG: |
       external_url 'https://gitlab.example.com'
       # Add any other gitlab.rb configuration here, each on its own line
   ports:
     - '80:80'
     - '443:443'
     - '22:22'
   volumes:
     - '/srv/gitlab/config:/etc/gitlab'
     - '/srv/gitlab/logs:/var/log/gitlab'
     - '/srv/gitlab/data:/var/opt/gitlab'
```

3. 确保您`docker-compose.yml`与运行`docker-compose up -d` 在同一目录中以运行GitLab

## OpenShift 安装

> :exclamation: 注意:
>
> 目前Gitlab通过OpenShift 安装, 有一些已知的问题. 并且只在OpenShift 3.11版本上测试通过.
>
> 另外, 安装是通过 Helm Chart方式进行安装的. 还是有点复杂的...

### 已知的问题

以下问题是已知的，并且预计适用于OpenShift上的GitLab安装：

1. `anyuid`scc的要求：(OpenShift 的安全加固导致的)
    - GitLab的不同组件，如Sidekiq，unicorn等，使用UID 1000来运行服务。
    - PostgreSQL chart以`root`用户身份运行服务。
    - [问题＃752](https://gitlab.com/charts/gitlab/issues/752)是open状态，以调查更多有关解决此问题的信息。
2. 如果使用`hostpath`卷，则需要为主机中的持久性卷目录授予`0777`权限，以授予所有用户对卷的访问权限。
3. OpenShift的内置router 不支持通过SSH进行Git操作。 [问题＃892](https://gitlab.com/charts/gitlab/issues/892) 是oepn状态，以调查更多有关解决此问题的信息。
4. 众所周知，GitLab Registry不能与OpenShift的内置router配合使用。 [问题＃893](https://gitlab.com/charts/gitlab/issues/893)是open状态，以调查更多有关修复此问题的信息。
5. 从Let's Encrypt自动发出SSL证书不适用于OpenShift router。我们建议[您使用自己的证书](https://docs.gitlab.com/charts/installation/tls.html#option-2-use-your-own-wildcard-certificate)。 [问题＃894](https://gitlab.com/charts/gitlab/issues/894)开放，以调查更多有关解决此问题的信息。

### 先决条件步骤

1. 请参阅[官方文档](https://www.okd.io/download.html#oc-platforms) 以安装和配置群集。

2. 运行`oc cluster status`并确认群集正在运行：

```bash
oc cluster status
```

    输出应类似于：

```
Web console URL: https://gitlab.example.com:8443/console/
    
Config is at host directory
Volumes are at host directory
Persistent volumes are at host directory /home/okduser/openshift/openshift.local.clusterup/openshift.local.pv
Data will be discarded when cluster is destroyed
```

    请注意主机中Persistent Volumes的位置（在上例中`/home/okduser/openshift/openshift.local.clusterup/openshift.local.pv`）。以下命令需要`PV_HOST_DIRECTORY`环境变量中的路径。

3. 修改PV目录的权限（用以上值替换以下命令中的路径）：

```bash
sudo chmod -R a+rwx ${PV_HOST_DIRECTORY}/*
```

4. 切换到系统管理员用户：

```bash
oc login -u system:admin
```

5. 将`anyuid`scc 添加到系统用户：

```bash
oc adm policy add-scc-to-group anyuid system:authenticated
```

    **警告**：此设置将应用于所有namespace，并将导致Docker镜像未明确指定USER作为`root`用户运行。 [问题＃895](https://gitlab.com/charts/gitlab/issues/895)是开放的，用于记录所需的不同服务帐户，并描述仅将scc添加到这些服务帐户，因此影响可能有限。

6. 创建服务帐户和`rolebinding`RBAC并[安装Tiller](https://docs.gitlab.com/charts/installation/tools.html#helm)：

```bash
kubectl create -f https://gitlab.com/charts/gitlab/raw/master/doc/installation/examples/rbac-config.yaml
helm init --service-account tiller
```

### 下一步

在群集启动并运行后，继续[安装chart](https://docs.gitlab.com/charts/installation/deployment.html)，并准备好静态IP和DNS条目。

在此之前，请注意常规 chart安装过程中的以下更改：

1. 我们将使用OpenShift的内置router，因此需要禁用chart中包含的nginx-ingress服务。将以下标志传递给`helm install`命令：

```bash
--set nginx-ingress.enabled=false
```

2. 由于已知内置注册表不能使用Helm Chart与OpenShift一起使用，因此请禁用注册表服务。将以下标志传递给 `helm install`命令：

```
--set registry.enabled=false
```

3. [使用您自己的SSL证书](https://docs.gitlab.com/charts/installation/tls.html#option-2-use-your-own-wildcard-certificate)

