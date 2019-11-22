Title: Spring Boot 微服务上容器平台的最佳实践 - 6
Status: published
Tags: spring boot, k8s, openshift, 最佳实践, devops, java
Date: 2019-11-20 10:30
Author: 东风微鸣
Summary: 把Spring Boot 微服务部署到容器平台（K8S，OpenShift）上！这是第六篇, 主要介绍 如何进行A/B测试。
Image: /images/spring_k8s.png

![Spring+K8s](./images/spring_k8s.png)

## 前言

今天开始第六篇, 主要介绍 如何进行A/B测试。

A/B测试直接是使用zuul的动态网关的功能。这次关于K8S的演示只是如何通过Volume挂载的方式将动态脚本挂载进去。

## A/B 测试

将Zuul项目中提供的groovy脚本复制到此服务的共享存储中：(`/mnt/zuul/volume/`是NFS共享存储)

```shell
$ cp Zuul/misc/ABTestingFilterBean.groovy /mnt/zuul/volume/
```

为Zuul服务申请一个PVC。放置在此位置的外部groovy脚本就可以提供动态路由。

```shell
$ oc create -f Zuul/misc/zuul-pvc.json
persistentvolumeclaim "groovy-claim" created
```

```yaml
{
  "apiVersion": "v1",
  "kind": "PersistentVolumeClaim",
  "metadata": {
    "name": "groovy-claim"
  },
  "spec": {
    "accessModes": [
      "ReadWriteOnce"
    ],
    "resources": {
      "requests": {
        "storage": "1Gi"
      }
    }
  }
}
```

验证这个claim是否绑定到持久卷:

```shell
$ oc get pvc
NAME           STATUS    VOLUME              CAPACITY   ACCESSMODES   AGE
groovy-claim   Bound     groovy              1Gi        RWO           7s
zipkin-mysql   Bound     zipkin-mysql-data   1Gi        RWO           2h
```

将持久卷声明(PVC)作为文件系统根目录上的一个名为groovy的目录附加到deployment config:

```shell
$ oc volume dc/zuul --add --name=groovy --type=persistentVolumeClaim --
claim-name=groovy-claim --mount-path=/groovy
deploymentconfig "zuul" updated
[bmozaffa@middleware-master LambdaAir]$ oc get pods
NAME                       READY     STATUS              RESTARTS   AGE
airports-1-72kng           1/1       Running             0          1h
flights-1-4xkfv            1/1       Running             0          1h
presentation-2-pxx85       1/1       Running             0          32m
sales-1-fqxjd              1/1       Running             0          1h
salesv2-1-s1wq0            1/1       Running             0          1h
zipkin-1-k0dv6             1/1       Running             0          2h
zipkin-mysql-1-g44s7       1/1       Running             0          2h
zuul-1-2jkj0               1/1       Running             0          1h
zuul-2-deploy              0/1       ContainerCreating   0          4s
```

同样，一旦新版本启动并运行，会进行新的部署并终止原来的zuul pod。

等待，直到第二个版本的pod到达运行状态:

```shell
$ oc get pods | grep zuul
zuul-2-gz7hl               1/1       Running     0          7m
```

返回浏览器并执行一次或多次航班搜索。然后返回OpenShift环境，查看zuul pod的日志。

如果从浏览器接收到的IP地址以奇数结尾，groovy脚本将过滤pricing调用并将其发送到sales服务的版本2。(根据IP奇偶进行A/B测试)这一点在zuul日志中会很清楚:

```shell
$ oc logs zuul-2-gz7hl
...
... groovy.ABTestingFilterBean               : Caller IP address is 10.3.116.79
Running filter
... groovy.ABTestingFilterBean               : Caller IP address is 10.3.116.79
Running filter
```

在本例中，来自salesv2的日志将显示使用修改后的算法定价的机票:

```shell
$ oc logs salesv2-1-s1wq0
... c.r.r.o.b.l.sales.service.Controller     : Priced ticket at 463 with lower hop discount
... c.r.r.o.b.l.sales.service.Controller     : Priced ticket at 425 with lower hop discount
... c.r.r.o.b.l.sales.service.Controller     : Priced ticket at 407 with lower hop discount
... c.r.r.o.b.l.sales.service.Controller     : Priced ticket at 549 with lower hop discount
... c.r.r.o.b.l.sales.service.Controller     : Priced ticket at 509 with lower hop discount
... c.r.r.o.b.l.sales.service.Controller     : Priced ticket at 598 with lower hop discount
... c.r.r.o.b.l.sales.service.Controller     : Priced ticket at 610 with lower hop discount
```

具体A/B 测试就是通过这个条件进行过滤的: `$ vi /mnt/zuul/volume/ABTestingFilterBean.groovy`

```grovvy
...
if( lastDigit % 2 == 0 )
{
     false
}
else
{
     true
}
...
```

## 小结

通过K8S的*PV和PVC*的概念, 我们可以将数据持久化. 然后要修改数据的话也可以通过直接放入持久化卷来生效. 再结合Zuul的动态路由功能, 就能够实现灵活的路由方式.
