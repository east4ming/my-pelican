Title: 使用OpenShift进行二进制构建
Status: published
Tags: openshift, docker, devops, git, containers
Author: 东风微鸣
Summary: OpenShift 推荐和常用的构建方式是: 直接从代码仓库(如GIT 或SVN)中拉取源码进行构建(即源码构建). 但是这一种构建方式并不能满足所有的需求, 所以还有一种构建方式就是: 二进制构建. 二进制构建适用于以下2个场景: 1.开发人员本地开发调试代码并构建; 2. OpenShift和 CI/CD的pipeline进行整合, 获取从前边平台(如自动化开发平台或测试平台)传过来的工件(即二进制包)并构建为镜像.
Image: /images/
Related_posts: openshift-and-kubernetes-whats-difference

[TOC]

## 介绍

OpenShift 推荐和常用的构建方式是: 直接从代码仓库(如GIT 或SVN)中拉取源码进行构建(即源码构建). 但是这一种构建方式并不能满足所有的需求, 所以还有一种构建方式就是: 二进制构建. 二进制构建适用于以下2个场景:

1. 开发人员本地开发调试代码并构建;
2. OpenShift和 CI/CD的pipeline进行整合, 获取从前边平台(如自动化开发平台或测试平台)传过来的工件(即二进制包)并构建为镜像.

OpenShift中的二进制构建功能允许开发人员将源代码或工件直接上传到构建(build)，而不是从Git存储库URL pull需要构建的源。通过源代码，Docker或自定义构建策略的 BuildConfig 都可以作为二进制构建启动。从本地工件启动构建时，现有源引用将替换为来自本地用户计算机的源。

可以使用几种方式提供源，这些方式对应于使用`start-build`命令时可用的参数：

- 从文件（`--from-file`）：当构建的整个源包含单个文件时就是这种情况。例如，它可能是用于Docker构建的`Dockerfile`，用于Java应用构建的`pom.xml`，或用于Ruby构建的`Gemfile`。
- 从目录（`--from-directory`）：当源在本地目录中并且未提交到Git存储库时使用此目录。`start-build` 命令将创建给定目录的存档，并将其作为源上传到构建器(builder)。
- 从存档（`--from-archive`）：当具有源的存档已存在时使用此选项。该存档可以是`tar`，`tar.gz`或`zip`格式。
- 从Git存储库（`--from-repo`）：源是当前用户本地计算机上的Git存储库的一部分。当前存储库的HEAD commit将被存档并发送到OpenShift进行构建。

### 用例

二进制构建适用于无法从现有Git存储库中提取源的需求。使用二进制构建的原因包括：

- 构建和测试本地代码的变更。克隆来自公共存储库的源，并将本地变更上传到OpenShift进行构建。而无需在任何地方提交或推送本地更改。
- 构建私有代码。新构建可以作为二进制构建从头开始。然后可以将源直接从本地工作站上传到OpenShift，而无需将其签入SCM。
- 使用其他来源的工件构建镜像。通过Jenkins pipeline，二进制构建可以用于整合使用Maven或C编译器等工具构建的工件，以及使用这些构建的运行时镜像。

### 限制

- 二进制构建无法重复。由于二进制构建依赖于在构建开始时用户上传工件，因此OpenShift无法重复相同的构建而无需用户每次都重复相同的上载。
- 无法自动触发二进制生成。它们只能在用户上传所需的二进制工件时手动启动。

> :exclamation:
>
> 以二进制构建方式启动的构建版本也可能具有已配置的源URL。如果是这种情况，触发器会成功启动构建，但源将来自配置的源URL，而不是来自上次构建运行时用户提供的源。(比如: 用户先从Git仓库下载了源码并修改, 用本地修改后的源码手动上传、构建，那么OpenShift会获取到Git仓库的URL, 如果配置了触发器, 下次构建就直接通过Git URL pull源码并自动构建, 而不是自动获取本地的源码.)

## 教程概述

以下教程假设您有一个可用的OpenShift集群，并且您有一个可以创建工件的项目。它要求您拥有本地`git`和`oc`客户端。

### 教程：构建本地代码更改

1. 基于现有源存储库创建新应用程序并为其创建路由：

    ```
    $ oc new-app https://github.com/openshift/ruby-hello-world.git
    $ oc expose svc/ruby-hello-world
    ```

2. 等待初始构建完成并通过route来查看应用程序的页面。你应该得到一个欢迎页面：

    ```
    $ oc get route ruby-hello-world
    ```

3. 在本地克隆存储库：

    ```
    $ git clone https://github.com/openshift/ruby-hello-world.git
    $ cd ruby-hello-world
    ```

4. 更改应用程序的视图。使用您喜欢的编辑器编辑 `views/main.rb`：将`<body>`标签更改为`<body style="background-color:blue">`。

5. 使用本地修改的源启动新构建。在存储库的本地目录中，运行：

    ```
    ----
    $ oc start-build ruby-hello-world --from-dir="." --follow
    ----
    ```

构建完成并重新部署应用程序后，指向应用程序主机的route应该会生成一个蓝色背景的页面。

您可以继续在本地进行更改并使用`oc start-build --from-dir`。

您还可以创建代码分支，在本地提交更改，并使用存储库的HEAD作为构建的源：

```
$ git checkout -b my_branch
$ git add .
$ git commit -m "My changes"
$ oc start-build ruby-hello-world --from-repo="." --follow
```

### 教程：构建私有代码

1. 创建一个本地目录来保存您的代码：

    ```
    $ mkdir myapp
    $ cd myapp
    ```

2. 在目录中创建一个名为`Dockerfile`的文件：

    ```
    FROM centos:centos7
 
    EXPOSE 8080
 
    COPY index.html /var/run/web/index.html
 
    CMD cd /var/run/web && python -m SimpleHTTPServer 8080
    ```

3. 创建一个`index.html`文件：

    ```
    <html>
      <head>
        <title>My local app</title>
      </head>
      <body>
        <h1>Hello World</h1>
        <p>This is my local application</p>
      </body>
    </html>
    ```

4. 为您的应用程序创建一个新的构建：

    ```
    $ oc new-build --strategy docker --binary --docker-image centos:centos7 --name myapp
    ```

5. 使用本地目录的内容启动二进制构建：

    ```
    $ oc start-build myapp --from-dir . --follow
    ```

6. 使用`new-app`部署应用程序，然后为其创建路由：

    ```
    $ oc new-app myapp
    $ oc expose svc/myapp
    ```

7. 获取指向对应应用主机的路由：

    ```
    $ oc get route myapp
    ```

在构建和部署代码之后，您可以通过更改本地文件并通过`oc start-build myapp --from-dir`再次调用启动新构建来进行迭代。构建完成后，代码将自动部署，更新的内容将在刷新页面时反映在浏览器中。

### 教程：来自 pipeline 的二进制工件

OpenShift上的Jenkins允许使用带有合适工具的slave镜像来构建代码。例如，您可以使用`maven` slave镜像来从代码存储库构建WAR包。但是，一旦构建了此工件，您需要将其提交到包含正确的运行时工件的镜像以运行您的代码。可以使用二进制构建将这些工件添加到运行时映像。在下面的教程中，我们将创建一个Jenkins pipeline，该pipeline使用`maven` slave构建WAR，然后使用带有`Dockerfile`的二进制构建将WAR添加到 wildfly 运行时映像。

1. 为您的应用程序创建一个新目录：

    ```
    $ mkdir mavenapp
    $ cd mavenapp
    ```

2. 创建一个`Dockerfile`将WAR复制到wildfly镜像内的适当位置以供执行。将以下内容复制到名为的本地文件 `Dockerfile`：

    ```
    FROM wildfly:latest
    COPY ROOT.war /wildfly/standalone/deployments/ROOT.war
    CMD  $STI_SCRIPTS_PATH/run
    ```

3. 为该`Dockerfile`创建一个新的BuildConfig：

    > :exclamation:
    >
    >   这将自动启动一个构建, 刚开始会构建失败，因为 `ROOT.war`工件尚不可用。下面的pipeline将使用二进制构建将该WAR包传递给构建。

    ```
    $ cat Dockerfile | oc new-build -D - --name mavenapp
    ```

4. 创建1个使用Jenkins pipeline的BuildConfig, 这个BuildConfig将构建1个WAR包，然后使用该WAR包和先前创建的`Dockerfile`来构建镜像。相同的模式可用于其他平台，其中二进制工件由一组工具构建，然后与最终的包含不同运行时的镜像组合。将以下代码保存到`mavenapp-pipeline.yml`：

    ```
    apiVersion: v1
    kind: BuildConfig
    metadata:
      name: mavenapp-pipeline
    spec:
      strategy:
        jenkinsPipelineStrategy:
          jenkinsfile: |-
            pipeline {
              agent { label "maven" }
              stages {
                stage("Clone Source") {
                  steps {
                    checkout([$class: 'GitSCM',
                                branches: [[name: '*/master']],
                                extensions: [
                                  [$class: 'RelativeTargetDirectory', relativeTargetDir: 'mavenapp']
                                ],
                                userRemoteConfigs: [[url: 'https://github.com/openshift/openshift-jee-sample.git']]
                            ])
                  }
                }
                stage("Build WAR") {
                  steps {
                    dir('mavenapp') {
                      sh 'mvn clean package -Popenshift'
                    }
                  }
                }
                stage("Build Image") {
                  steps {
                    dir('mavenapp/target') {
                      sh 'oc start-build mavenapp --from-dir . --follow'
                    }
                  }
                }
              }
            }
        type: JenkinsPipeline
      triggers: []
    ```

5. 创建pipeline 构建。如果Jenkins未部署到您的项目中，则使用管道创建的BuildConfig会先部署Jenkins。在Jenkins准备建立您的管道之前可能需要几分钟来启动。您可以通过调用`oc rollout status dc/jenkins`来检查Jenkins的状态：

    ```
    $ oc create -f ./mavenapp-pipeline.yml
    ```

6. 一旦Jenkins准备就绪，启动之前定义的管道：

    ```
    $ oc start-build mavenapp-pipeline
    ```

7. 管道构建完成后，使用`new-app`部署新应用程序并公开其route：

    ```
    $ oc new-app mavenapp
    $ oc expose svc/mavenapp
    ```

8. 使用浏览器，导航到应用程序的路径：

    ```
    $ oc get route mavenapp
    ```
