Title: Spring Boot 微服务上容器平台的最佳实践 - 11 - ZUUL
Status: published
Tags: spring boot, k8s, openshift, 最佳实践, devops, java
Date: 2019-11-22 17:00
Author: 东风微鸣
Summary: 把Spring Boot 微服务部署到容器平台（K8S，OpenShift）上！这是第11篇, 主要介绍 ZUUL.
Image: /images/spring_k8s.png

![Spring+K8s](./images/spring_k8s.png)

## 前言

今天开始第11篇, 主要介绍 ZUUL.

## ZUUL

这个Demo 使用Zuul作为微服务之间所有调用的中心代理。默认情况下，zuul使用在其[application properties(应用程序属性)](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zuul/src/main/resources/application.yml#L8-L18)中定义的静态路由:

```yaml
 zuul:
   routes:
     airports:
       path: /airports/**
       url: http://airports:8080/
     flights:
       path: /flights/**
       url: http://flights:8080/
     sales:
       path: /sales/**
       url: http://sales:8080/
```

上述规则中提供的路径使用web地址的第一部分来确定要调用的服务，并使用地址的其余部分作为上下文。

### A/B 测试

为了实现A/B测试，Salesv2服务在计算票价的算法中引入了一个小的变化。Zuul通过筛选一些请求的[filter](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Zuul/misc/ABTestingFilterBean.groovy)提供动态路由。

对其他服务的调用不进行过滤:

```java
if( 
!RequestContext.currentContext.getRequest().getRequestURI().matches("/sale
s.*") )
{
    //Won't filter this request URL
    false
}
```

只过滤来自以奇数结尾的IP地址的对sales 服务的调用:

```java
String caller = new HTTPRequestUtils().getHeaderValue("baggage-forwarded-
for");
logger.info("Caller IP address is " + caller)
int lastDigit = caller.reverse().take(1) as Integer
if( lastDigit % 2 == 0 )
{
    //Even IP address won't be filtered
    false
}
else
{
    //Odd IP address will be filtered
    true
}
```

如果调用者的IP地址末尾有一个奇数，请求将被重新路由。这意味着执行filter的[run](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zuul/misc/ABTestingFilterBean.groovy#L49-L52)方法，该方法更改路由的host:

```java
@Override
Object run() {
    println("Running filter")
    RequestContext.currentContext.routeHost = new URL("http://salesv2:8080")
}
```

为了在不更改应用程序代码的情况下启用动态路由，OpenShift节点可以使用共享存储，并[创建](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Zuul/misc/zuul-pv.json)和[声明](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Zuul/misc/zuul-pvc.json)一个持久卷。卷设置好并设置了groovy过滤器之后，OpenShift deployment config 可以进行管理调整，以将目录作为卷挂载:

```shell
$ oc volume dc/zuul --add --name=groovy --type=persistentVolumeClaim --claim-name=groovy-claim --mount-path=/groovy
```

这将导致在groovy目录下找到所有的groovy脚本。zuul应用程序代码通过[查找和应用](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zuul/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/zuul/RestApplication.java#L27-L35)此路径下的任何groovy脚本，实现了动态路由filter的引入:

```java
for( Resource resource : new PathMatchingResourcePatternResolver().getResources( "file:/groovy/.groovy" 
) ) { logger.info( "Found and will load groovy script " + resource.getFilename() ); sources.add( resource ); } if( sources.size() == 1 ) { logger.info( "No groovy script found under /groovy/.groovy" );
}
```

## 结束语

至此, 关于《Spring Boot 微服务上容器平台的最佳实践》的系列文章已经全部完结。我们回顾下以下内容：

1. Spring Boot 微服务的基本概念和使用；
2. OpenShift 的简单应用；
3. Spring Boot中的一些组件和OpenShift组合使用，而无需太多代码的修改。

这一系列文章为 Spring Boot 微服务上容器平台（K8S和OpenShift）做了研究和实现，同时提供了对相关概念使用的实例，希望对各位的Spring Boot容器化部署有所帮助。:tada::tada::tada: