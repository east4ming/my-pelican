Title: Spring Boot 微服务上容器平台的最佳实践 - 7 
Status: published
Tags: spring boot, k8s, openshift, 最佳实践, devops, java
Date: 2019-11-20 10:30
Author: 东风微鸣
Summary: 把Spring Boot 微服务部署到容器平台（K8S，OpenShift）上！这是第七篇, 主要介绍 spring微服务的相关设计和开发思路。
Image: /images/spring_k8s.png

![Spring+K8s](./images/spring_k8s.png)

## 前言

今天开始第七篇, 主要介绍 spring微服务的相关设计和开发思路。

在第六篇, Spring Boot 微服务部署到容器平台已经完工. 接下来我们就会对Spring 微服务的相关设计和开发, 以及K8S(或OpenShift)与Spring Boot之间的协作进行更深一层的设计和开发.

今天先开个头, 先介绍下K8S的`Resource Limits`概念, 通过这个概念可以对每个微服务的资源用量进行控制. 防止单个有问题微服务吃光全部资源导致雪崩效应.

## RESOURCE LIMITS

OpenShift[允许](https://access.redhat.com/documentation/en-us/openshift_container_platform/3.7/html/developer_guide/dev-guide-compute-resources)管理员设置约束来限制每个项目中使用的对象的数量或计算资源的数量。虽然这些约束总体上适用于项目(即namespace)，但[每个pod](https://access.redhat.com/documentation/en-us/openshift_container_platform/3.7/html/developer_guide/dev-guide-compute-resources#dev-compute-resources)也可以请求最小的资源和/或受到内存和CPU使用限制的约束。

项目存储库中提供的OpenShift template使用此功能请求至少20%的CPU内核和200MB内存可用于其容器。如果需要并且可用，可以向容器提供两倍的处理能力和四倍的内存，但再超过就不会分配了。

```yaml
resources:
  limits:
    cpu: "400m"
    memory: "800Mi"
  requests:
    cpu: "200m"
    memory: "200Mi"
```

> :notebook: 备注:
>
> 根据我之前的文章: [《容器最佳实践》](https://www.ewhisper.cn/container-best-practices.html#java)
>
> JAVA程序都有一个启动阶段，启动阶段也会大量消耗CPU, CPU使用越多, 启动阶段越短.
> 下面是一个表，总结了不同CPU限制下的spring boot 示例应用启动时间(m表示millicore):
>
> - 500m — 80 seconds
> - 1000m — 35 seconds
> - 1500m — 22 seconds
> - 2500m — 17 seconds
> - 3000m — 12 seconds
>
> 根据以上情况, 容器平台管理员考虑对JAVA容器做如下限制:
>
> - 使用CPU requests, 不设置cpu limit (Kubernetes功能) (或者限制到3000m)
>
> ```yaml
> resources:
>   requests:
>     memory: "1024Mi"
>     cpu: "500m"
>   limits:
>     memory: "1024Mi"
> ```

当使用fabric8 Maven插件创建镜像并直接编辑*deployment config*不方便时，可以使用[资源片段(*resource fragments*)](https://maven.fabric8.io/#configuration)来提供所需的片段。此应用程序提供[deployment.yml](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Airports/src/main/fabric8/deployment.yml)文件来利用这个功能，并在Spring启动项目上设置资源请求和限制.

```yaml
spec:
   replicas: 1
   template:
     spec:
       containers:
         - resources:
             requests:
               cpu: '200m'
               memory: '400Mi'
             limits:
               cpu: '400m'
               memory: '800Mi'
```

对各个服务的内存和CPU使用的控制通常是关键的。如上所述，这些值的正确配置与部署和管理过程是无缝衔接的。在项目中设置[资源配额](https://access.redhat.com/documentation/en-us/openshift_container_platform/3.7/html/developer_guide/dev-guide-compute-resources#dev-quotas)以[强制](https://access.redhat.com/documentation/en-us/openshift_container_platform/3.7/html/developer_guide/dev-guide-compute-resources#dev-requests-vs-limits)将它们包含在pod部署配置中是有帮助的。

## 小结

通过K8S的*Resource Limits*的概念, 可以对容器(以及其中的微服务)进行内存和CPU的resource request和limit的配置. 允许根据需求分配容器到满足条件的机器, 同时限制容器的最大资源使用.
