Title: Dynatrace AppMon 实战手册 - 24.手机ADK
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第二十四篇, 主要介绍Dynatrace监控手机APP所用到的应用开发套件(ADK).

[TOC]
dynaTrace UEM的手机应用支持跟踪访问者、操作，你的iOS、安卓应用触发的PurePath操作。要跟踪用户行为，你必须添加手机APP的ADK方法调用到你的手机应用源代码里。当ADK内嵌进应用，用户体验数据可以以用户使用浏览器访问站点同样的方式被收集。
下图为手机APP ADK工作流
![workflow](http://pic.yupoo.com/east4ming_v/FiGXviWP/medium.jpg)

## 支持平台

- Apple iOS 5或更高（armv7,armv7s或更高架构）

- 谷歌Android2.2或更高

## 下载ADK

从[http://www.dynatrace.com/downloads/Downloads.aspx](http://www.dynatrace.com/downloads/Downloads.aspx)下载*dynatrace-mobile-adk-$VERSION.$BUILD.zip*

## 配置dynaTrace

安装步骤和安装UEM类似：

- 进行基本的dynaTrace安装。

- 应用UEM license，包括访问数。

- 安装Agent和用户体验Sensor在应用服务器或web服务器上。

## 和应用整合

对于和把ADK和手机应用整合的具体细节，参见下面的相关章节。

### 本地应用

#### iOS ADK

参见**iOS ADK安装和使用说明**

#### iOS 自动化使用说明

参见**iOS自动化使用说明**

#### Android ADK

参见**Android ADK安装和使用说明**

#### Android应用（APK）使用说明

参见**Android使用说明**

#### Hybrid应用

参见**Hybrid应用安装和使用说明**

## 关联Web请求

## iOS ADK安装和使用说明

### ADK安装

#### 1. 解包ADK到任意目录

#### 2. 添加这些文件到你的Xcode项目和iOS target：

- libCompuwareUEM.a

- CompuwareUEM.h

#### 3. 添加需要的框架和库到你的Xcode项目。

在项目导航里，选择你的项目，选择target，选择**Build Phases**标签页，展开**Link Binaries with Libraries**，点击 **+** 按钮，选择下列框架和库：

- libsqlite3.dylib

- CoreLocation.framework

- CoreTelephony.framework

- Security.framework

- SystemConfiguration.framework

- libz.dylib

- libc++.dylib

- MessageUI.framework

#### 4. 添加flags到**Other Linker Flags**

在项目导航里，选择你的项目，选择你的target，选择**Build Settings**，添加如下设置到**Other Linker Flags**设置：

- -Objc

#### 5. 设置编译选项**Strip Style**为**Debugging Symbols**

这会使你的包稍微增大，但是会保留完整的设备崩溃信息。

#### 6. 添加文档到Xcode：

复制*com.compuware.uem.iOS.CompuwareUEM.docset**到下列路径 ~/Library/Developer/Shared/Documentation/DocSets

#### 7. 基于Swift编程app的手工操作说明：

- 创建一个包括Mobile Agent header的Bridging header

```swift
#ifndef myApp_Bridging_Header_h

#define myApp_Bridging_Header_h

#import "CompuwareUEM.h"

#endif
```

- 在项目导航，选择你的项目，选择你的target，选择**Build Settings**，添加先下列选项到**Objective-C Bridging Header** 设置：$(SRCROOT)/myApp/Bridging-Header.h

### 使用说明

CompuwareUEM.h中定义了2个类来instrument你的iOS app。CompuwareUEM类用于管理ADK的操作。UEMAction类用于创建行为和相关报告。

#### CompuwareUEM

##### setMonitorCookie

    `+ (void) setMonitorCookie:(NSString *)cookieString`

| 参数|含义 |
|------------|-----------|
| cookieString |A cookie string such as MIGRATION_FLAG=3 or n1=v1; n2=v2. Pass nil to remove the Cookie header from requests.|

设置由ADK发送（当和后端建立链接或者发送数据到后端）的HTTP Cookie header的每个HTTP GET/POST请求。只有当你的网络架构里需要该cookie，这个方法才是必须的。这个方法必须被包含在startupWithApplicationName:serverURL:allowAnyCert:certificatePath:之前，来确保最早的请求也包括该cookie。它可以随时被再次调用（invoke）来改变cookie string。

##### startupWithApplicationName

```
+ (CPWR_StatusCode) startupWithApplicationName:(NSString *)applicationId
                                      serverURL:(NSString *)serverURL
                                   allowAnyCert:(BOOL)allowAnyCert
                                certificatePath:(NSString *)pathToCertificateAsDER
```

| 参数|含义 |
|------------|-----------|
| applicatonName |用户定义的应用识别符 (eg. @"EasyTravel" ). 在应用名称里不要使用下划线（_）。|
| serverURL |嵌入UEM agent的web server的URL (e.g. `http://myhost.mydomain.com:8080/agentLocation/`). 包括使用的传输协议( https or   http ) 和这个应用的dynaTrace UEM设置里指定的Agent 位置.|
| allowAnyCert |允许https通讯的任何认证。这个参数只在server name里指定https协议时生效|
| pathToCertificateAsDER |在DER规格料理的到证书（自签署）的路径；或nil。|

| 返回值|含义 |
|------------|-----------|
| CPWR_UemOn |ADK成功启动|
| CPWR_Error_InvalidParameter |*applicatonName*或*serverURL*参数为nil或空字符串。|
| CPWR_TruncatedEventName |*applicatonName*超过255个字符。|
| CPWR_Error_NotInitialized |数据库没有初始化|
| CPWR_UemOff |关闭中；完成后重启|

调用该方法来实例化ADK。**该方法必须在任何其他方法调用前被引用（invoked）。**如果在ADK没有关闭前，对该方法的多次调用将被忽略。如果*allowAnyCert*和使用自签名证书，那么需要用DER格式认证，它是被用作一个额外的锚点（anchor）来验证HTTPS通讯。例如：

    NSString *pathToCertificateAsDER = [[NSBundle mainBundle] pathForResource:@"easyTravelServerCert" ofType:@"der"];

##### shutdown

    + (CPWR_StatusCode) shutdown

| 返回值 |含义 |
|------------|-----------|
| CPWR_UemOff |成功关闭|
调用该方法来关闭ADK。收集的数据被发送到dynaTrace Server。这个方法直到本次操作成功或失败才会返回值。你不应该在主线程中调用该方法，因为它会导致你的UI无响应。如果操作失败，数据会保留。在数据过期前如果ADK被重启，数据会之后再次发送。

##### enableCrashReportingWithReport

取决于使用的语法，*enableCrashReportingWithReport*方法可以发送crash报告到dynaTrace Server， HockeyApp Server，Quincy Server或Victory Server，或发送crash电子邮件报告到指定接收者。

###### dynaTrace Server

    `+ (CPWR_StatusCode) enableCrashReportingWithReport:(BOOL)sendCrashReport`

| 参数 |含义 |
|------------|-----------|
| sendCrashReport |*True*：发送完整crash报告。*False*：只发送crash事件，不包含全部细节。|

| 返回值 |含义 |
|------------|-----------|
| CPWR_CrashReportingUnavailable |无法启用crash报告|
| CPWR_CrashReportingAvailable |crash报告已启用|
| CPWR_UemOff |ADK没有初始化或ADK没有在收集数据|
这个方法会激活ADK中的KSCrash框架来抓取信号和未处理的例外。crash发生时，在设备上一份报告被保存。app下次启动后，报告会被处理。如果参数为*True*，完整的iOS crash报告被发送到dynaTrace Server.否则包括一些关于crash线程的信息被发送，而不是完整的报告。如果在七天内相同的例外再次发生，crash数据不会被再次报告，但是附带之前已被报告的crash数据的crash事件会被报告。
~~关于发送到其他Server，略。~~

##### setGpsLocation

    `+ (CPWR_StatusCode) setGpsLocation:(id)gpsLocation`

| 参数 |含义 |
|------------|-----------|
| gpsLocation |从用户应用获得的带有GPS坐标的*CLLocation*对象|

| 返回值 |含义 |
|------------|-----------|
| CPWR_UemOn |ADK实例化，GPS坐标被接收。|
| CPWR_UemOff |ADK没有实例化，GPS坐标被接收。|
| CPWR_Error_InvalidParameter |参数非法|

使用该方法记录用户的当前GPS位置。ADK不会自动收集任何位置信息。当前dynaTrace Server版本不会对GPS位置信息进行处理，但是未来版本的dynaTrace会。

##### lastErrorCode

    `+ (CPWR_StatusCode) lastErrorCode`

返回与最近的内部ADK错误有关的错误代码。返回*0*表示没有错误。

##### lastErrorMsg

    `+ (NSString *) lastErrorMsg`

返回与最近的内部ADK错误有关的错误信息。如果没有错误会返回nil。

##### flushEvents

    `+ (CPWR_StatusCode) flushEvents`

| 返回值 |含义 |
|------------|-----------|
| CPWR_UemOn |ADK实例化。|
| CPWR_UemOff |ADK没有实例化。|
立即发送所有收集到的事件。为了减少网络阻塞/使用，收集的事件通常以包的形式来发送，最老的事件超过9分钟。使用该方法强制发送所有的收集到的事件而不管事件的收集时间。

#### UEMAction

##### enterActionWithName

```
    + (UEMAction *) enterActionWithName:(NSString *)actionName
    + (UEMAction *) enterActionWithName:(NSString *)actionName
                           parentAction:(UEMAction *)parentAction
```

| 参数 |含义 |
|------------|-----------|
| actionName |行为名|
| parentAction |当前行为的UEMAction对象|

| 返回值 |含义 |
|------------|-----------|
| CPWR_Error_InvalidParameter |*parentAction*为nil，*parentAction*已经结束，或行为名为nil或空|
| CPWR_UemOff |ADK没有实例化|
| CPWR_TruncatedEventName |行为名被缩短到最大长度。这是warning；行为仍然会创建。|
| CPWR_Error_InternalError |ADK内部错误发生|
启动一个行为，会在dynaTrace里产生一条手机行为。在你想计时的代码的开头调用该方法。你必须通过调用*leaveAction*设置行为结束。如果行为被成功创建，返回值是non-nil。如果报错，返回值是nil。调用lastErrorCode 或 lastErrorMsg来定位错误。
返回的*UEMAction*被保留，因此它如果不再需要那么必须被释放（只在non-ARC环境合法）。

##### leaveAction

    `- (CPWR_StatusCode) leaveAction`

| 返回值 |含义 |
|------------|-----------|
| CPWR_UemOn |行为成功结束|
| CPWR_UemOff |ADK已经关闭|
| CPWR_Error_ActionEnded |*UEMAction*已经结束。这意味着*leaveAction*已经在该行为或其父行为被调用|
| CPWR_Error_InternalError |发生数据库错误|
| CPWR_Error_ActionNotFound |行为不再存在。如果行为保持打开的时间大于发送间隔会发生。|
结束以前开始的行为。所有在一个行为开始结束之间的报告事件，值，或被标记的web请求讲师行为的一部分，例如嵌入手机行为的PurePath。调用该方法在你想计时的代码结尾。

##### endVisit

    - (CPWR_StatusCode) endVisit
    + (CPWR_StatusCode) endVisit

| 返回值 |含义 |
|------------|-----------|
| CPWR_UemOn |行为成功结束|
| CPWR_UemOff |ADK已经关闭|
| CPWR_Error_ActionEnded |*UEMAction*已经关闭。这意味着*leaveAction*已经被该行为或其父行为调用|
| CPWR_Error_InternalError |数据库错误|
| CPWR_Error_NotSupportedInFreeMode |该操作只支持更高版本|

结束当前访问，关闭所有当前行为（actions），传输期间的数据给server，然后开始一个新的访问。

##### reportEventWithName

    `- (CPWR_StatusCode) reportEventWithName:(NSString *)eventName`

| 返回值 |含义 |
|------------|-----------|
| eventName |事件名|

| 返回值 |含义 |
|------------|-----------|
| CPWR_UemOn |行为成功结束|
| CPWR_UemOff |ADK已经关闭|
| CPWR_Error_ActionEnded |*UEMAction*已经关闭。这意味着*leaveAction*已经被该行为或其父行为调用|
| CPWR_Error_InvalidParameter |事件名为nil或空|
| CPWR_TruncatedEventName |事件名被压缩到最大长度。这是warning；事件仍然会被创建|
| CPWR_Error_InternalError |发生数据库错误|

发送一个事件到dynaTrace，会产生一个节点的手机行为PurePath.

##### reportValueWithName

```
    - (CPWR_StatusCode) reportValueWithName:(NSString *)valueName
                                   intValue:(NSInteger)value
    - (CPWR_StatusCode) reportValueWithName:(NSString *)valueName
                                doubleValue:(double)doubleValue
    - (CPWR_StatusCode) reportValueWithName:(NSString *)valueName
                                stringValue:(NSString *)stringValue
```

| 参数 |含义 |
|------------|-----------|
| valueName |值的名称|
| intValue |0-2147483的整型值|
| doubleValue |double值|
| stringValue |字符串值|

| 返回值 |含义 |
|------------|-----------|
| CPWR_UemOn |值被成功创建|
| CPWR_UemOff |ADK已经关闭|
| CPWR_Error_actionEnded |*UEMAction*已经结束。这意味着*leaveAction*已经被该行为或其父行为调用|
| CPWR_Error_InvalidParameter |值的名称为nil或空|
| CPWR_TruncatedEventName |值的名称已经被限制到最大长度。这是warning：事件仍会创建|
| CPWR_Error_InternalError |数据库发生错误|
| CPWR_Error_NotSupprotedInFreeMode |免费版不支持含有*doubleValue*的*reportValueWithName*|
发送一个键/值对到dynaTrace，会产生一个节点的手机行为PurePath。这个值可以通过方法进行图表处理。

##### reportErrorWithName

```
    - (CPWR_StatusCode) reportErrorWithName:(NSString *)errorName
                                 errorValue:(NSInteger)errorValue
    - (CPWR_StatusCode) reportErrorWithName:(NSString *)errorName
                                  exception:(NSException *)exception
    + (CPWR_StatusCode) reportErrorWithName:(NSString *)errorName
                                 errorValue:(NSInteger)errorValue
    + (CPWR_StatusCode) reportErrorWithName:(NSString *)errorName
                                  exception:(NSException *)exception
```

| 参数 |含义 |
|------------|-----------|
| errorName |值的名称|
| errorValue |错误整型值|
| exception |例外描述被发送到Server|

| 返回值 |含义 |
|------------|-----------|
| CPWR_UemOn |错误值被成功创建|
| CPWR_UemOff |ADK已经关闭（或类的方法还没有实例化）|
| CPWR_Error_ActionEnded |*UEMAction*已经被关闭。这意味着*leaveAction*已经被该行为或其副行为调用。|
| CPWR_Error_InvalidParameter |值名称为nil或空|
| CPWR_TruncatedEventName |错误名已经被压缩至最大长度，这是warning；错误仍然会被创建。|
| CPWR_Error_InternalError |发生数据库错误。|
| CPWR_Error_NotSupportedInFreeMode |带有*exception*的*reportErrorWithName*在免费版中不受支持。|

##### getRequestTagHeader

    `- (NSString *) getRequestTagHeader`

你必须添加一个Web请求到dynaTrace Server，链接*UEMAction*到PurePath中，会返回HTTP头的名称。你不应该像平常那样调用该方法，因为该自动化请求标签应该抓取所有的网络请求。

##### getRequestTagValue

    `- (NSString *) getRequestTagValue`

返回由*getRequestTagHeader*返回的HTTP头的值。你不应该像平常那样调用该方法，因为该自动化请求标签应该抓取所有的网络请求。

#### 返回值定义

| 代码 | 值 |含义 |
|------------|-----------|-----------|
| CPWR_UemOff |1 |数据抓取关闭|
| CPWR_UemOn |2 |数据抓取开启，或方法被成功调用。|
| CPWR_CrashReportingUnavailable |4 |*KSCrash*框架无法实例化|
| CPWR_CrashReportingAvailable |5 |*KSCrash*成功实例化。|
| CPWR_Error_NotInitialized |-1 |ADK实例化失败|
| CPWR_Error_InvalidRange |-2 |整型值超过界限0-2147483|
| CPWR_Error_ActionNotFound |-4 |当使用JavaScript bridge，这意味着行为名没有找到|
| CPWR_Error_InvalidParameter |-5 |非法字段被发送给一个ADK方法|
| CPWR_Error_ActionEnded |-6 |在已经被*leaveAction*方法结束的行为执行了一个操作|
| CPWR_ReportErrorOff |-8 |dynaTrace Server已禁用错误报告。|
| CPWR_TruncatedEventName |-9 |一个行为，错误，或值名称太长而被压缩。|
| CPWR_Error_NotSupportedInFreeMode |-11 |该方法在免费版不被支持|

### 日志

> 你可以启用日志并且通过添加*cpwrUEM_logging*来设置日志级别。日志关键词在应用的*info.plist*文件。参见**iOS自动安装说明**。

实例说明
像这样，下列代码将创建一个用户行为PurePath：
*示例PurePath*
![用户行为PurePath](http://pic.yupoo.com/east4ming_v/FjNDMj8O/medium.jpg)

```swift
    #import "CompuwareUEM.h"
    - (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
    {
        ...
        // initialize CompuwareUEM here or anywhere else (mind that actions and events that occur before initialization are not reported to dynaTrace!)
        [CompuwareUEM startupWithApplicationName:@"easyTravel"
                                       serverURL:@"http://easytravel.example.com:8080/eT/"
                                    allowAnyCert:NO
                                 certificatePath:nil];
        ...
    }

    - (IBAction)performSearch:(id)sender
    {
        ...
        // [1a] start action "search"
        UEMAction *action = [UEMAction enterActionWithName:@"search"];
        // [2] named event inside an action
        [action reportEventWithName:@"searchStart"];
        // [3a] starting sub-action
        UEMAction *child = [UEMAction enterActionWithName:@"searchRequest"
                                             parentAction:action];
        // [4] NSURLRequest and NSMutableURLReqest are tagged automatically
        NSError* error;
        NSHTTPURLResponse* response;
        NSURL *searchURL = [[NSURL URLWithString:
                             [NSString stringWithFormat:@"http://127.0.0.1:8080/ajax/TimeService?tz=GMT",
                              [sender query]]] retain];
        NSData *data = [NSURLConnection sendSynchronousRequest:[NSURLRequest requestWithURL:searchURL]
                                             returningResponse:&response error:&error];
        [searchURL release];
        if(data == nil){
            // [x] report an error if communication fails
            [action reportErrorWithName:@"CommunicationError" errorValue:[error code]];
        }
        // [5] custom value inside an action
        [child reportValueWithName:@"responseCode" intValue:[response statusCode]];
        // [3b] end action "searchRequest"
        [child leaveAction];
        // [6] named event on successful completion
        [action reportEventWithName:@"searchEnd"];
        // [1b] end action "search"
        [action leaveAction];
        ...
    }


### 生命周期说明

在应用中很早实例化ADK来抓取初始视图展现或者使用自动启动功能。从*main()*调用*startupWithApplicationName*是可以的。

#### 限制

在dynaTrace5.6之前的版本，在**System Profile-Error Detection**条件中的特殊字符（如：空格）被ADK使用下划线自动替换。确定你有正确的比较字符串，因为5.6及以后版本的ADK不会替换这些字符串。

### 总结

添加iOS ADK到应用会增加如下大小：

| 架构 | 大小 |
|------------|-----------|
|armv7 |340KB |
|armv7s |340KB |
|arm64 |325KB |
|All three |980KB |

行为，事件，错误被自动创建或者通过ADK API被储存在一个在应用的Document路径的SQLite 数据库。平均下来，这些项在数据库中大概占用150 bytes。大小取决于项中的字符串的长度，像名称、错误信息。
默认情况下，ADK储存项在数据库中一直到2min在发送给Server端或者删除。你可以在dynaTrace 客户端管理发送间隔。


## iOS自动感知（Auto-Instrumentation）

*Auto-Instrumentation for iOS*允许任何人通过手机App ADK来监控iOS应用。该说明程序是自动添加标准手机App ADK到应用而不用手动修改源代码。标准手机App ADK用于自动化的处理进程。自动化添加的应用和手动添加的应用收集到的基本数据是一样的。该方法提供应用、crash监测、应用启动和web交易相应时间性能监控真实用户体验流。

### 自动化功能

下列功能是自动感知的：

- ADK自动启动-你必须使用instrumentation keys来配置自动启动。

- 生命周期数据

- crash报告

- web请求标记（tagging）

- web请求事件（报告执行时间和认证第三方请求）

- web视图

- 自动用户行为检测（真实用户行为像点按按钮及其他浏览操作和控制的监测和计时）

- ADK 日志记录-你必须使用相应的instrumentation key来启动自动日志记录

所有这些功能默认开启。你可以禁用或改进这些自动感知功能通过添加***configuration keys***到你的应用的*info.plist*文件。
你可以把自动感知和手动赶集结合起来。例如，你可能想在开发阶段手动获取确切用户定义的行为（并报告数值和事件），然后使用自动感知添加上列功能到你的应用。

### 自动感知概览

1. 链接iOS 手机ADK静态库到你的应用并且编译进Xcode。参见**iOS ADK安装使用说明**获取更多细节。
2. 添加keys到你的应用的*info.plist*文件，配置自动感知。
3. 在编译期间自动感知发生。之后应用会感知在*info.plist*文件中的级别配置。

#### 感知配置

下表的keys（properties）是自动感知的配置选项。根据需要添加keys到你的应用的info.plist文件。其中的很多属性值参考**CompuwareUEM 手机App ADK API**

| 关键字 | 关键字类型 |描述 |
|------------|-----------|-----------|
| cpwrUEM_logging.level |字符串 |如果该关键词合法（ALL,FINEST,FINER,FINE,CONFIG,INFO,WARNING,SEVERE,OFF），ADK日志记录就会自动启用对应等级。如果关键字没是哟个或者没有合法值，自动记录日志**关闭**，你必须手动在应用中开启日志记录功能。|
| cpwrUEM.setMonitorCookie |字符串 |如果配置该关键字，该值会自动作为HTTP请求到*serverUrl*(参见*cpwrUEM_startup.agentpath*)的一个cookie，这样他们可以通过你的基础架构需求。|
| cpwrUEM_startup.agentPath |字符串 |如果该关键字配置一个合法的值，ADK将自动启动，使用该值作为*serverUrl*,并将忽略你app中任何手动的*startupWithApplicationName*调用。*serverUrl*需要使用http://或https://传输。如果没配置，你必须手动调用*startupWithApplicationName*来启动ADK|
| cpwrUEM_startup.sApplId |字符串 |如果配置该关键字，它的值会被用作你应用的名称。如果没有配置，ADK将使用在main bundle中的应用名|
| cpwrUEM_startup.useAnyCert |布尔 |默认值是*NO*。该关键字等价于启动时调用*allowAnyCert*参数。如果设置为*YES*，所有证书都会被接受。如果设置为*NO*，来自已知认证机构的合法证书会被接受；如果提供了一个自签名证书（参见*cpwrUEM_startup.certPath*）,将检查它的有效性。|
| cpwrUEM_startup.certPath |字符串 |默认值为nil。该关键字定义了一个DER格式的（自签名）证书路径，用作一个额外的anchor来验证HTTPS通讯。如果*cpwrUEM_startup.useAnyCert*是*NO*,并且server上用了一个自签名的证书，那么需要使用该关键字。|
| cpwrUEM_crash.reporting |布尔 |默认值是*YES*。crash报告默认自动启用。如果你不想启动crash报告，你必须使用该关键字，并设置值为*NO*。如果你想报告crashes到一个不是dynaTrace server的server上，或者启用发送crash email通知，在你的代码里添加合适的*enableCrashReportingWithReport* API调用来覆盖默认配置。|
| cpwrUEM_crash.sendCrashReport |布尔 |默认值是*YES*。对于*enableCrashReportingWithReport*发送crash报告到dynaTrace server，它和*sendCrashReport*字段是等价的。如果你不想设置发送crash报告，设置该关键字为*NO*|
| cpwrUEM_instr.lifecycleMonitoring |布尔 |默认值是*YES*。不用使用iOS ADK生命周期类覆盖你的view controller 类，自动生命周期监测是启用的。设置该值为*NO*来禁用自动生命周期监测。|
| cpwrUEM_instr.webRequestTagging |布尔 |默认是*YES*，打开自动web请求标记。注意，如果*webRequestTiming*被启用，*webRequestTagging*也会启用，因为有依赖关系。要关闭自动web请求标记，你需要把*webRequestTiming*和*webRequestTagging*都设置为*NO*|
| cpwrUEM_instr.webRequestTiming |布尔 |默认是*YES*，即开启自动web请求计时。设置为*NO*禁用。注意该关键字和*webRequestTagging*相互依赖。|
| cpwrUEM_instr.wrapWebRequestInAction |布尔 |默认值是*YES*。如果一个手动用户行为或自动用户行为不可用，就自动把web请求包进用户行为里。设置该值为*NO*来禁用自动web请求行为包裹。|
| cpwrUEM_instr.autoUserAction |布尔 |默认值是*YES*。可以自动创建用户和app交互的行为（按按钮，跳转至其他页面，表单浏览选择等）.设置该值为*NO*来禁用该功能。|
| cpwrUEM_action.autoActionTimeoutMs |数字 |The default value is 500 ms. It sets the value for how long a particular automatic user action is active. The purpose is to catch all web requests that happen when an automatic user action is active. If the automatic user action has completed web requests, the ADK leaves the action at the end of this time. The minimum allowed value is 100 ms, the maximum allowed value is 5000 ms (5 seconds).|
| cpwrUEM_action.autoActionMaxDurationMs |数字 |The default value is 60000 ms (60 seconds). It sets the value for how long a particular automatic user action is retained before being deleted. The purpose is to catch all web requests that happen when an automatic user action is active. If the automatic user action has pending web requests (because they are taking a long time to complete), the ADK waits for this amount of time for the web requests to complete before leaving the user action. The minimum allowed value is 100 ms, the maximum allowed value is 540000 ms (9 minutes).|
| cpwrUEM_action.sendEmptyAutoAction |布尔 |The default value is NO. It determines whether to send automatic user actions if they do not contain any web requests or lifecycle actions.|
| cpwrUEM_instr.webViewTiming |布尔 |The default value is YES . It automatically detects and times  web views in your hybrid app. Set the value to   to disable automatic detection and timing of web views.|
| cpwrUEM_instr.excludeControls |数组 |This key defines an array of items where each item contains a type of view or control to exclude from automatic creation of user actions. Each item in the array is a case-insensitive string. The possible values are Button， toolBar segmentedControl tableView tabBar alertView and  pageView navigationController collectionView actionSheet|
| cpwrUEM_instr.excludeLifecycleClasses |数组 |This is an array of items where each item contains the name of a class to exclude from automatic lifecycle instrumentation. Each item in the array is a case-sensitive string that must **exactly** match the name of the class to be  excluded.|

### 限制

~~2698页~~
