Title: Spring Boot 微服务上容器平台的最佳实践 - 8 - Rest Service
Status: published
Tags: spring boot, k8s, openshift, 最佳实践, devops, java
Date: 2019-11-21 14:40
Author: 东风微鸣
Summary: 把Spring Boot 微服务部署到容器平台（K8S，OpenShift）上！这是第八篇, 主要介绍 spring微服务的相关设计和开发思路, 这次介绍REST服务的实现.
Image: /images/spring_k8s.png

![Spring+K8s](./images/spring_k8s.png)

## 前言

今天开始第八篇, 主要介绍 spring微服务的相关设计和开发思路, 这次介绍REST服务的实现.

[*Airports*](https://github.com/RHsyseng/spring-boot-msa-ocp/tree/master/Airports) 服务是应用程序中最简单的微服务，这为构建基本的Spring Boot REST服务提供了很好的参考。

## Spring Boot Rest Service

### Spring Boot Application Class

要将Java项目指定为Spring Boot应用程序，需要包含一个用[SpringBootApplication](https://docs.spring.io/spring-boot/docs/current/reference/html/using-boot-using-springbootapplication-annotation.html)注释的[Java类](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Airports/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/airports/RestApplication.java)，该类实现默认的Java main方法.

```java
package com.redhat.refarch.obsidian.brownfield.lambdaair.airports;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class RestApplication
{
 public static void main(String[] args)
 {
  SpringApplication.run( RestApplication.class, args );
 }
}
```

声明应用程序名称(application name)也是一种良好的实践，它可以作为[common application properties](https://docs.spring.io/spring-boot/docs/current/reference/html/common-application-properties.html)的一部分。这个应用程序使用以每个项目的名称开头的[application.yml](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Airports/src/main/resources/application.yml) 文件.

```yaml
spring:
  application:
    name: airports
```

### Maven Project File

每个微服务项目都包含一个Maven [POM文件](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Airports/pom.xml)，该文件除了声明模块属性(module properties)和依赖项外，还包含一个配置文件定义(profile definition)，用于使用[fabric8-maven-plugin](https://maven.fabric8.io/)创建和部署K8S或OpenShift镜像。

该POM文件使用一个属性(property)来声明包含操作系统和Java开发工具包(JDK)的基础镜像。此应用程序中的所有服务都构建在Red Hat Enterprise Linux (RHEL)基础镜像之上，其中包含一个受支持的OpenJDK版本:

```xml
<properties>
...
  <fabric8.generator.from>registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift</fabric8.generator.from>
</properties>
```

要轻松地包含提供REST服务的简单Spring Boot应用程序的依赖项，请声明以下两个构件(artifacts):

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-tomcat</artifactId>
</dependency>
```

此应用程序中的每个服务还声明了对[Spring Boot Actuator](https://github.com/spring-projects/spring-boot/tree/master/spring-boot-actuator) 组件的依赖关系，其中包括许多附加功能，可以帮助监视和管理应用程序。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

**当声明了对*Actuator*的依赖时，fabric8会生成默认的OpenShift [health probes](https://access.redhat.com/documentation/en-us/openshift_container_platform/3.7/html/developer_guide/dev-guide-application-health#container-health-checks-using-probes)**，该probes与*Actuator*服务通信，以确定服务是否正在运行(running)并准备(ready)好为请求提供服务:

```yaml
    livenessProbe:
      failureThreshold: 3
      httpGet:
        path: /health
        port: 8080
        scheme: HTTP
      initialDelaySeconds: 180
      periodSeconds: 10
      successThreshold: 1
      timeoutSeconds: 1
    readinessProbe:
      failureThreshold: 3
      httpGet:
        path: /health
        port: 8080
        scheme: HTTP
      initialDelaySeconds: 10
      periodSeconds: 10
      successThreshold: 1
      timeoutSeconds: 1
```

### Spring Boot REST Controller

要接收和处理REST请求，需要包含一个用[RestController](https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html)注释的[Java类](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Airports/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/airports/service/Controller.java).

```java
...
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller
```

在[application properties(应用程序属性)](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Airports/src/main/resources/application.yml#L10-L11)中为该服务指定监听端口:

```yaml
server:
  port: 8080
```

每个REST操作都由Java方法实现。业务操作通常需要指定[请求参数](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Airports/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/airports/service/Controller.java#L30-L32):

```java
@RequestMapping( value = "/airports", method = RequestMethod.GET )
public Collection<Airport> airports(
  @RequestParam( value = "filter", required = false ) String filter)
{
 ...
```

### 启动初始化

*Airports* 服务在启动时使用 eager initialization(即时初始化)将机场数据加载到内存中。这是通过监听特定类型事件的[ApplicationListener](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Airports/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/airports/service/ApplicationInitialization.java)实现的:

```java
import org.springframework.context.ApplicationListener;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.stereotype.Component;

@Component
public class ApplicationInitialization implements 
ApplicationListener<ContextRefreshedEvent>
{
 @Override
 public void onApplicationEvent(ContextRefreshedEvent 
contextRefreshedEvent)
```

## 小结

这篇有2个知识点:

1. 当声明了对*Actuator*的依赖时，fabric8会生成默认的OpenShift health probes. 这也算fabric8的一个优势, 少了人工加probe的步骤;
2. 能外部化的配置都可以外部化到: application properties里. 它可以是`application.yml`.