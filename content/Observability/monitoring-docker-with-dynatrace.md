Title: 使用 Dynatrace AppMon 监控 Docker 应用
Date: 2019-03-12 10:58
Category: Observability
Tags: APM, Dynatrace, docker
Slug: monitoring-docker-app-with-dynatrace
Authors: 东风微鸣
Summary: 本章节介绍了将AppMon agent与dockerized应用程序集成的两种方案。

[TOC]

可以配置 AppMon 来监控包裹在docker 容器里的应用:


## 使用AppMon 监控 dockerized apps (basic)

本章节介绍了将[AppMon](https://www.dynatrace.com/solutions/application-monitoring/) agent与dockerized应用程序集成的两种方案。这些方案在本页面上被称为**基于组合**和**基于继承**的方案。每个方案的利弊都会列出. 但是，建议不要使用**基于继承**的方法，而是将其用于演示目的。

### 基于组合的方案

使用基于组合的方案，您可以使用[AppMon/agent](https://hub.docker.com/r/dynatrace/agent/) Docker镜像(示例见下), 该镜像包含所有的AppMon agent, 你可以配置附加到你的现有的Docker容器中。

**AppMon 6.5 示例:**

```dockerfile
#DOCKERFILE FOR DYNATRACE AGENT
FROM alpine:3.5

LABEL maintainer="Blazej Tomaszewski <blazej.tomaszewski@dynatrace.com>"

ARG DT_HOME
ARG BUILD_VERSION
ARG VERSION
ARG CUID
ARG CGID

ENV AGENT_INSTALLER_NAME=dynatrace-agent-${BUILD_VERSION}-unix.jar
ENV WSAGENT_INSTALLER32_NAME=dynatrace-wsagent-${BUILD_VERSION}-linux-x86-32.tar
ENV WSAGENT_INSTALLER64_NAME=dynatrace-wsagent-${BUILD_VERSION}-linux-x86-64.tar
ENV NODE_AGENT_INSTALLER_NAME=dynatrace-one-agent-nodejs-${BUILD_VERSION}-linux-x86.tgz
ENV AGENT_INSTALLER_URL=https://files.dynatrace.com/downloads/OnPrem/dynaTrace/${VERSION}/${BUILD_VERSION}/${AGENT_INSTALLER_NAME}
ENV WSAGENT_INSTALLER32_URL=https://files.dynatrace.com/downloads/OnPrem/dynaTrace/${VERSION}/${BUILD_VERSION}/${WSAGENT_INSTALLER32_NAME}
ENV WSAGENT_INSTALLER64_URL=https://files.dynatrace.com/downloads/OnPrem/dynaTrace/${VERSION}/${BUILD_VERSION}/${WSAGENT_INSTALLER64_NAME}
ENV NODE_AGENT_INSTALLER_URL=https://files.dynatrace.com/downloads/OnPrem/dynaTrace/${VERSION}/${BUILD_VERSION}/${NODE_AGENT_INSTALLER_NAME}

ENV SLAVE_AGENT_PORT=8001

ENV DT_INSTALL_DEPS=curl\ openjdk8-jre-base
ENV DT_RUNTIME_DEPS=bash

COPY build/scripts/install-agent.sh /usr/bin
COPY build/scripts/install-node-agent.sh /usr/bin
COPY build/scripts/install-wsagent.sh /usr/bin

RUN  apk update && apk add --no-cache ${DT_INSTALL_DEPS} ${DT_RUNTIME_DEPS} && \
     mkdir -p ${DT_HOME} && \
     /usr/bin/install-agent.sh ${AGENT_INSTALLER_URL} && \
     /usr/bin/install-wsagent.sh ${WSAGENT_INSTALLER32_URL} && \
     /usr/bin/install-wsagent.sh ${WSAGENT_INSTALLER64_URL} && \
     /usr/bin/install-node-agent.sh ${NODE_AGENT_INSTALLER_URL} && \
	 mkdir -p ${DT_HOME}/log/agent && \
	 apk del ${DT_INSTALL_DEPS}

ADD  build/bin/dtnginx_offsets.json.tar.gz ${DT_HOME}/agent/conf
COPY build/scripts/run-wsagent.sh ${DT_HOME}

COPY build/scripts/create-user.sh /tmp
ENV CUID="${CUID:-0}"
ENV CGID="${CGID:-0}"
RUN /bin/sh -c /tmp/create-user.sh && rm -rf /tmp/*
USER ${CUID}:${CGID}

CMD while true; do sleep 1; done
```

从技术上讲，这种方法使用了docker的一个特性，它允许docker容器将其文件系统的一部分导出为[docker卷](https://docs.docker.com/engine/tutorials/dockervolumes/)，从而使其可以被其他感兴趣的容器获得。

![]({static}/images/dynatrace_docker_1.png)

#### 示例

以下示例假定您已经运行`dynatrace/agent` Docker容器, 通过名字 `dtagent` 导入到`/dynatrace`安装目录作为一个卷. GitHub上的[AppMon in Docker](https://github.com/Dynatrace/Dynatrace-AppMon-Docker) 项目包含脚本来完成这个任务，甚至允许你在docker中方便地设置一个完整的appmon环境。更多的信息可以在以下的"性能诊所"(视频)找到。

##### 示例: Apache Tomcat

下边的`docker-compose.yml` 挂载容器`dtagent` 导入的卷, 并且使用合适的`-agentpath`来初始化`CATALINA_OPTS`环境变量.

```yaml
tomcat:
  image: tomcat
  ports:
  - 8080
  volumes_from:
  - dtagent
  environment:
    CATALINA_OPTS: "-agentpath:/dynatrace/agent/lib64/libdtagent.so=name=tomcat,collector=127.0.0.1:9998"
  command: catalina.sh run
```

##### 示例: NGINX

> 待补充

#### 分析

- **优点**: 这种方法有助于巧妙地清晰地分离关注点，这是Docker世界的设计原则。此外，您不需要将agent放入您的基本映像中。在运行时进行一个简单的配置就可以监控您需要的容器的一切。
- **缺点**: 虽然Docker运行时对容器之间交换volumes有很大的支持，但在容器编排平台（如kubernetes或openshift）上这样做会使您的应用程序配置过于复杂。

### 基于继承的方案

> **注意:**
>
> 不建议使用此方法，仅在此处进行演示。

从技术角度而言，Docker化应用程序通常涉及两个部分：

- 一个基本镜像, 如:`java:8`或`node:7`, 提供基础的执行环境
- 一个`Dockerfile`, 用特定于应用程序的安装指令来扩充选定的基本镜像。

使用你的`Dockerfile`, 运行`docker build`命令来创建需要的Docker 镜像.

[Docker Hub](https://hub.docker.com/)上提供了一整套的基础镜像. 你可以阅读[使用Dockerfiles自动化镜像构建](https://www.digitalocean.com/community/tutorials/docker-explained-using-dockerfiles-to-automate-building-of-images)和[写Dockerfiles的最佳实践](https://docs.docker.com/articles/dockerfile_best-practices/)获取更多信息.

![]({static}/images/dynatrace_docker_2.png)

#### 示例

你可以为准备监控的应用创建基础镜像. 把agent打包为基础的自动启用监控的镜像。

![]({static}/images/dynatrace_docker_3.png)

##### 示例: Java

本例子展示了一个`Dockerfile`, 来扩展官方的[openJDK Docker镜像](https://github.com/docker-library/openjdk) 基础镜像, 并下载对应的agent. 为了遍历, 需要设置一些环境变量, 如`DT_AGENT_NAME`和`DT_AGENT_COLLECTOR`, 以后可以在这些变量中填入你自己的数据. 另外, `JAVA_OPTS`添加一个指向`DT_AGENT_LIB64`的`-agentpath`参数.

```dockerfile
FROM openjdk:8

ENV DT_AGENT_INSTALLER_URL "http://files.dynatrace.com/downloads/OnPrem/dynaTrace/6.5/6.5.0.1289/dynatrace-agent-6.5.0.1289-unix.jar"

ENV DT                     "/dynatrace"
ENV DT_AGENT_LIB32         "${DT}/agent/lib/libdtagent.so"
ENV DT_AGENT_LIB64         "${DT}/agent/lib64/libdtagent.so"

ENV DT_AGENT_NAME          "java"
ENV DT_AGENT_COLLECTOR     "127.0.0.1:9998"

ENV JAVA_OPTS              "-agentpath:${DT_AGENT_LIB64}=name=${DT_AGENT_NAME},collector=${DT_AGENT_COLLECTOR}"

# Install the Agent
RUN curl -L -o /tmp/`basename ${DT_AGENT_INSTALLER_URL}` ${DT_AGENT_INSTALLER_URL} && \
    java -jar /tmp/`basename ${DT_AGENT_INSTALLER_URL}` -t ${DT} && \
    rm -f /tmp/`basename ${DT_AGENT_INSTALLER_URL}`
```

构建该Dockerfile使用`docker build . -t openjdk:8-dtappmon -f ./Dockerfile`在本地Docker仓库创建一个新的Docker镜像, 名字为`openjdk`, 标签为`8-dtappmon`. 每个应用构建, 你可以通过扩展`openjdk:8-dtappmon`来创建应用镜像(如下所示, `repo.internal`指的是虚拟仓库, `my-app`是虚拟应用.) 你也可以覆盖`DT_AGENT_NAME`环境变量来在该镜像里更准确的配置.

```dockerfile
FROM openjdk:8-dtappmon

ENV DT_AGENT_NAME "my-app"
ADD https://repo.internal/my-app/builds/latest.tar.gz /app
 
CMD java ${JAVA_OPTS} -jar /app/my-app.jar
```

##### 示例: Nginx

> 待补充

#### 分析

- **优点**: 一旦agent已经被放入你的Docker基础映像中，在哪个容器平台上运行你的应用程序并不重要. 此外，这种方案减少了appmon整合的准备工作，不会增加频繁building，shipping和running Dockerized 应用程序过程的任何开销。
- **缺点**: 根据您的特定用例和您所使用的技术,您必须手动集成这些技术. 因为这个方案会在特定技术的基础镜像上, 与特定技术的agent(如Java agent)紧密绑定, 当切换到另一种技术或appmon的新版本时，这些基本镜像可能需要被全部重新创建. (其实这个不算什么大问题, 就是定期更新agent)

### Q&A

#### 我能监控运行在docker, alpine上的程序么?

> 待补充

#### 我能监控在kubernetes或OpenShift上单 docker化应用么?

是的. 参见下一章节.

#### 我能在docker中运行easyTravel(AppMon的demo程序)么?

EasyTravel已经在GitHub的[EasyTravel in Docker ](https://github.com/dynatrace/Dynatrace-easytravel-docker)完全实现容器化了. 你可以使用[Dynatrace in Docker](https://github.com/Dynatrace/Dynatrace-AppMon-Docker)项目来注入监控.

## 使用AppMon 监控 dockerized apps - Kubernetes 和 OpenShift

上一章描述了如何使用[AppMon](https://www.dynatrace.com/solutions/application-monitoring/)监控 普通的Docker环境中的Dockerized apps.

本章阐述了如何监控在[Kubernetes](http://kubernetes.io/)和[Red Hat OpenShift(v3)](https://www.openshift.com/)的 Dockerized 应用. (OpenShift算是Kubernetes的商业化).

如上章"如何使用AppMon监控dockerized apps"所述, 根据于你的实际情况,  你可能会发现下列的方案更适合. 每种方案的利弊都已列出.

### 方案A: 基于继承的方案

基于继承的方案的目标是把AppMon的agent放到你的Docker基础镜像里. 因为Kubernetes和OpenShift都是容器平台, 这种方案允许你来在这些平台上复用你的启用监控的镜像. 然而, 因为OpenShift是一个安全加固的容器平台, 使用root运行容器和执行进程(大部分Docker都是这么构建的)默认会被禁止.  参考[OpenShift 容器镜像向导](https://docs.openshift.org/latest/creating_images/guidelines.html)来学习如何为OpenShift准备你的Docker镜像. 参见[如何使用AppMon监控dockerized apps](https://www.dynatrace.com/support/doc/appmon/application-monitoring/monitor-specific-applications/monitor-docker-apps/monitor-dockerized-apps-with-appmon/)获取如何应用本方案到你的Docker镜像.

#### 示例: Java

因为在你的基础镜像中的特定技术已被appmon监控，因此只需简单的运行时配置设置即可将agent绑定到appmon collector。

下列例子为一个运行在[Pod](http://kubernetes.io/docs/user-guide/pods/)上的一个叫做*catalog*的容器定义了一个[ReplicationController](http://kubernetes.io/docs/user-guide/replication-controller/). 环境变量`DT_AGENT_NAME`和`DT_AGENT_COLLECTOR`([如何使用AppMon监控dockerized apps](https://www.dynatrace.com/support/doc/appmon/application-monitoring/monitor-specific-applications/monitor-docker-apps/monitor-dockerized-apps-with-appmon/)中已定义好)覆盖掉由基础的`acmeco/my-app`镜像提供的各自的对应值.

```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: my-app
spec:
  template:
    spec:
      containers:
      - name: my-app
        image: acmeco/my-app
        env:
        - name: DT_AGENT_NAME
          value: "my-app"
        - name: DT_AGENT_COLLECTOR
          value: "dtappmon-collector.acmeco.com:9998"
        ports:
        - containerPort: 8080
```

#### 示例: Nginx

> 待补充

#### 分析

- **优点**: 一旦agent已经被放入你的Docker基础映像中，在哪个容器平台上运行你的应用程序并不重要. 此外，这种方案减少了appmon整合的准备工作，不会增加频繁building，shipping和running Dockerized 应用程序过程的任何开销。
- **缺点**: 根据您的特定用例和您所使用的技术,您必须手动集成这些技术. 因为这个方案会在特定技术的基础镜像上, 与特定技术的agent(如Java agent)紧密绑定, 当切换到另一种技术或appmon的新版本时，这些基本镜像可能需要被全部重新创建. (其实这个不算什么大问题, 就是定期更新agent)

### B方案: 基于组合的方案

> 待补充.


