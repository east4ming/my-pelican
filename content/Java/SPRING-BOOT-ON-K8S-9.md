Title: Spring Boot 微服务上容器平台的最佳实践 - 9 - Ribbon和负载均衡
Status: published
Tags: spring boot, k8s, openshift, 最佳实践, devops, java
Date: 2019-11-21 15:30
Author: 东风微鸣
Summary: 把Spring Boot 微服务部署到容器平台（K8S，OpenShift）上！这是第九篇, 主要介绍 Ribbon和负载均衡. 利用Ribbon和生成的OpenShift Service实现高可用性。
Image: /images/spring_k8s.png

![Spring+K8s](./images/spring_k8s.png)

## 前言

今天开始第九篇, 主要介绍 Ribbon和负载均衡.

[*Flights*](https://github.com/RHsyseng/spring-boot-msa-ocp/tree/master/Flights)服务的结构与*Airports*服务类似，但依赖并调用*Airports*服务。因此，它利用**Ribbon**和生成的**OpenShift Service**实现高可用性。

## Ribbon 和 负载均衡

### RestTemplate 和 Ribbon

要快速且轻松地声明使用Ribbon所需的依赖项，请将以下构件(artifact)添加为Maven依赖项:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-ribbon</artifactId>
</dependency>
```

该应用程序还利用[Jackson JSR 310](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Flights/pom.xml#L54-L59)库正确地序列化和反序列化Java 8日期对象(date objects):

```xml
<dependency>
    <groupId>com.fasterxml.jackson.datatype</groupId>
    <artifactId>jackson-datatype-jsr310</artifactId>
    <version>2.8.8</version>
</dependency>
```

声明一个负载均衡的[RestTemplate](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Flights/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/flights/service/Controller.java#L39-L47)并使用注入将其分配给一个字段(field):

```java
@LoadBalanced
@Bean
RestTemplate restTemplate()
{
 return new RestTemplate();
}

@Autowired
private RestTemplate restTemplate;
```

对于传出调用，只需[使用restTemplate字段](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Flights/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/flights/service/Controller.java#L64):

```java
Airport[] airportArray = restTemplate.getForObject( "http://zuul/airports/airports", Airport[].class );
```

作为URL的主机部分提供的服务地址是通过Ribbon根据[应用程序属性](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Flights/src/main/resources/application.yml#L13-L15)中提供的值解析的: (`http://zuul`中的zuul会被解析为: `http://zuul:8080`)

```yaml
zuul:
  ribbon:
    listOfServers: zuul:8080
```

在本例中，Ribbon需要一个静态定义的服务地址**列表**，但是只有一个服务地址是用`zuul:8080`提供。Zuul使用地址的第二部分，即根web上下文(如上文的`/airports/`)，通过静态或动态路由重定向请求，本文档后面将对此进行解释。

**提供的zuul主机名其实是OpenShift的Service 名**(这个Service名在OpenShift集群内是可以作为域名使用的)，并解析为Service的Cluster IP地址，然后路由到内部的OpenShift负载均衡器。OpenShift Service名称是在使用oc工具创建Service时确定的，或者在使用fabric8 Maven插件部署镜像时确定的，它在[service yaml](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Zuul/src/main/fabric8/svc.yml)文件中声明。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: zuul
spec:
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP
```

再解释下, 可以这么理解, OpenShift的Service类似于硬件Load Balancer(如F5), 这个Service的Cluster IP类似于F5的VIP. 它后面会有1个或多个zuul服务. 网络流: rest请求 -> zuul -> 1个OpenShift Service -> 1个或多个zuul实例.

实际上，Ribbon并不负责负载均衡请求，而是将它们发送到OpenShift内部负载均衡器，该负载均衡器知道服务实例的副本数和失败情况，可以正确地重定向请求(对于Ribbon来说, 就是1个地址; 服务的注册和发现其实是由OpenShift的Service来实现了)。

## 小结

这一次, Spring 微服务的负载均衡是通过: Ribbon 和 OpenShift(或K8S)的Service来做的.

1. Ribbon仅负责反向代理; (不负责负载均衡)
2. OpenShift Service 负责负载均衡, 以及服务的注册和发现.
    1. 具体某一个服务的失败与否是通过K8S的Health Probe来探测的.

