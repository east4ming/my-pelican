Title: Spring Boot 微服务上容器平台的最佳实践 - 5
Status: published
Tags: spring boot, k8s, openshift, 最佳实践, devops
Date: 2019-11-19 16:40
Author: 东风微鸣
Summary: 把Spring Boot 微服务部署到容器平台（K8S，OpenShift）上！这是第五篇, 主要介绍 如何将配置外部化。
Image: /images/spring_k8s.png

![Spring+K8s](./images/spring_k8s.png)

## 前言

今天开始第四篇, 主要介绍下 如何将配置外部化。

这次没有用到*Spring*的*Config Server*, 而是使用*OpenShift*的*ConfigMap*作为参数外部化的方案.

## 参数外部化

*Presentation* 服务在其应用程序属性中将*Hystrix*配置为[线程池](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Presentation/src/main/resources/application.yml#L22)大小为20。在航班搜索操作之后，通过搜索*presentation* pod的日志来确认这一点，并验证batch size是相同的。

```shell
$ oc logs presentation-1-k2xlz | grep batch
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 20 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 13 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 20 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 13 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 20 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 13 
tickets
```

△ 当前batch size最大为**20**

创建一个新`application.yml`文件. `vi application.yml`

输入以下内容：

```yaml
hystrix:
  threadpool:
    SalesThreads:
      coreSize: 30
      maxQueueSize: 300
      queueSizeRejectionThreshold: 300    
```

通过`oc` 创建`configmap`:

```shell
$ oc create configmap presentation --from-file=application.yml
configmap "presentation" created
```

编辑*presentation*的`deployment config`并将这个ConfigMap挂载为卷， 路径为： `/deployment/config`，它将自动成为Spring启动应用程序classpath的一部分.  `$ oc edit dc presentation`

添加具有任意名称的新卷，例如`config-volume`, 来引用前面创建的configmap。`volume`定义是`template spec`的一个子规范。接下来，在容器下面创建一个volume mount来引用这个卷，并指定应该挂载它的位置。最后的结果如下所示. (`volumeMounts` -> `dnsPolicy`之前)

```yaml
...
        resources: {}
        securityContext:
          privileged: false
        terminationMessagePath: /dev/termination-log
        volumeMounts:
        - name: config-volume
          mountPath: /deployments/config
      volumes:
        - name: config-volume
          configMap:
            name: presentation
      dnsPolicy: ClusterFirst
      restartPolicy: Always
...
```

一旦修改并保存了deployment config，OpenShift将部署包含覆盖属性的服务的新版本。这个更改是持久的，将来使用这个新版本的部署配置创建的pod也将挂载这个yaml文件。

列出pod，并注意一个新的pod正在创建来反映部署配置(即挂载的文件)中的更改:

```shell
$ oc get pods
NAME                       READY     STATUS      RESTARTS   AGE
airports-1-72kng           1/1       Running     0          18m
flights-1-4xkfv            1/1       Running     0          15m
presentation-1-k2xlz       1/1       Running     0          10m
presentation-2-deploy      0/1       ContainerCreating   0          3s
sales-1-fqxjd              1/1       Running     0          7m
salesv2-1-s1wq0            1/1       Running     0          5m
zipkin-1-k0dv6             1/1       Running     0          1h
zipkin-mysql-1-g44s7       1/1       Running     0          1h
zuul-1-2jkj0               1/1       Running     0          1m
```

等待，直到pod的第二个版本已经启动, 处于running状态。第一个版本将被终止，随后被删除.

```shell
$ oc get pods
NAME                       READY     STATUS      RESTARTS   AGE
...
presentation-2-pxx85       1/1       Running     0          5m
...
```

一旦发生这种情况，使用浏览器进行一次或多次航班搜索。然后通过搜索新的表示pod的日志来验证更新后的线程池大小，并验证batch size: 

```shell
$ oc logs presentation-2-pxx85 | grep batch
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 30 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 3 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 30 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 3 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 30 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 3 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 30 
tickets
... c.r.r.o.b.l.p.s.API_GatewayController    : Will price a batch of 3 
tickets
```

△ 注意，使用挂载的覆盖属性时，定价将以30个并发批次进行，而不是现在的20个。

## 小结

通过K8S的*configmap*的概念, 我们可以将配置参数外部化. 然后外部化的参数可以通过2种方式挂载到运行时中:

1. 环境变量 ENV
2. Volume 挂载到指定路径.

还是比较灵活的.