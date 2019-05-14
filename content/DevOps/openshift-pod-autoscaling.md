Title: 容器自动伸缩
Status: published
Tags: openshift, containers, docker, k8s,
Author: 东风微鸣
Summary: OpenShift 容器云平台可以对容器进行自动缩放, 当前, 自动缩放只能根据以下2个指标进行判断: CPU使用率和内存使用率.
Image: /images/Matrix-agent-Smith-clones.jpg

[TOC]

## 概览

![](./images/Matrix-agent-Smith-clones.jpg)

由`HorizontalPodAutoscaler`对象定义的横向pod自动伸缩器(autoscaler)指定系统应如何根据从属于该复制控制器(replication controller)或部署配置(deployment configuration)的pod收集的度量标准(metrics)自动增加或减少复制控制器或部署配置的规模。

## 使用Horizontal Pod Autoscalers的要求

要使用横向pod自动伸缩器(horizontal pod autoscalers)，您需要安装OpenShift Container Platform度量服务器：

```bash
$ ansible-playbook \
/usr/share/ansible/openshift-ansible/playbooks/metrics-server/config.yml \
-e openshift_metrics_server_install=true
```

您可以通过运行以下命令验证服务器是否已正确安装：

```bash
$ oc adm top node
$ oc adm top pod
```

有关这些命令的其他信息，请参阅 [查看Nodes](https://docs.openshift.com/container-platform/3.11/admin_guide/manage_nodes.html#viewing-nodes)和 [查看Pods](https://docs.openshift.com/container-platform/3.11/admin_guide/managing_pods.html#viewing-pods)。

## 支持的指标

Horizontal pod autoscalers支持以下度量标准：

| 指标       | 描述                                                         | API版本                                  |
| :--------- | :----------------------------------------------------------- | :--------------------------------------- |
| CPU利用率  | [请求的CPU的](https://docs.openshift.com/container-platform/3.11/dev_guide/compute_resources.html#dev-cpu-requests)百分比 | `autoscaling/v1`， `autoscaling/v2beta1` |
| 内存利用率 | 请求的内存百分比                                             | `autoscaling/v2beta1`                    |

## 自动缩放

您可以使用`oc autoscale`命令创建horizontal pod autoscaler，并指定要运行的pod 的最小和最大数量，以及pod应指向的 [CPU利用率](https://docs.openshift.com/container-platform/3.11/dev_guide/pod_autoscaling.html#creating-a-hpa)或[内存利用率](https://docs.openshift.com/container-platform/3.11/dev_guide/pod_autoscaling.html#pod-autoscaling-memory)。

创建horizontal pod autoscaler后，它开始尝试查询Heapster以获取pod上的指标。在Heapster获得初始指标之前可能需要一到两分钟。

在Heapster中提供度量标准后，horizontal pod autoscaler将计算当前度量标准利用率与所需度量标准利用率的比率，并相应地向上或向下扩展。缩放将定期发生，但在指标进入Heapster之前可能需要一到两分钟。

对于复制控制器(replication controller)，此扩展直接对应于复制控制器的副本。对于部署配置(deployment configuration)，此扩展直接对应于部署配置的副本计数。请注意，自动缩放仅适用于`Complete`阶段中的最新部署。

OpenShift Container Platform自动对资源进行核算，并防止在资源激增期间（例如启动期间）进行不必要的自动扩展。在向上扩展时，`unready`状态中的pod的CPU使用率为`0 CPU`，并且autoscaler在向下伸缩时会忽略这些pod。无法获取到指标的pod在向上伸缩时CPU使用率为0%，向下伸缩时CPU使用率为100%。这样可以在HPA决策期间实现更高的稳定性。要使用此功能，您必须配置 [readiness checks](https://docs.openshift.com/container-platform/3.11/dev_guide/application_health.html#dev-guide-application-health) 以确定是否可以使用新容器。

## 根据CPU利用率自动扩展

使用`oc autoscale`命令并指定在任何给定时间至少要运行的最大pod数。您可以选择指定pod的最小数量以及pod应该定位的平均CPU利用率，否则将从OpenShift Container Platform服务器获得这些默认值。

例如：

```bash
$ oc autoscale dc/frontend --min 1 --max 10 --cpu-percent=80
deploymentconfig "frontend" autoscaled
```

上面的示例在使用`autoscaling/v1`版本的horizontal pod autoscaler时会创建一个具有以下定义的horizontal pod autoscaler：

例1. Horizontal Pod Autoscaler 对象定义

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: frontend 
spec:
  scaleTargetRef:
    kind: DeploymentConfig 
    name: frontend 
    apiVersion: apps/v1 
    subresource: scale
  minReplicas: 1 
  maxReplicas: 10 
  cpuUtilization:
    targetCPUUtilizationPercentage: 80 
```

| 参数                           | 说明                                     |
| ------------------------------ | ---------------------------------------- |
| metadata.name                  | 这个horizontal pod autoscaler 对象的名字 |
| kind                           | 要伸缩的对象类型                         |
| scaleTargetRef.name            | 要伸缩的对象的名称                       |
| scaleTargetRef.apiVersion      | 要扩展的对象的API版本                    |
| minReplicas                    | 向下伸缩时的最小副本数                   |
| maxReplicas                    | 向上扩展时的最大副本数                   |
| targetCPUUtilizationPercentage | 理想情况下每个pod应使用的请求CPU的百分比 |

或者，在`oc autoscale`使用horizontal pod autoscaler的`v2beta1`版本时，该命令会创建一个具有以下定义的horizontal pod autoscaler:

```yaml
apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-resource-metrics-cpu 
spec:
  scaleTargetRef:
    apiVersion: apps/v1 
    kind: ReplicationController 
    name: hello-hpa-cpu 
  minReplicas: 1 
  maxReplicas: 10 
  metrics:
  - type: Resource
    resource:
      name: cpu
      targetAverageUtilization: 50 
```

| 参数                      | 说明                                     |
| ------------------------- | ---------------------------------------- |
| metadata.name             | 这个horizontal pod autoscaler 对象的名字 |
| scaleTargetRef.apiVersion | 要扩展的对象的API版本                    |
| kind                      | 要扩展的对象类型                         |
| scaleTargetRef.name       | 要缩放的对象的名称                       |
| minReplicas               | 向下伸缩时的最小副本数                   |
| maxReplicas               | 向上扩展时的最大副本数                   |
| targetAverageUtilization  | 每个pod应使用的请求CPU的平均百分比       |

## 根据内存利用率自动缩放

与基于CPU的自动缩放不同，基于内存的自动缩放需要使用YAML而不是使用`oc autoscale`命令来指定自动缩放器。（可选）您可以指定pod的最小数量以及pod应该定位的平均内存利用率，否则将从OpenShift Container Platform服务器获得这些默认值。

1. 基于内存的自动扩展仅适用`v2beta1`的自动扩展API 的版本。通过将以下内容添加到群集的`master-config.yaml`文件来启用基于内存的自动缩放：

```yaml
...
apiServerArguments:
  runtime-config:
  - apis/autoscaling/v2beta1=true
...
```

2. 将以下内容放在一个文件中，例如`hpa.yaml`：

```yaml
apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-resource-metrics-memory 
spec:
  scaleTargetRef:
    apiVersion: apps/v1 
    kind: ReplicationController 
    name: hello-hpa-memory 
  minReplicas: 1 
  maxReplicas: 10 
  metrics:
  - type: Resource
    resource:
      name: memory
      targetAverageUtilization: 50 
```

| 参数                      | 说明                                     |
| ------------------------- | ---------------------------------------- |
| metadata.name             | 这个horizontal pod autoscaler 对象的名字 |
| scaleTargetRef.apiVersion | 要扩展的对象的API版本                    |
| kind                      | 要扩展的对象类型                         |
| scaleTargetRef.name       | 要缩放的对象的名称                       |
| minReplicas               | 向下缩小时的最小副本数                   |
| maxReplicas               | 向上扩展时的最大副本数                   |
| targetAverageUtilization  | 每个pod应使用的请求内存的平均百分比      |

3. 然后，从上面的文件创建自动缩放器：`$ oc create -f hpa.yaml`

> :exclamation:注意:
>
> 要使基于内存的自动缩放工作，内存使用量必须与副本计数成比例地增加和减少。一般：
>
> - 副本计数的增加必然导致每个pod的内存（工作集 working set）使用率整体下降。
> - 副本计数的减少必然导致每个pod的内存使用量整体增加。
>
> 使用OpenShift Web控制台检查应用程序的内存行为，并确保在使用基于内存的自动缩放之前，您的应用程序满足这些要求。

## 查看Horizontal Pod Autoscaler

要查看Horizontal Pod Autoscaler的状态：

- 使用`oc get`命令可以查看有关CPU利用率和容器 limits 的信息：

    ```bash
    $ oc get hpa/hpa-resource-metrics-cpu
    NAME                         REFERENCE                                 TARGET    CURRENT  MINPODS        MAXPODS    AGE
    hpa-resource-metrics-cpu     DeploymentConfig/default/frontend/scale   80%       79%      1              10         8d
    ```

    输出包括以下内容：

    - **目标(Target)**。由部署配置控制(deployment configuration)的所有pod的目标平均CPU利用率。
    - **Current**。由部署配置(deployment configuration)控制的所有pod的当前CPU利用率。
    - **Minpods/Maxpods**。autoscaler可以设置的最小和最大副本数。

- 使用`oc describe`命令获取有关Horizontal Pod Autoscaler对象的详细信息。

```bash
$ oc describe hpa/hpa-resource-metrics-cpu
Name:                           hpa-resource-metrics-cpu
Namespace:                      default
Labels:                         <none>
CreationTimestamp:              Mon, 26 Oct 2015 21:13:47 -0400
Reference:                      DeploymentConfig/default/frontend/scale
Target CPU utilization:         80% 
Current CPU utilization:        79% 
Min replicas:                   1 
Max replicas:                   4 
ReplicationController pods:     1 current / 1 desired
Conditions: 
  Type                  Status  Reason                  Message
  ----                  ------  ------                  -------
  AbleToScale           True    ReadyForNewScale        the last scale time was sufficiently old as to warrant a new scale
  ScalingActive         True    ValidMetricFound        the HPA was able to successfully calculate a replica count from pods metric http_requests
  ScalingLimited        False   DesiredWithinRange      the desired replica count is within the acceptable range
Events:
```
| 参数                    | 说明                                     |
| ----------------------- | ---------------------------------------- |
| Target CPU utilization  | 每个pod应使用的请求内存的平均百分比。                        |
| Current CPU utilization | 由部署配置(deployment configuration)控制的所有pod的当前CPU利用率。 |
| Min replicas            | 要缩小到的最小副本数                                         |
| Max replicas            | 要扩展到的最大副本数                                         |
| Conditions              | 如果对象使用`v2alpha1`API，则显示[status conditions](https://docs.openshift.com/container-platform/3.11/dev_guide/pod_autoscaling.html#viewing-a-hpa-status)。 |

### 查看Horizontal Pod Autoscaler Status Conditions

您可以使用设置的状态条件(status conditions)来确定Horizontal Pod Autoscaler 是否能够进行缩放以及当前是否以任何方式限制它。

自动扩展API `v2beta1`的版本提供Horizontal Pod Autoscaler Status Conditions：

```yaml
kubernetesMasterConfig:
  ...
  apiServerArguments:
    runtime-config:
    - apis/autoscaling/v2beta1=true
```

设置以下状态条件：

- `AbleToScale` 指示Horizontal Pod Autoscaler 是否能够获取和更新 scales，以及是否有任何backoff 条件阻止缩放。
    - `True`表示缩放是允许的。
    - `False`表示对指定的原因缩放不允许。
- `ScalingActive` 指示是否启用Horizontal Pod Autoscaler （目标的副本计数不为零）并且能够计算所需的比例。
    - `True`状态表示度量工作正常。
    - `False`条件通常表明与获取指标时遇到问题。
- `ScalingLimited` 表示不允许自动缩放，因为达到了最大或最小副本计数。
    - `True`条件表明，为了进行缩放你需要提高或降低最小或最大副本数。
    - `False`状态表明请求的比例是允许的。

如果您需要添加或编辑此行，请重新启动OpenShift Container Platform服务：

```bash
#master-restart api
#master-restart controllers
```

要查看影响Horizontal Pod Autoscaler 的条件，请使用`oc describe hpa`。条件出现在`status.conditions`字段中：

```bash
$ oc describe hpa cm-test
Name:                           cm-test
Namespace:                      prom
Labels:                         <none>
Annotations:                    <none>
CreationTimestamp:              Fri, 16 Jun 2017 18:09:22 +0000
Reference:                      ReplicationController/cm-test
Metrics:                        ( current / target )
  "http_requests" on pods:      66m / 500m
Min replicas:                   1
Max replicas:                   4
ReplicationController pods:     1 current / 1 desired
Conditions: 
  Type                  Status  Reason                  Message
  ----                  ------  ------                  -------
  AbleToScale       True      ReadyForNewScale    the last scale time was sufficiently old as to warrant a new scale
  ScalingActive     True      ValidMetricFound    the HPA was able to successfully calculate a replica count from pods metric http_request
  ScalingLimited    False     DesiredWithinRange  the desired replica count is within the acceptable range
Events:
```

Horizontal Pod Autoscaler Status Conditions:

- `AbleToScale`条件指示HPA是否能够获取和更新比例，以及任何与backoff相关的条件是否会阻止扩展。
- `ScalingActive`状况指示HPA是否被启用（例如，目标的副本数不为零），并能够计算所需的scales。`False`状态通常表示获取指标的问题。
- `ScalingLimited`条件指示期望scale由Horizontal Pod Autoscaler的最大或最小上限。`True`状态一般预示着你可能需要在你的水平荚自动配置器升高或降低的最小或最大副本数量的限制。

以下是无法扩展的pod的示例：

```
Conditions:
  Type           Status    Reason            Message
  ----           ------    ------            -------
  AbleToScale    False     FailedGetScale    the HPA controller was unable to get the target's current scale: replicationcontrollers/scale.extensions "hello-hpa-cpu" not found
```

以下是无法获取缩放所需pod的指标示例：

```
Conditions:
  Type                  Status    Reason                    Message
  ----                  ------    ------                    -------
  AbleToScale           True     SucceededGetScale          the HPA controller was able to get the target's current scale
  ScalingActive         False    FailedGetResourceMetric    the HPA was unable to compute the replica count: unable to get metrics for resource cpu: no metrics returned from heapster
```

以下是请求的自动缩放小于所需最小值的pod示例：

```
Conditions:
  Type              Status    Reason              Message
  ----              ------    ------              -------
  AbleToScale       True      ReadyForNewScale    the last scale time was sufficiently old as to warrant a new scale
  ScalingActive     True      ValidMetricFound    the HPA was able to successfully calculate a replica count from pods metric http_request
  ScalingLimited    False     DesiredWithinRange  the desired replica count is within the acceptable range
Events:
```
