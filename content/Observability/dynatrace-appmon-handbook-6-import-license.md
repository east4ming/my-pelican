Title: Dynatrace AppMon 实战手册 - 6.Dynatrace 生产环境License导入
Author: 东风微鸣
Category: Observability
Tags: Dynatrace, Observability
Summary: Dynatrace AppMon 实战手册系列文章. 本文是第六篇, 主要是Dynatrace授权license的导入.

1. 在Dynatrace eservices -> [My Licenses](https://eservices.dynatrace.com/eservices/customers-licenses.jsf)找到对应的License Key的信息，点击**Download License File**，如下图：(下载后得到License文件名示例：**dynaTrace_license_201608031073.key**)

   ![下载未激活License](http://pic.yupoo.com/east4ming_v/FMMHkMhr/medium.jpg)

2. 进入到Dynatrace Server 设置 -> License，选择**导入**，如下图：

   ![导入未激活License](http://pic.yupoo.com/east4ming_v/FMMGDsAH/medium.jpg)

3. 点击**下一步**，出现如下图所示，如果Dynatrace Server无法连接到Internet，点击**跳过**：

   ![](http://pic.yupoo.com/east4ming_v/FMMGbuuD/medium.jpg)

4. 跳过后需要手动导入之前下载的**未激活的License文件**，如下图：

   ![从文件导入未激活License](http://pic.yupoo.com/east4ming_v/FMMGEfhk/medium.jpg)

5. 导入**未激活的License**后，会提示需要在网上进行**激活**的操作，如下图：

   ![需要网上激活](http://pic.yupoo.com/east4ming_v/FMMGEMTr/medium.jpg)

6. 点击下一步，会出现License激活的相关信息，主要的是**Activation Key**信息，为25位的大写字母和数字的组合，如下图：

   ![Activation Key](http://pic.yupoo.com/east4ming_v/FMMHj38Z/medium.jpg)

7. 记下该激活码信息，登陆Dynatrace eservices -> [My Licenses](https://eservices.dynatrace.com/eservices/customers-licenses.jsf),输入激活码激活,如下图：

   ![](http://pic.yupoo.com/east4ming_v/FMMHj7UN/medium.jpg)

8. 激活后会提示成功激活，并给出**已激活的License下载地址**，如下：

   ![](http://pic.yupoo.com/east4ming_v/FMMGFUk2/medium.jpg)

9. 下载**已激活License**，（下载后的文件示例：**dynaTrace_license_201608031073__activated.key**),再次导入，如下图：（导入**未激活的License**会提示**当前许可证尚未启用**；导入**已激活的License**提示会消失）

   ![导入已激活License](http://pic.yupoo.com/east4ming_v/FMMGGbCZ/medium.jpg)

10. 通过文件导入**已激活License**文件，如下图：

   ![通过文件导入已激活License](http://pic.yupoo.com/east4ming_v/FMMGGsUD/medium.jpg)

导入后成功激活，显示如下：

   ![成功激活](http://pic.yupoo.com/east4ming_v/FMMY9dbb/medium.jpg)
