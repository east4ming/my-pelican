Title: Spring Boot 微服务上容器平台的最佳实践 - 4
Status: published
Tags: spring boot, k8s, openshift, 最佳实践, devops
Date: 2019-11-15 19:30
Author: 东风微鸣
Summary: 把Spring Boot 微服务部署到容器平台（K8S，OpenShift）上！这是第四篇, 主要介绍 几个微服务的部署.
Image: /images/spring_k8s.png

![Spring+K8s](./images/spring_k8s.png)

## 前言

今天开始第四篇, 主要介绍下 几个微服务的部署. 介绍2种方法, 一种是分步的, 构建jar、打镜像、传到镜像库、K8S部署；另一种直接通过Maven + Farbic8 一气呵成。

## 微服务部署

微服务部署这里介绍2种方式:

1. Maven, Docker build, K8S 部署
2. Maven Farbic8 直接部署到K8S

如果已有的maven编译等方式不希望改动, 且希望build和deploy分离, 则推荐用第一种方式;

如果希望更快速高效, 全新的代码直接上K8S, 则推荐第二种方式.

第二种 **Maven Farbic8 直接部署到K8S** 部署方式的一些优点:

1. 参数, 变量, 配置可以全局应用. 如: 服务名....
2. 会检测`actuator`, 并自动添加K8S Liveness和Readiness Probe
3. 可以添加icon到容器平台, 展示更友好;
4. 可以根据编译好的版本号等自动打镜像tag
5. 自动登录K8S或OpenShift平台;
6. 自动部署

### Maven, Docker build, K8S 部署

细节就不介绍了, 说一下简要步骤.

1. Maven 构建为jar包
2. 写个Dockerfile, jar包通过docker build方式构建为docker镜像;
3. 将构建好的镜像打好tag, 如`snapshot-191114-111831-0702`, push到镜像仓库.
4. K8S 创建Deployment和Service和Ingress(或Route), 并引用镜像仓库中新的镜像tag, 并启动.

### Maven Farbic8 直接部署到K8S

要部署Spring启动服务，使用*Maven*构建项目，使用*openshift*配置文件的*fabric8:deploy* target将构建的镜像部署到openshift。为了方便起见，在项目的根目录下提供了一个聚合器pom文件，它将同一个Maven构建委托给所有6个配置的模块.

```shell
$ mvn clean fabric8:deploy -Popenshift
[INFO] Scanning for projects...
[INFO]
[INFO] ---------------------------------------------------------------
---------
[INFO] Building Lambda Air 1.0-SNAPSHOT
[INFO] ---------------------------------------------------------------
---------
...
...
...
[INFO] --- fabric8-maven-plugin:3.5.30:deploy (default-cli) @ aggregation 
---
[WARNING] F8: No such generated manifest file 
/Users/bmozaffa/RedHatDrive/SysEng/Microservices/SpringBoot/SpringBootOCP/
LambdaAir/target/classes/META-INF/fabric8/openshift.yml for this project 
so ignoring
[INFO] ---------------------------------------------------------------
---------
[INFO] Reactor Summary:
[INFO]
[INFO] Lambda Air ......................................... SUCCESS [01:33 
min]
[INFO] Lambda Air ......................................... SUCCESS [02:21 
min]
[INFO] Lambda Air ......................................... SUCCESS [01:25 
min]
[INFO] Lambda Air ......................................... SUCCESS [01:05 
min]
[INFO] Lambda Air ......................................... SUCCESS [02:20 
min]
[INFO] Lambda Air ......................................... SUCCESS [01:06 
min]
[INFO] Lambda Air ......................................... SUCCESS [  
1.659 s]
[INFO] ---------------------------------------------------------------
---------
[INFO] BUILD SUCCESS
[INFO] ---------------------------------------------------------------
---------
[INFO] Total time: 09:55 min
[INFO] Finished at: 2017-12-08T16:03:12-08:00
[INFO] Final Memory: 67M/661M
[INFO] ---------------------------------------------------------------
---------
```

以上是RedHat官方的做法: 用*fabric8* maven插件, 直接将源代码打成镜像, 并推送到镜像仓库. 另外会直接访问OpenShift去创建相关的 *Deployment*, *Service*, *Route*等. 

#### Farbic8 详细解释

maven Farbic8:deploy 举一个 airports 的构建例子, 具体构建日志如下:

1. 运行于 K8S mode: `[INFO] F8: Running in Kubernetes mode`

2. generator spring-boot. `[INFO] F8: Running generator spring-boot`

3. 使用Docker Image: `registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift`作为基础镜像和构建镜像. `[INFO] F8: spring-boot: Using Docker image registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift as base / builder`

4. 使用`Airports\src\main\fabric8` resource templates, 里边包括`deployment.yml`和`svc.yml`. 用于创建OpenShift Deployment和Service. `[INFO] F8: using resource templates from D:\Projects\spring-boot-msa-ocp\Airports\src\main\fabric8`

5. 由于使用了spring-boot的`spring-boot-starter-actuator`, 所以会自动加 Readiness Probe. `INFO] F8: spring-boot-health-check: Adding readiness probe on port 8080, path='/health', scheme='HTTP', with initial delay 10 seconds`

6. 同理, 也加了Liveness Probe: `[INFO] F8: spring-boot-health-check: Adding liveness probe on port 8080, path='/health', scheme='HTTP', with initial delay 180 seconds`

7. 还能自动加icon到Deployment和Service: `[INFO] F8: f8-icon: Adding icon for deployment [INFO] F8: f8-icon: Adding icon for service`

8. 找有没有OpenShift的 DeploymentConfig 的yaml文件, 没找到.

9. 找有没有K8S的Deployment 的yaml文件, 没找到.

10. 然后就可以常规的编译, 生成spring-boot jar包: `airports-1.0-SNAPSHOT.jar` 和 `airports-1.0-SNAPSHOT-exec.jar`

11. 把`airports-1.0-SNAPSHOT-exec.jar`拷贝到`target\docker\lambdaair\airports\snapshot-191114-101239-0722\build\maven`目录: `[INFO] Copying files to D:\Projects\spring-boot-msa-ocp\Airports\target\docker\lambdaair\airports\snapshot-191114-101239-0722\build\maven`

12. 然后用`Dockerfile` 执行`docker build`, 其实很简单的:

    ```dockerfile
    FROM registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift
    ENV JAVA_APP_DIR=/deployments
    EXPOSE 8080 8778 9779
    COPY maven /deployments/
    ```

13. 然后打上标签: `latest`

14. 接下来连接K8S或OpenShift控制台. (我用的是OpenShift 4.2, farbic8好像不兼容, 认成了K8S了. K8S创建的是Deployment, OpenShift创建的是DeploymentConfig).

15. 使用Project: `lambdaair`

16. 创建SVC: `[INFO] Updated Service: \target\fabric8\applyJson\lambdaair\service-airports.json`

17. 创建Deployment: `[INFO] Updated Deployment: \target\fabric8\applyJson\lambdaair\deployment-airports.json`. 这时候已经启动了Pod.

18. 完成.

```log
[INFO] >>> fabric8-maven-plugin:3.5.30:deploy (default-cli) > install @ airports >>>
[INFO]
[INFO] --- maven-resources-plugin:2.6:resources (default-resources) @ airports ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Copying 2 resources
[INFO]
[INFO] --- fabric8-maven-plugin:3.5.30:resource (default) @ airports ---
[INFO] F8: Running in Kubernetes mode
[INFO] F8: Running generator spring-boot
[INFO] F8: spring-boot: Using Docker image registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift as base / builder
[INFO] F8: using resource templates from D:\Projects\spring-boot-msa-ocp\Airports\src\main\fabric8
[INFO] F8: spring-boot-health-check: Adding readiness probe on port 8080, path='/health', scheme='HTTP', with initial delay 10 seconds
[INFO] F8: spring-boot-health-check: Adding liveness probe on port 8080, path='/health', scheme='HTTP', with initial delay 180 seconds
[INFO] F8: fmp-revision-history: Adding revision history limit to 2
[INFO] F8: f8-icon: Adding icon for deployment
[INFO] F8: f8-icon: Adding icon for service
[INFO] F8: validating D:\Projects\spring-boot-msa-ocp\Airports\target\classes\META-INF\fabric8\openshift\airports-deploymentconfig.yml resource
[ERROR] Failed to load json schema!
java.net.ConnectException: Connection timed out: connect
    at java.net.DualStackPlainSocketImpl.connect0 (Native Method)
    at java.net.DualStackPlainSocketImpl.socketConnect (DualStackPlainSocketImpl.java:79)
    at java.net.AbstractPlainSocketImpl.doConnect (AbstractPlainSocketImpl.java:350)
    at java.net.AbstractPlainSocketImpl.connectToAddress (AbstractPlainSocketImpl.java:206)
    at java.net.AbstractPlainSocketImpl.connect (AbstractPlainSocketImpl.java:188)
    at java.net.PlainSocketImpl.connect (PlainSocketImpl.java:172)
    at java.net.SocksSocketImpl.connect (SocksSocketImpl.java:392)
    at java.net.Socket.connect (Socket.java:607)
    at sun.security.ssl.SSLSocketImpl.connect (SSLSocketImpl.java:666)
    at sun.security.ssl.BaseSSLSocketImpl.connect (BaseSSLSocketImpl.java:173)
    at sun.net.NetworkClient.doConnect (NetworkClient.java:180)
    at sun.net.www.http.HttpClient.openServer (HttpClient.java:463)
    at sun.net.www.http.HttpClient.openServer (HttpClient.java:558)
    at sun.net.www.protocol.https.HttpsClient.<init> (HttpsClient.java:264)
    at sun.net.www.protocol.https.HttpsClient.New (HttpsClient.java:367)
    at sun.net.www.protocol.https.AbstractDelegateHttpsURLConnection.getNewHttpClient (AbstractDelegateHttpsURLConnection.java:191)
    at sun.net.www.protocol.http.HttpURLConnection.plainConnect0 (HttpURLConnection.java:1162)
    at sun.net.www.protocol.http.HttpURLConnection.plainConnect (HttpURLConnection.java:1056)
    at sun.net.www.protocol.https.AbstractDelegateHttpsURLConnection.connect (AbstractDelegateHttpsURLConnection.java:177)
    at sun.net.www.protocol.http.HttpURLConnection.getInputStream0 (HttpURLConnection.java:1570)
    at sun.net.www.protocol.http.HttpURLConnection.getInputStream (HttpURLConnection.java:1498)
    at sun.net.www.protocol.https.HttpsURLConnectionImpl.getInputStream (HttpsURLConnectionImpl.java:268)
    at java.net.URL.openStream (URL.java:1067)
    at com.networknt.schema.JsonSchemaFactory.getSchema (JsonSchemaFactory.java:63)
    at io.fabric8.maven.core.util.validator.ResourceValidator.getJsonSchema (ResourceValidator.java:156)
    at io.fabric8.maven.core.util.validator.ResourceValidator.validate (ResourceValidator.java:109)
    at io.fabric8.maven.plugin.mojo.build.ResourceMojo.validateIfRequired (ResourceMojo.java:286)
    at io.fabric8.maven.plugin.mojo.build.ResourceMojo.executeInternal (ResourceMojo.java:270)
    at io.fabric8.maven.plugin.mojo.AbstractFabric8Mojo.execute (AbstractFabric8Mojo.java:74)
    at org.apache.maven.plugin.DefaultBuildPluginManager.executeMojo (DefaultBuildPluginManager.java:137)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:210)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.MojoExecutor.executeForkedExecutions (MojoExecutor.java:355)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:200)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:117)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:81)
    at org.apache.maven.lifecycle.internal.builder.singlethreaded.SingleThreadedBuilder.build (SingleThreadedBuilder.java:56)
    at org.apache.maven.lifecycle.internal.LifecycleStarter.execute (LifecycleStarter.java:128)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:305)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:192)
    at org.apache.maven.DefaultMaven.execute (DefaultMaven.java:105)
    at org.apache.maven.cli.MavenCli.execute (MavenCli.java:956)
    at org.apache.maven.cli.MavenCli.doMain (MavenCli.java:288)
    at org.apache.maven.cli.MavenCli.main (MavenCli.java:192)
    at sun.reflect.NativeMethodAccessorImpl.invoke0 (Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke (NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke (DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke (Method.java:498)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launchEnhanced (Launcher.java:282)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launch (Launcher.java:225)
    at org.codehaus.plexus.classworlds.launcher.Launcher.mainWithExitCode (Launcher.java:406)
    at org.codehaus.plexus.classworlds.launcher.Launcher.main (Launcher.java:347)
[WARNING] F8: Failed to validate resources: java.net.ConnectException: Connection timed out: connect
[INFO] F8: validating D:\Projects\spring-boot-msa-ocp\Airports\target\classes\META-INF\fabric8\kubernetes\airports-deployment.yml resource
[ERROR] Failed to load json schema!
java.net.ConnectException: Connection timed out: connect
    at java.net.DualStackPlainSocketImpl.connect0 (Native Method)
    at java.net.DualStackPlainSocketImpl.socketConnect (DualStackPlainSocketImpl.java:79)
    at java.net.AbstractPlainSocketImpl.doConnect (AbstractPlainSocketImpl.java:350)
    at java.net.AbstractPlainSocketImpl.connectToAddress (AbstractPlainSocketImpl.java:206)
    at java.net.AbstractPlainSocketImpl.connect (AbstractPlainSocketImpl.java:188)
    at java.net.PlainSocketImpl.connect (PlainSocketImpl.java:172)
    at java.net.SocksSocketImpl.connect (SocksSocketImpl.java:392)
    at java.net.Socket.connect (Socket.java:607)
    at sun.security.ssl.SSLSocketImpl.connect (SSLSocketImpl.java:666)
    at sun.security.ssl.BaseSSLSocketImpl.connect (BaseSSLSocketImpl.java:173)
    at sun.net.NetworkClient.doConnect (NetworkClient.java:180)
    at sun.net.www.http.HttpClient.openServer (HttpClient.java:463)
    at sun.net.www.http.HttpClient.openServer (HttpClient.java:558)
    at sun.net.www.protocol.https.HttpsClient.<init> (HttpsClient.java:264)
    at sun.net.www.protocol.https.HttpsClient.New (HttpsClient.java:367)
    at sun.net.www.protocol.https.AbstractDelegateHttpsURLConnection.getNewHttpClient (AbstractDelegateHttpsURLConnection.java:191)
    at sun.net.www.protocol.http.HttpURLConnection.plainConnect0 (HttpURLConnection.java:1162)
    at sun.net.www.protocol.http.HttpURLConnection.plainConnect (HttpURLConnection.java:1056)
    at sun.net.www.protocol.https.AbstractDelegateHttpsURLConnection.connect (AbstractDelegateHttpsURLConnection.java:177)
    at sun.net.www.protocol.http.HttpURLConnection.getInputStream0 (HttpURLConnection.java:1570)
    at sun.net.www.protocol.http.HttpURLConnection.getInputStream (HttpURLConnection.java:1498)
    at sun.net.www.protocol.https.HttpsURLConnectionImpl.getInputStream (HttpsURLConnectionImpl.java:268)
    at java.net.URL.openStream (URL.java:1067)
    at com.networknt.schema.JsonSchemaFactory.getSchema (JsonSchemaFactory.java:63)
    at io.fabric8.maven.core.util.validator.ResourceValidator.getJsonSchema (ResourceValidator.java:156)
    at io.fabric8.maven.core.util.validator.ResourceValidator.validate (ResourceValidator.java:109)
    at io.fabric8.maven.plugin.mojo.build.ResourceMojo.validateIfRequired (ResourceMojo.java:286)
    at io.fabric8.maven.plugin.mojo.build.ResourceMojo.executeInternal (ResourceMojo.java:276)
    at io.fabric8.maven.plugin.mojo.AbstractFabric8Mojo.execute (AbstractFabric8Mojo.java:74)
    at org.apache.maven.plugin.DefaultBuildPluginManager.executeMojo (DefaultBuildPluginManager.java:137)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:210)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.MojoExecutor.executeForkedExecutions (MojoExecutor.java:355)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:200)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:117)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:81)
    at org.apache.maven.lifecycle.internal.builder.singlethreaded.SingleThreadedBuilder.build (SingleThreadedBuilder.java:56)
    at org.apache.maven.lifecycle.internal.LifecycleStarter.execute (LifecycleStarter.java:128)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:305)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:192)
    at org.apache.maven.DefaultMaven.execute (DefaultMaven.java:105)
    at org.apache.maven.cli.MavenCli.execute (MavenCli.java:956)
    at org.apache.maven.cli.MavenCli.doMain (MavenCli.java:288)
    at org.apache.maven.cli.MavenCli.main (MavenCli.java:192)
    at sun.reflect.NativeMethodAccessorImpl.invoke0 (Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke (NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke (DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke (Method.java:498)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launchEnhanced (Launcher.java:282)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launch (Launcher.java:225)
    at org.codehaus.plexus.classworlds.launcher.Launcher.mainWithExitCode (Launcher.java:406)
    at org.codehaus.plexus.classworlds.launcher.Launcher.main (Launcher.java:347)
[WARNING] F8: Failed to validate resources: java.net.ConnectException: Connection timed out: connect
[INFO]
[INFO] --- maven-compiler-plugin:3.6.1:compile (default-compile) @ airports ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 6 source files to D:\Projects\spring-boot-msa-ocp\Airports\target\classes
[INFO]
[INFO] --- maven-resources-plugin:2.6:testResources (default-testResources) @ airports ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory D:\Projects\spring-boot-msa-ocp\Airports\src\test\resources
[INFO]
[INFO] --- maven-compiler-plugin:3.6.1:testCompile (default-testCompile) @ airports ---
[INFO] No sources to compile
[INFO]
[INFO] --- maven-surefire-plugin:2.12.4:test (default-test) @ airports ---
[INFO] No tests to run.
[INFO]
[INFO] --- maven-jar-plugin:2.4:jar (default-jar) @ airports ---
[INFO] Building jar: D:\Projects\spring-boot-msa-ocp\Airports\target\airports-1.0-SNAPSHOT.jar
[INFO]
[INFO] --- spring-boot-maven-plugin:1.5.8.RELEASE:repackage (default) @ airports ---
[INFO] Attaching archive: D:\Projects\spring-boot-msa-ocp\Airports\target\airports-1.0-SNAPSHOT-exec.jar, with classifier: exec
[INFO]
[INFO] --- fabric8-maven-plugin:3.5.30:build (default) @ airports ---
[INFO] F8: Building Docker image in Kubernetes mode
[INFO] F8: Running generator spring-boot
[INFO] F8: spring-boot: Using Docker image registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift as base / builder
[INFO] Copying files to D:\Projects\spring-boot-msa-ocp\Airports\target\docker\lambdaair\airports\snapshot-191114-101239-0722\build\maven
[INFO] Building tar: D:\Projects\spring-boot-msa-ocp\Airports\target\docker\lambdaair\airports\snapshot-191114-101239-0722\tmp\docker-build.tar
[INFO] F8: [lambdaair/airports:snapshot-191114-101239-0722] "spring-boot": Created docker-build.tar in 142 milliseconds
[INFO] F8: [lambdaair/airports:snapshot-191114-101239-0722] "spring-boot": Built image sha256:f13a7
[INFO] F8: [lambdaair/airports:snapshot-191114-101239-0722] "spring-boot": Tag with latest
[INFO]
[INFO] --- maven-install-plugin:2.4:install (default-install) @ airports ---
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Airports\target\airports-1.0-SNAPSHOT.jar to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\airports\1.0-SNAPSHOT\airports-1.0-SNAPSHOT.jar
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Airports\pom.xml to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\airports\1.0-SNAPSHOT\airports-1.0-SNAPSHOT.pom
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Airports\target\classes\META-INF\fabric8\openshift.yml to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\airports\1.0-SNAPSHOT\airports-1.0-SNAPSHOT-openshift.yml
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Airports\target\classes\META-INF\fabric8\openshift.json to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\airports\1.0-SNAPSHOT\airports-1.0-SNAPSHOT-openshift.json
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Airports\target\classes\META-INF\fabric8\kubernetes.yml to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\airports\1.0-SNAPSHOT\airports-1.0-SNAPSHOT-kubernetes.yml
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Airports\target\classes\META-INF\fabric8\kubernetes.json to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\airports\1.0-SNAPSHOT\airports-1.0-SNAPSHOT-kubernetes.json
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Airports\target\airports-1.0-SNAPSHOT-exec.jar to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\airports\1.0-SNAPSHOT\airports-1.0-SNAPSHOT-exec.jar
[INFO]
[INFO] <<< fabric8-maven-plugin:3.5.30:deploy (default-cli) < install @ airports <<<
[INFO]
[INFO]
[INFO] --- fabric8-maven-plugin:3.5.30:deploy (default-cli) @ airports ---
[INFO] F8: Using Kubernetes at https://api.cce-test.ccic-net.com.cn:6443/ in namespace lambdaair with manifest D:\Projects\spring-boot-msa-ocp\Airports\target\classes\META-INF\fabric8\kubernetes.yml
[INFO] Using project: lambdaair
[INFO] Updating a Service from kubernetes.yml
[INFO] Updated Service: \target\fabric8\applyJson\lambdaair\service-airports.json
[INFO] Using project: lambdaair
[INFO] Updating Deployment from kubernetes.yml
[INFO] Updated Deployment: \target\fabric8\applyJson\lambdaair\deployment-airports.json
[INFO] F8: HINT: Use the command `kubectl get pods -w` to watch your pods start up
[INFO]
[INFO] ----------< com.redhat.refarch.spring.boot.lambdaair:flights >----------
[INFO] Building Lambda Air 1.0-SNAPSHOT                                   [2/7]
[INFO] --------------------------------[ jar ]---------------------------------
[INFO]
[INFO] --- maven-clean-plugin:2.5:clean (default-clean) @ flights ---
[INFO] Deleting D:\Projects\spring-boot-msa-ocp\Flights\target
[INFO]
[INFO] >>> fabric8-maven-plugin:3.5.30:deploy (default-cli) > install @ flights >>>
[INFO]
[INFO] --- maven-resources-plugin:2.6:resources (default-resources) @ flights ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Copying 2 resources
[INFO]
[INFO] --- fabric8-maven-plugin:3.5.30:resource (default) @ flights ---
[INFO] F8: Running in Kubernetes mode
[INFO] F8: Running generator spring-boot
[INFO] F8: spring-boot: Using Docker image registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift as base / builder
[INFO] F8: using resource templates from D:\Projects\spring-boot-msa-ocp\Flights\src\main\fabric8
[INFO] F8: spring-boot-health-check: Adding readiness probe on port 8080, path='/health', scheme='HTTP', with initial delay 10 seconds
[INFO] F8: spring-boot-health-check: Adding liveness probe on port 8080, path='/health', scheme='HTTP', with initial delay 180 seconds
[INFO] F8: fmp-revision-history: Adding revision history limit to 2
[INFO] F8: f8-icon: Adding icon for deployment
[INFO] F8: f8-icon: Adding icon for service
[INFO] F8: validating D:\Projects\spring-boot-msa-ocp\Flights\target\classes\META-INF\fabric8\openshift\flights-deploymentconfig.yml resource
[ERROR] Failed to load json schema!
java.net.ConnectException: Connection timed out: connect
    at java.net.DualStackPlainSocketImpl.connect0 (Native Method)
    at java.net.DualStackPlainSocketImpl.socketConnect (DualStackPlainSocketImpl.java:79)
    at java.net.AbstractPlainSocketImpl.doConnect (AbstractPlainSocketImpl.java:350)
    at java.net.AbstractPlainSocketImpl.connectToAddress (AbstractPlainSocketImpl.java:206)
    at java.net.AbstractPlainSocketImpl.connect (AbstractPlainSocketImpl.java:188)
    at java.net.PlainSocketImpl.connect (PlainSocketImpl.java:172)
    at java.net.SocksSocketImpl.connect (SocksSocketImpl.java:392)
    at java.net.Socket.connect (Socket.java:607)
    at sun.security.ssl.SSLSocketImpl.connect (SSLSocketImpl.java:666)
    at sun.security.ssl.BaseSSLSocketImpl.connect (BaseSSLSocketImpl.java:173)
    at sun.net.NetworkClient.doConnect (NetworkClient.java:180)
    at sun.net.www.http.HttpClient.openServer (HttpClient.java:463)
    at sun.net.www.http.HttpClient.openServer (HttpClient.java:558)
    at sun.net.www.protocol.https.HttpsClient.<init> (HttpsClient.java:264)
    at sun.net.www.protocol.https.HttpsClient.New (HttpsClient.java:367)
    at sun.net.www.protocol.https.AbstractDelegateHttpsURLConnection.getNewHttpClient (AbstractDelegateHttpsURLConnection.java:191)
    at sun.net.www.protocol.http.HttpURLConnection.plainConnect0 (HttpURLConnection.java:1162)
    at sun.net.www.protocol.http.HttpURLConnection.plainConnect (HttpURLConnection.java:1056)
    at sun.net.www.protocol.https.AbstractDelegateHttpsURLConnection.connect (AbstractDelegateHttpsURLConnection.java:177)
    at sun.net.www.protocol.http.HttpURLConnection.getInputStream0 (HttpURLConnection.java:1570)
    at sun.net.www.protocol.http.HttpURLConnection.getInputStream (HttpURLConnection.java:1498)
    at sun.net.www.protocol.https.HttpsURLConnectionImpl.getInputStream (HttpsURLConnectionImpl.java:268)
    at java.net.URL.openStream (URL.java:1067)
    at com.networknt.schema.JsonSchemaFactory.getSchema (JsonSchemaFactory.java:63)
    at io.fabric8.maven.core.util.validator.ResourceValidator.getJsonSchema (ResourceValidator.java:156)
    at io.fabric8.maven.core.util.validator.ResourceValidator.validate (ResourceValidator.java:109)
    at io.fabric8.maven.plugin.mojo.build.ResourceMojo.validateIfRequired (ResourceMojo.java:286)
    at io.fabric8.maven.plugin.mojo.build.ResourceMojo.executeInternal (ResourceMojo.java:270)
    at io.fabric8.maven.plugin.mojo.AbstractFabric8Mojo.execute (AbstractFabric8Mojo.java:74)
    at org.apache.maven.plugin.DefaultBuildPluginManager.executeMojo (DefaultBuildPluginManager.java:137)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:210)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.MojoExecutor.executeForkedExecutions (MojoExecutor.java:355)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:200)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:117)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:81)
    at org.apache.maven.lifecycle.internal.builder.singlethreaded.SingleThreadedBuilder.build (SingleThreadedBuilder.java:56)
    at org.apache.maven.lifecycle.internal.LifecycleStarter.execute (LifecycleStarter.java:128)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:305)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:192)
    at org.apache.maven.DefaultMaven.execute (DefaultMaven.java:105)
    at org.apache.maven.cli.MavenCli.execute (MavenCli.java:956)
    at org.apache.maven.cli.MavenCli.doMain (MavenCli.java:288)
    at org.apache.maven.cli.MavenCli.main (MavenCli.java:192)
    at sun.reflect.NativeMethodAccessorImpl.invoke0 (Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke (NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke (DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke (Method.java:498)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launchEnhanced (Launcher.java:282)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launch (Launcher.java:225)
    at org.codehaus.plexus.classworlds.launcher.Launcher.mainWithExitCode (Launcher.java:406)
    at org.codehaus.plexus.classworlds.launcher.Launcher.main (Launcher.java:347)
[WARNING] F8: Failed to validate resources: java.net.ConnectException: Connection timed out: connect
[INFO] F8: validating D:\Projects\spring-boot-msa-ocp\Flights\target\classes\META-INF\fabric8\kubernetes\flights-deployment.yml resource
[ERROR] Failed to load json schema!
java.net.ConnectException: Connection timed out: connect
    at java.net.DualStackPlainSocketImpl.connect0 (Native Method)
    at java.net.DualStackPlainSocketImpl.socketConnect (DualStackPlainSocketImpl.java:79)
    at java.net.AbstractPlainSocketImpl.doConnect (AbstractPlainSocketImpl.java:350)
    at java.net.AbstractPlainSocketImpl.connectToAddress (AbstractPlainSocketImpl.java:206)
    at java.net.AbstractPlainSocketImpl.connect (AbstractPlainSocketImpl.java:188)
    at java.net.PlainSocketImpl.connect (PlainSocketImpl.java:172)
    at java.net.SocksSocketImpl.connect (SocksSocketImpl.java:392)
    at java.net.Socket.connect (Socket.java:607)
    at sun.security.ssl.SSLSocketImpl.connect (SSLSocketImpl.java:666)
    at sun.security.ssl.BaseSSLSocketImpl.connect (BaseSSLSocketImpl.java:173)
    at sun.net.NetworkClient.doConnect (NetworkClient.java:180)
    at sun.net.www.http.HttpClient.openServer (HttpClient.java:463)
    at sun.net.www.http.HttpClient.openServer (HttpClient.java:558)
    at sun.net.www.protocol.https.HttpsClient.<init> (HttpsClient.java:264)
    at sun.net.www.protocol.https.HttpsClient.New (HttpsClient.java:367)
    at sun.net.www.protocol.https.AbstractDelegateHttpsURLConnection.getNewHttpClient (AbstractDelegateHttpsURLConnection.java:191)
    at sun.net.www.protocol.http.HttpURLConnection.plainConnect0 (HttpURLConnection.java:1162)
    at sun.net.www.protocol.http.HttpURLConnection.plainConnect (HttpURLConnection.java:1056)
    at sun.net.www.protocol.https.AbstractDelegateHttpsURLConnection.connect (AbstractDelegateHttpsURLConnection.java:177)
    at sun.net.www.protocol.http.HttpURLConnection.getInputStream0 (HttpURLConnection.java:1570)
    at sun.net.www.protocol.http.HttpURLConnection.getInputStream (HttpURLConnection.java:1498)
    at sun.net.www.protocol.https.HttpsURLConnectionImpl.getInputStream (HttpsURLConnectionImpl.java:268)
    at java.net.URL.openStream (URL.java:1067)
    at com.networknt.schema.JsonSchemaFactory.getSchema (JsonSchemaFactory.java:63)
    at io.fabric8.maven.core.util.validator.ResourceValidator.getJsonSchema (ResourceValidator.java:156)
    at io.fabric8.maven.core.util.validator.ResourceValidator.validate (ResourceValidator.java:109)
    at io.fabric8.maven.plugin.mojo.build.ResourceMojo.validateIfRequired (ResourceMojo.java:286)
    at io.fabric8.maven.plugin.mojo.build.ResourceMojo.executeInternal (ResourceMojo.java:276)
    at io.fabric8.maven.plugin.mojo.AbstractFabric8Mojo.execute (AbstractFabric8Mojo.java:74)
    at org.apache.maven.plugin.DefaultBuildPluginManager.executeMojo (DefaultBuildPluginManager.java:137)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:210)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.MojoExecutor.executeForkedExecutions (MojoExecutor.java:355)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:200)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:117)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:81)
    at org.apache.maven.lifecycle.internal.builder.singlethreaded.SingleThreadedBuilder.build (SingleThreadedBuilder.java:56)
    at org.apache.maven.lifecycle.internal.LifecycleStarter.execute (LifecycleStarter.java:128)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:305)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:192)
    at org.apache.maven.DefaultMaven.execute (DefaultMaven.java:105)
    at org.apache.maven.cli.MavenCli.execute (MavenCli.java:956)
    at org.apache.maven.cli.MavenCli.doMain (MavenCli.java:288)
    at org.apache.maven.cli.MavenCli.main (MavenCli.java:192)
    at sun.reflect.NativeMethodAccessorImpl.invoke0 (Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke (NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke (DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke (Method.java:498)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launchEnhanced (Launcher.java:282)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launch (Launcher.java:225)
    at org.codehaus.plexus.classworlds.launcher.Launcher.mainWithExitCode (Launcher.java:406)
    at org.codehaus.plexus.classworlds.launcher.Launcher.main (Launcher.java:347)
[WARNING] F8: Failed to validate resources: java.net.ConnectException: Connection timed out: connect
[INFO]
[INFO] --- maven-compiler-plugin:3.6.1:compile (default-compile) @ flights ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 8 source files to D:\Projects\spring-boot-msa-ocp\Flights\target\classes
[INFO]
[INFO] --- maven-resources-plugin:2.6:testResources (default-testResources) @ flights ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory D:\Projects\spring-boot-msa-ocp\Flights\src\test\resources
[INFO]
[INFO] --- maven-compiler-plugin:3.6.1:testCompile (default-testCompile) @ flights ---
[INFO] No sources to compile
[INFO]
[INFO] --- maven-surefire-plugin:2.12.4:test (default-test) @ flights ---
[INFO] No tests to run.
[INFO]
[INFO] --- maven-jar-plugin:2.4:jar (default-jar) @ flights ---
[INFO] Building jar: D:\Projects\spring-boot-msa-ocp\Flights\target\flights-1.0-SNAPSHOT.jar
[INFO]
[INFO] --- spring-boot-maven-plugin:1.5.8.RELEASE:repackage (default) @ flights ---
[INFO] Attaching archive: D:\Projects\spring-boot-msa-ocp\Flights\target\flights-1.0-SNAPSHOT-exec.jar, with classifier: exec
[INFO]
[INFO] --- fabric8-maven-plugin:3.5.30:build (default) @ flights ---
[INFO] F8: Building Docker image in Kubernetes mode
[INFO] F8: Running generator spring-boot
[INFO] F8: spring-boot: Using Docker image registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift as base / builder
[INFO] Copying files to D:\Projects\spring-boot-msa-ocp\Flights\target\docker\lambdaair\flights\snapshot-191114-101329-0408\build\maven
[INFO] Building tar: D:\Projects\spring-boot-msa-ocp\Flights\target\docker\lambdaair\flights\snapshot-191114-101329-0408\tmp\docker-build.tar
[INFO] F8: [lambdaair/flights:snapshot-191114-101329-0408] "spring-boot": Created docker-build.tar in 111 milliseconds
[INFO] F8: [lambdaair/flights:snapshot-191114-101329-0408] "spring-boot": Built image sha256:18eaa
[INFO] F8: [lambdaair/flights:snapshot-191114-101329-0408] "spring-boot": Tag with latest
[INFO]
[INFO] --- maven-install-plugin:2.4:install (default-install) @ flights ---
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Flights\target\flights-1.0-SNAPSHOT.jar to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\flights\1.0-SNAPSHOT\flights-1.0-SNAPSHOT.jar
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Flights\pom.xml to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\flights\1.0-SNAPSHOT\flights-1.0-SNAPSHOT.pom
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Flights\target\classes\META-INF\fabric8\openshift.yml to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\flights\1.0-SNAPSHOT\flights-1.0-SNAPSHOT-openshift.yml
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Flights\target\classes\META-INF\fabric8\openshift.json to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\flights\1.0-SNAPSHOT\flights-1.0-SNAPSHOT-openshift.json
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Flights\target\classes\META-INF\fabric8\kubernetes.yml to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\flights\1.0-SNAPSHOT\flights-1.0-SNAPSHOT-kubernetes.yml
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Flights\target\classes\META-INF\fabric8\kubernetes.json to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\flights\1.0-SNAPSHOT\flights-1.0-SNAPSHOT-kubernetes.json
[INFO] Installing D:\Projects\spring-boot-msa-ocp\Flights\target\flights-1.0-SNAPSHOT-exec.jar to C:\Users\8000619804\.m2\repository\com\redhat\refarch\spring\boot\lambdaair\flights\1.0-SNAPSHOT\flights-1.0-SNAPSHOT-exec.jar
```

一旦所有服务都被构建和部署，应该总共有8个运行的pod，包括之前的2个Zipkin pod，以及6个服务中的每一个新的pod:

```shell
$ oc get pods
NAME                       READY     STATUS      RESTARTS   AGE
airports-1-72kng           1/1       Running     0          18m
flights-1-4xkfv            1/1       Running     0          15m
presentation-1-k2xlz       1/1       Running     0          10m
sales-1-fqxjd              1/1       Running     0          7m
salesv2-1-s1wq0            1/1       Running     0          5m
zipkin-1-k0dv6             1/1       Running     0          1h
zipkin-mysql-1-g44s7       1/1       Running     0          1h
zuul-1-2jkj0               1/1       Running     0          1m
```

## 小结

*presentation* 服务还创建一个Route。再次列出OpenShift项目中的路由:

```shell
$ oc get routes
NAME           HOST/PORT                                    PATH      SERVICES       PORT      TERMINATION   WILDCARD
presentation   presentation-lambdaair.ocp.xxx.example.com             presentation   8080                    None
zipkin         zipkin-lambdaair.ocp.xxx.example.com                   zipkin         9411                    None
```

使用路由的URL从浏览器访问HTML应用程序，并验证它是否出现.