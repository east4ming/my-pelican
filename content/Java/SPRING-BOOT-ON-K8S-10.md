Title: Spring Boot 微服务上容器平台的最佳实践 - 10 - Zipkin
Status: published
Tags: spring boot, k8s, openshift, 最佳实践, devops, java
Date: 2019-11-21 16:30
Author: 东风微鸣
Summary: 把Spring Boot 微服务部署到容器平台（K8S，OpenShift）上！这是第10篇, 主要介绍 zipkin在K8S上的部署.
Image: /images/spring_k8s.png

![Spring+K8s](./images/spring_k8s.png)

## 前言

今天开始第10篇, 主要介绍 zipkin在K8S上的部署.

## Zipkin

这个demo使用Spring Sleuth来收集tracing 数据并将其发送到OpenZipkin, OpenZipkin作为OpenShift服务部署，并由一个持久的MySQL数据库镜像支持。可以从Zipkin控制台查询tracing 数据，该控制台通过OpenShift route公开。日志集成也可以使用trace id将相同业务请求的分布式执行捆绑在一起。

### MySQL 数据库

这个demo使用OpenShift提供并支持的 [MySQL镜像](https://access.redhat.com/documentation/en-us/openshift_container_platform/3.7/html/using_images/database-images#using-images-db-images-mysql)来存储持久的zipkin数据。

#### Persistent Volume

为了支持MySQL数据库镜像的持久存储，这个demo 创建并挂载一个通过NFS公开的逻辑卷。OpenShift [persistent volume](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Zipkin/zipkin-mysql-pv.json) 向镜像公开存储。在NFS服务器设置并共享存储之后可以进行如下操作:

```shell
$ oc create -f zipkin-mysql-pv.json
persistentvolume "zipkin-mysql-data" created
```

#### MySQL 镜像

这个demo 提供了一个[OpenShift template](https://raw.githubusercontent.com/RHsyseng/spring-boot-msa-ocp/master/Zipkin/zipkin-mysql.yml) 来创建数据库镜像、OpenZipkin所需的数据库 schema和OpenZipkin镜像本身。该模板依赖于openshift项目中[默认可用](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zipkin/zipkin-mysql.yml#L275-L278)的MySQL镜像定义。

#### 数据库初始化

> :notebook: 备注:
>
> 这一章节简要介绍了下pod的高级用法 - **lifecycle hooks**.

这个demo 演示了在创建pod之后使用[lifecycle hooks(生命周期钩子)](https://access.redhat.com/documentation/en-us/openshift_container_platform/3.7/html/developer_guide/deployments#lifecycle-hooks)初始化数据库。具体来说，[post hook](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zipkin/zipkin-mysql.yml#L192-L205)的用法如下:

```yaml
       recreateParams:
         post:
           failurePolicy: Abort
           execNewPod:
             containerName: mysql
             command:
             - /bin/sh
             - -c
             - hostname && sleep 10 && /opt/rh/rh-mysql57/root/usr/bin/mysql -h
$DATABASE_SERVICE_NAME -u $MYSQL_USER -D $MYSQL_DATABASE -p$MYSQL_PASSWORD -P
3306 < /docker-entrypoint-initdb.d/init.sql && echo Initialized database
             env:
             - name: DATABASE_SERVICE_NAME
               value: ${DATABASE_SERVICE_NAME}
             volumes:
             - mysql-init-script
```

注意，这个钩子使用命令行mysql实用程序来运行位于`/docker-entrypoint-initdb.d/init.sql` SQL脚本。

创建 schema 的SQL脚本作为 [config map](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zipkin/zipkin-mysql.yml#L264-L266)嵌入到template 中。然后config map 被声明为一个卷，并挂载在`/docker-entrypoint-initdb.d`下的最终路径上.

### OpenZipkin 镜像

模板使用OpenZipkin提供的[镜像](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zipkin/zipkin-mysql.yml#L145-L177): `image: openzipkin/zipkin:1.19.2`

OpenZipkin访问相关MySQL数据库所需的参数可以配置，也可以作为相同模板的一部分生成。数据库密码作为模板的一部分由OpenShift[随机生成](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zipkin/zipkin-mysql.yml#L313-L324)，并存储在一个[Secret](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zipkin/zipkin-mysql.yml#L21-L30) 中，这使得用户和管理员将来无法访问它们。这就是为什么要打印[tempate message(模板消息)](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zipkin/zipkin-mysql.yml#L5-L11)来允许一次性访问数据库密码，以便进行监控和故障排除。

要创建Zipkin 服务:

```shell
$ oc new-app -f LambdaAir/Zipkin/zipkin-mysql.yml
--> Deploying template "lambdaair/" for "zipkin-mysql.yml" to project 
lambdaair
     ---------
     MySQL database service, with persistent storage. For more information 
about using this template, including OpenShift considerations, see 
https://github.com/sclorg/mysql-container/blob/master/5.7/README.md.
     NOTE: Scaling to more than one replica is not supported. You must 
have persistent volumes available in your cluster to use this template.
     The following service(s) have been created in your project: zipkin-
mysql.
            Username: zipkin
            Password: Y4hScBSPH5bAhDL2 
       Database Name: zipkin
      Connection URL: mysql://zipkin-mysql:3306/
     For more information about using this template, including OpenShift 
considerations, see https://github.com/sclorg/mysql-
container/blob/master/5.7/README.md.
     * With parameters:
        * Memory Limit=512Mi
        * Namespace=openshift
        * Database Service Name=zipkin-mysql
        * MySQL Connection Username=zipkin
        * MySQL Connection Password=Y4hScBSPH5bAhDL2 # generated(这里随机生成的, 存储在K8S的Secret, 会挂载在mysql和zipkin2个pod的env里.)
        * MySQL root user Password=xYVNsuRXRV5xqu4A # generated
        * MySQL Database Name=zipkin
        * Volume Capacity=1Gi
        * Version of MySQL Image=5.7
--> Creating resources ...
    secret "zipkin-mysql" created
    service "zipkin" created
    service "zipkin-mysql" created
    persistentvolumeclaim "zipkin-mysql" created
    configmap "zipkin-mysql-cnf" created
    configmap "zipkin-mysql-initdb" created
    deploymentconfig "zipkin" created
    deploymentconfig "zipkin-mysql" created
    route "zipkin" created
--> Success
    Run 'oc status' to view your app.
```

### Spring Sleuth

虽然Zipkin服务允许对分布式tracing 数据进行聚合、持久化并用于报告，但该应用程序依赖于Spring Sleuth来关联调用并将数据发送给Zipkin。

与Ribbon和其他框架库的集成使得在应用程序中使用Spring Sleuth变得非常容易。通过在项目Maven文件中声明一个依赖项来包含这些库:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-sleuth-zipkin</artifactId>
</dependency>
```

还可以在application properties(应用程序属性)中指定应该trace的请求的百分比，以及到zipkin服务器的地址。我们再次依赖OpenShift Service抽象概念来访问zipkin。如下:

```yaml
spring:
  sleuth:
    sampler:
      percentage: 1.0
  zipkin:
    baseUrl: http://zipkin/
```

百分比值1.0表示100%的请求将被捕获。

这两个步骤足以收集tracing 数据，但是也可以将 [Tracer](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Presentation/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/presentation/service/API_GatewayController.java#L63) 对象注入代码以实现扩展功能。虽然每个远程调用默认情况下都可以生成和存储trace，但是[添加tag](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Presentation/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/presentation/service/API_GatewayController.java#L68)有助于更好地理解zipkin报告。它也会 [创建](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Presentation/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/presentation/service/API_GatewayController.java#L68) 和 [标定](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Presentation/src/main/java/com/redhat/refarch/obsidian/brownfield/lambdaair/presentation/service/API_GatewayController.java#L124) 感兴趣的tracing spans来收集更多有意义的tracing 数据.

#### Baggage Data

虽然Spring Sleuth主要是作为一种分布式tracing 工具，但它关联分布式调用的能力也可以有其他实际用途。每个创建的span都允许附加任意数据(称为**baggage item**)，这些数据将自动插入HTTP标头，并在span期间随业务请求从一个服务到另一个服务无缝传输。这个应用程序感兴趣的是使每个微服务都可以得到用户的真实IP。在OpenShift环境中，调用IP地址存储在HTTP头文件的标准key中。检索并在span上设置此值:

```java
querySpan.setBaggageItem( "forwarded-for", request.getHeader( "x-
forwarded-for" ) );
```

之后，可以通过`baggage-forward -for`的header key从相同调用范围内的任何服务访问此值。Groovy脚本中的Zuul服务[使用](https://github.com/RHsyseng/spring-boot-msa-ocp/blob/master/Zuul/misc/ABTestingFilterBean.groovy#L32)它来执行动态路由。

## 小结

这里边有几个重要的知识点:

1. K8S(或OpenShift) PV的概念及使用;
2. MySQL镜像通过OpenShift的 **lifecycle hooks**来执行init.sql
3. OpenShift 的Template 资源, 可以配置多个pod或镜像需要公用的信息(如数据库密码), 并可以通过设置pattern来自动生成.
4. Spring Sleuth微服务如何引入该依赖;
5. Spring Sleuth 也可以由其他用途, 如添加header, 来全链路传输感兴趣的信息(本例中为: 用户真实IP - `x-forwarded-for`)

