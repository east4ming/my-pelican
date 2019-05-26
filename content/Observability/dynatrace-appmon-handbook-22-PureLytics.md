Title: Dynatrace AppMon 实战手册 - 22.数据流接口-PureLytics
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第二十二篇, 主要介绍如何通过Dynatrace PureLytics将大数据导出到Hadoop ELK等大数据分析平台.

## 概览

PureLytics stream从AppMon Server发送实时UEM数据到外部数据源如Elasticsearch，这样你可以利用UEM数据作为大数据分析的一部分。流数据包括用户访问，用户行为和客户端错误。

使用Elasticsearch，基于大量的访问和用户行为数据来做即席分析，并且结合来自其他源的分析数据。你可以通过使用可视化工具如Kibana做细节图和其他数据可视化来消耗来自外部源的存储组合数据，以此提供详细的用户体验分析。

当启用时，PureLytics stream自动发送所有访问和用户行为的JSON数据到配置的HTTP端点。导出也可以在特定时间或session按命令触发。

![](http://pic.yupoo.com/east4ming_v/FX1LCylT/medium.jpg)

> 关于Elasticsearch
>
> Elasticsearch is a highly scalable open-source search engine with a full-text search-engine library. It includes a distributed real-time document store where all fields are indexed and can be searched. Streaming live UEM data to Elasticsearch provides multi-dimensional Ad-hoc analysis on large data sets over long time frames.

### JSON Document 格式

访问，用户行为，和客户端错误数据作为JSON导出。对于访问、用户行为的Business Transactions也作为JSON的一部分导出。

> JSON  Document 示例
>
> 下表展示了导出JSON的示例
>
> | Visit                                    | User Action                              | Client Error                             |
> | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
> | [Browser Visit](https://community.dynatrace.com/community/download/attachments/221381017/browser_visit.txt?version=3&modificationDate=1453723096180&api=v2) | [Browser User Action](https://community.dynatrace.com/community/download/attachments/221381017/browser_useraction.txt?version=6&modificationDate=1474979996337&api=v2) | [Javascript Error](https://community.dynatrace.com/community/download/attachments/221381017/javascript_error.txt?version=2&modificationDate=1453723238497&api=v2) |
> | [Mobile Visit](https://community.dynatrace.com/community/download/attachments/221381017/mobile_visit.txt?version=2&modificationDate=1453723109770&api=v2) | [Mobile User Action](https://community.dynatrace.com/community/download/attachments/221381017/mobile_useraction.txt?version=1&modificationDate=1453723162260&api=v2) | [Mobile Web Request](https://community.dynatrace.com/community/download/attachments/221381017/mobile_web_request.txt?version=2&modificationDate=1453723254897&api=v2) |
> |                                          |                                          | [Mobile Error Code](https://community.dynatrace.com/community/download/attachments/221381017/mobile_error_code.txt?version=1&modificationDate=1453723269387&api=v2) |
> |                                          |                                          | [Mobile Exception](https://community.dynatrace.com/community/download/attachments/221381017/mobile_exception.txt?version=1&modificationDate=1453723295607&api=v2) |
> |                                          |                                          | [Mobile Crash](https://community.dynatrace.com/community/download/attachments/221381017/mobile_crash.txt?version=1&modificationDate=1453723428797&api=v2) |
> |                                          |                                          | [Javascript Warning & Info](https://community.dynatrace.com/community/download/attachments/221381017/javascript_warning.txt?version=1&modificationDate=1453973925313&api=v2) |

## 使用PureLytics Stream整合Elasticsearch和Kibana

下列视频展示如何使用Kibana可视化来自PureLytics的数据的示例。

[PureLytics chats with ElasticSearch](https://s3.amazonaws.com/apmu-test-videos/RBZaCD-eEh41srh-wF0jkI/Whats_New_63_PurelyticsStream.mp4)

以下部分描述了使用Elasticsearch和Kibana来可视化PureLytics Stream的一般步骤。

### 需求和先决条件

> 需求和先决条件
>
> - Elasticsearch 1.5.2 or later. Elasticsearch 2.0.0 or higher is recommended because of the major stability improvements and improved resource use introduced in the 2.0.0 release.
>
>
> - Elasticsearch requires a recent version of Java on the machine where Elasticsearch runs. You can install the latest Java version from [www.java.com.](http://www.java.com/)
> - Most later versions of Kibana work seamlessly with Elasticsearch. However, the latest version of Kibana is recommended because of the increased level of integration with Elasticsearch and more robust analytics and charting features.
> - If running Elasticsearch on Windows, install cURL so you can quickly and conveniently submit requests to Elasticsearch. Download cURL from [`http://curl.haxx.se/download.html`](http://curl.haxx.se/download.html).
> - Familiarity with Elasticsearch is needed for deploying Elasticsearch, creating nodes and clusters, indexing, and executing Elasticsearch queries.
> - Familiarity with Kibana is needed for visualizing data.

### 安装Streaming Target软件和可视化软件

如果尚未安装，[install Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/guide/current/running-elasticsearch.html) 和 [install Kibana](https://www.elastic.co/downloads/kibana)。

### 启动Elasticsearch和配置集群

必须启动Elasticsearch并且至少在一个节点启动一个集群来创建JSON documents。最佳选择是使用至少2个节点来运行Elasticsearch 集群。

> 关于节点和集群的附加信息
>
> - It is recommended to create and use multiple nodes rather than one node with more CPU cores.
> - Node memory should be between 8 GB and 64 GB.
> - Get the fastest SSD you can get to boost performance.
> - Once started, communicate with Elasticsearch using the JSON based REST API residing at localhost port 9200. You can query Elasticsearch using cURL in Windows, or use graphical tools such as [Fiddler](http://www.telerik.com/fiddler) or [RESTClient](https://addons.mozilla.org/en-US/firefox/addon/restclient/) on other platforms. You can also use Elasticsearch's [Sense](https://www.elastic.co/guide/en/sense/current/introduction.html) plug-in, which is a simple user interface specifically for using ElasticSearch's REST API that includes auto-completion.
> - See the official Elasticsearch documentation on [Hardware](https://www.elastic.co/guide/en/elasticsearch/guide/current/hardware.html) and [Sizing Elasticsearch](https://www.elastic.co/blog/found-sizing-elasticsearch) for more information.

查看Elasticsearch 官网的[guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/running-elasticsearch.html)，来获取关于启动和使用Elasticsearch的更多信息。

### 应用一个动态模板

应用[dynamic template](https://community.dynatrace.com/community/download/attachments/221381017/dynamic_template.txt?version=2&modificationDate=1455701735027&api=v2) 到集群。

```JSON
PUT _template/dynatrace
{
  "order": 0,
  "template": "dt_*",
  "settings": {
     "number_of_shards": "6"
  },
  "mappings": {
     "useraction": {
        "dynamic_templates": [
           {
              "allStrings": {
                 "mapping": {
                    "index": "not_analyzed",
                    "type": "string"
                 },
                 "match_mapping_type": "string",
                 "match": "*"
              }
           }
        ],
        "properties": {
           "data": {
              "properties": {
                 "startTime": {
                    "type": "date"
                 },
                 "endTime": {
                    "type": "date"
                 },
                 "visitId": {
                     "type": "long"
                 },
                 "tagId": {
                     "type": "long"
                 },
                 "agentId": {
                     "type": "long"
                 },
                 "clientDetails": {
                    "properties" : {
                      "gpsCoordinates" : {
                        "type" : "geo_point"
                      }
                    }
                 },
                 "resourceReport": {
                   "properties" : {
                     "cdn" : {
                       "properties": {
                         "domains": {
                           "type": "nested"
                         }
                       }
                     },
                     "thirdParty" : {
                       "properties": {
                         "domains": {
                           "type": "nested"
                         }
                       }
                     }
                   }
                 }
              }
           }
        },
        "_parent": {
           "type": "visit"
        }
     },
     "visit": {
        "dynamic_templates": [
           {
              "allStrings": {
                 "mapping": {
                    "index": "not_analyzed",
                    "type": "string"
                 },
                 "match_mapping_type": "string",
                 "match": "*"
              }
           }
        ],
        "properties": {
           "data": {
              "properties": {
                 "startTime": {
                    "type": "date"
                 },
                 "endTime": {
                    "type": "date"
                 },
                 "visitId": {
                     "type": "long"
                 },
                 "clientDetails": {
                    "properties" : {
                      "gpsCoordinates" : {
                        "type" : "geo_point"
                      }
                    }
                 }
              }
           }
        }
     },
     "clienterror": {
      "dynamic_templates": [
           {
              "allStrings": {
                 "mapping": {
                    "index": "not_analyzed",
                    "type": "string"
                 },
                 "match_mapping_type": "string",
                 "match": "*"
              }
           }
        ],
        "properties": {
           "data": {
              "properties": {
                 "startTime": {
                    "type": "date"
                 },
                 "visitId": {
                    "type": "long"
                 },
                 "tagId": {
                     "type": "long"
                 },
                 "agentId": {
                     "type": "long"
                 },
                 "clientDetails": {
                    "properties" : {
                      "gpsCoordinates" : {
                        "type" : "geo_point"
                      }
                    }
                 }
              }
           }
        },
        "_parent": {
           "type": "visit"
        }
     }
  },
  "aliases": {}
}
```

### 配置PureLytics Stream

要配置AppMon来实时流传输PureLytics数据，启用PureLytics stream功能，指定Elasticsearch端点和其他AppMon Server关于实时流的设置，然后为你想导出数据的每个系统配置文件启用PureLytics stream。

> 配置PureLytics Stream
>
> 1. 在AppMon客户端设置里打开实时流(**Settings > Dynatrace Server > Realtime Streaming > PureLytics Stream**)
>
> 2. 检查**Configure PureLytics Stream.**
>
> 3. 选择你想导出JSON数据的目标。 你可以导出它们到一个Elasticsearch 集群或一个通用的HTTP端点 (使用与Elasticsearch相同的块格式).
>
> 4. 然后数据到Elasticsearch集群的URL或在**URL** field的通用HTTP端点（REST端口）。 **注意:**  PureLytics Stream 会在输入的URL后加上 **"/_bulk" **).
>
> 5. 如果你想使用HTTPS和使用非官方证书，可选**Allow untrusted SLL**。
>
> 6. 使用 **Dispatch Interval(s)** and **Queue Size**来设置每个请求块发送的数据量 和请求的间隔时间。
>
>    ​
>
>    A request is sent when the internal document queue hits the size specified in **Queue Size** **and/or** after the amount of time specified in **Dispatch Interval(s)**  has passed (*Dispatch Interval*). Request size is approximately the number of documents times 2 kB. This depends heavily on factors such as configured Business Transactions and resource timings.![img](https://community.dynatrace.com/community/download/thumbnails/221381017/config%20dialogue.png?version=2&modificationDate=1474975218090&api=v2)
>
> 7. 点击**OK**.
>
> 8. 在** Cockpits** 标签页,双击指定的系统配置文件来打开 该配置文件的Preferences 会话框。
>
> 9. 在常用标签页, 勾选**PureLytics Stream** 并点击 **OK**.
>    ![Enable the PureLytics Stream for each System Profile you want to export](https://community.dynatrace.com/community/download/thumbnails/221381017/system_profile.png?version=3&modificationDate=1474975882020&api=v2)

### 按命令导出

你可以在AppMon客户端按命令导出指定的数据，或者使用PureLytics Stream REST API来导出。

> 使用Dynatrace 客户端
>
> - 右存储的或实时的包含要导出数据的会话 并选择 **PureLytics Stream**.
>
> ![img](https://community.dynatrace.com/community/download/thumbnails/221381017/on_demand_export.png?version=3&modificationDate=1474976227450&api=v2)
>
> - 指定抓取的PureLytics stream的时间范围和哪些内容要导出（用户行为和/或访问）。 按需修改stream配置并点击 **Stream**.
>   ![img](https://community.dynatrace.com/community/download/thumbnails/221381017/on_demand_export_dialogue.png?version=4&modificationDate=1474979722060&api=v2)
>
> 使用REST接口
>
> 使用REST API来触发和监控一个按命令导出。 更多信息查看 [PureLytics Stream (REST)](https://community.dynatrace.com/community/pages/viewpage.action?pageId=221381578).
>
> - Create a job that exports data with a POST request. For example:
>
>   `POST https://<server>:8021/rest/management/profiles/<profilename>/analyticsstreamjob`
>
>   ​
>
> - Monitor the job with a GET request. For example:
>
>   `GET https://<server>:8021/rest/management/profiles/<profilename>/analyticsstreamjob/<jobId>`
>
>

### 在Kibana中可视化数据

必须配置至少一种索引模式来使用Kibana。索引模式识别你想要搜索和可视化PureLytics数据的索引。每个你指定的索引模式必须符合你的Elasticsearch索引的名称。

![](http://pic.yupoo.com/east4ming_v/FX1LBTRo/10UZbY.png)

## 技术细节和限制

- Documents在它们被分析后导出。 对于访问数据, 这意味者访问完成后documents才会被导出。一个访问在Elasticsearch中可视需要一定时间, 这个时间取决于访问的长度和配置的访问超时。
- 每个配置的系统文件存储在*每个时间戳的索引上*。每月创建一个索引，并以此命名。 例如, 开始于2016年1月的访问、用户行为和客户端错误 (使用document field `data.startTime`) 存储于索引，命名为`dt_2016-01`.
- PureLytics streaming使用Elasticsearch bulk API ([https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)). AppMon UEM 添加 `/_bulk` 到配置的URL之后  (仅当目标“Elasticsearch”被选中)。单一请求包含多个不同类型的documents。Bulk API也需要额外的元数据，实际数据包含多种信息, 包括使用的索引， document type, 和document ID。

```JSON
{"index":{"_index":"dt_2016-03","_type":"visit","_id":"1860046861_14036"}}
{"serverID":1860046861,"serverName":"lnz124742d03","systemProfile":"easyTravel","data":{"visitId":14036,"startTime":1457606705739,"endTime":1457606729349,"duration":23610,"application":"easyTravel mobile","appVersion":"1.9","visitTag":null,"additionalTags":{},"userExperienceIndex":1.0,"userExperience":"satisfied","userExperienceReason":"Satisfied","connectionType":"WIFI","bandwidth":5496,"isConverted":0,"isBounced":0,"isCrashed":0,"pageViews":2,"userActions":7,"failedActions":0,"landingPage":{"title":"SearchJourneyActivity","responseTime":1909,"isFailed":0},"exitPage":{"title":"easyTravel - Terms of Use","responseTime":289,"isFailed":0},"clientType":"mobile","clientDetails":{"osFamily":"Android","osVersion":"Android 2.3.3","manufacturer":"Samsung","deviceName":"Galaxy S","modelId":"GT-I9000","resolution":"480x800","cpuInfo":"armv7","isRooted":0,"adkVersion":"6.1.1234","gpsCoordinates":{"lat":48.85832,"lon":2.29436},"applicationBuildVersion":"1234"},"ipAddress":"159.108.218.157","location":{"continent":"Europe","country":"France","region":"Ile-de-France","city":"Neuilly"},"convertedBy":null,"businessTransactions":{"Conversion+visits":{"measures":{},"splittings":null},"Visits+by+connection+type":{"measures":{},"splittings":{"Connection+Type+of+Visits":"WIFI"}}},"carrier":"Orange"}}
{"index":{"_index":"dt_2016-03","_type":"visit","_id":"1860046861_14037"}}
{"serverID":1860046861,"serverName":"lnz124742d03","systemProfile":"easyTravel","data":{"visitId":14037,"startTime":1457606708560,"endTime":1457606709023,"duration":463,"application":"easyTravel portal","appVersion":"1.8","visitTag":null,"additionalTags":{"Visits - App Version":"1.8"},"userExperienceIndex":0.0,"userExperience":"frustrated","userExperienceReason":"DueToErrorInLastAction","connectionType":"Broadband","bandwidth":5496,"isConverted":0,"isBounced":1,"isCrashed":0,"pageViews":1,"userActions":1,"failedActions":1,"landingPage":{"title":"easyTravel - Terms of Use","responseTime":463,"isFailed":1},"exitPage":{"title":"easyTravel - Terms of Use","responseTime":463,"isFailed":1},"clientType":"browser","clientDetails":{"osFamily":"Android","osVersion":"Android 4.0.x Ice Cream Sandwich","browserFamily":"Chrome Mobile","browserVersion":"38.0"},"ipAddress":"128.133.96.84","location":{"continent":"North America","country":"United States","region":"Alabama","city":"Montgomery"},"convertedBy":null,"businessTransactions":{"Conversion+visits":{"measures":{},"splittings":null},"Visits+by+connection+type":{"measures":{},"splittings":{"Connection+Type+of+Visits":"Broadband (>1500 kb/s)"}}},"browserErrors":1,"videoStreams":0,"audioStreams":0,"isp":"-"}}
{"index":{"_index":"dt_2016-03","_type":"useraction","_id":"1860046861_1385397273_1","parent":"1860046861_14036"}}
{"serverID":1860046861,"serverName":"lnz124742d03","systemProfile":"easyTravel","data":{"visitId":14036,"tagId":1,"agentId":1385397273,"startTime":1457606705739,"endTime":1457606707648,"visitTag":null,"additionalTags":{},"name":"searchJourney","prettyName":"searchJourney","type":"ActionEvent","actionGroup":"Mobile ADK Actions","actionGroupPerformanceBaseline":4000,"apdex":1.0,"userExperience":"satisfied","isFailed":0,"failingReasons":null,"responseTime":1909.0,"networkContributionTime":1665.6201,"serverContributionTime":26.379906,"thirdPartyContribution":-1.0,"cdnContribution":-1.0,"application":"easyTravel mobile","appVersion":"1.9","location":{"continent":"Europe","country":"France","region":"Ile-de-France","city":"Neuilly"},"clientDetails":{"osFamily":"Android","osVersion":"Android 2.3.3","manufacturer":"Samsung","deviceName":"Galaxy S","modelId":"GT-I9000","resolution":"480x800","cpuInfo":"armv7","isRooted":0,"adkVersion":"6.1.1234","gpsCoordinates":{"lat":48.85832,"lon":2.29436},"applicationBuildVersion":"1234","isPortrait":0,"batteryStatus":0.33563203,"totalMemory":790,"freeMemory":0.56,"runningProcesses":26,"networkTechnology":"802.11x","signalStrength":-115},"xhrUrl":null,"clientErrors":0,"serverErrors":0,"perceivedRenderTime":-1,"perceivedRenderTimeSlowestImageSrc":"-","source":{"name":"SearchJourneyActivity","viewDuration":3593},"target":{"name":"SearchJourneyActivity"},"resourceSummary":null,"navTiming":null,"onLoad":-1,"domready":0,"metaData":null,"adkStrings":{},"adkValues":{},"businessTransactions":{"Pageview+Apdex+by+Country":{"measures":{"Apdex":1.0},"splittings":{"Country+of+Visits":"France"}},"Pageview+Apdex+by+Application":{"measures":{"Apdex":1.0},"splittings":null}}}}
(...)
```
