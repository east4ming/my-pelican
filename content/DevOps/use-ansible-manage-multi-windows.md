# 使用 Ansible 批量管理 Windows

Title: 使用 Ansible 批量管理 Windows
Author: 东风微鸣
Category: DevOps
Tags: ansible, windows, devops
Summary: 在windows上安装winrm组件, Ansible通过winrm实现对windows的批量管理. 包括: 批量创建下发删除文件及目录、执行脚本、重启机器、管理用户、管理服务...
Image: /images/ansible_logo.png
Related_posts: DevOps-questionnaire

## 概述

Ansible是自动化运维工具，基于Python开发，实现了批量系统配置、批量程序部署、批量运行命令等功能。Ansible是基于模块(module)和剧本(playbook)工作。

## 安装指南

> 本次在Ubuntu上安装Ansible 2.7 . 更详细安装方式参见: [Ansible 安装指南](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

### 服务器端的要求

目前Ansible可以从安装了Python 2（2.7版）或Python 3（3.5及更高版本）的任何机器上运行。控制计算机**不支持Windows**。

这包括Red Hat，Debian，CentOS，macOS，任何BSD等等。

### 服务器端安装Ansible

#### 通过Apt (Ubuntu)安装最新版本

这里有[一个PPA](https://launchpad.net/~ansible/+archive/ubuntu/ansible)版本的Ubuntu源。

要在您的计算机上配置PPA并安装ansible，请运行以下命令：

```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install ansible
```

> :exclamation:
>
> 在较旧的Ubuntu发行版中，“software-properties-common”被称为“python-software-properties”。

## Windows 指南

### 设置Windows主机

#### 主机要求

要使Ansible与Windows主机通信并使用Windows模块，Windows主机必须满足以下要求：

- Ansible支持的Windows版本通常与Microsoft当前和扩展支持下的版本相匹配。支持的桌面操作系统包括**Windows 7,8.1和10**，受支持的服务器操作系统包括**Windows Server 2008,2008 R2,2012,2012 R2和2016**。
- Ansible需要**PowerShell 3.0**或更高版本，并且至少要在Windows主机上安装**.NET 4.0**。
- 应创建并激活**WinRM listener **。更多细节可以在下面找到。

> :exclamation:
>
> 虽然这些是Ansible连接的基本要求，但是一些Ansible模块还有其他要求，例如较新的OS或PowerShell版本。请参阅模块的文档页面以确定主机是否满足这些要求。

#### 升级PowerShell和.NET框架

> 升级powershell需要**重启服务器**才能生效。

Ansible需要PowerShell 3.0版和.NET Framework 4.0或更高版本才能在较旧的操作系统（如Server 2008和Windows 7）上运行。基本OS镜像不符合此要求。您可以使用[Upgrade-PowerShell.ps1](https://github.com/jborean93/ansible-windows/blob/master/scripts/Upgrade-PowerShell.ps1)脚本来更新这些脚本。

这是如何从PowerShell运行此脚本的示例：

```powershell
$url = "https://raw.githubusercontent.com/jborean93/ansible-windows/master/scripts/Upgrade-PowerShell.ps1"
$file = "$env:temp\Upgrade-PowerShell.ps1"
$username = "Administrator"
$password = "Password"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force

# version can be 3.0, 4.0 or 5.1
&$file -Version 5.1 -Username $username -Password $password -Verbose
```

完成后，您将需要删除自动登录并将执行策略设置回默认值`Restricted`。您可以使用以下PowerShell命令执行此操作：

```powershell
# this isn't needed but is a good security practice to complete
Set-ExecutionPolicy -ExecutionPolicy Restricted -Force

$reg_winlogon_path = "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"
Set-ItemProperty -Path $reg_winlogon_path -Name AutoAdminLogon -Value 0
Remove-ItemProperty -Path $reg_winlogon_path -Name DefaultUserName -ErrorAction SilentlyContinue
Remove-ItemProperty -Path $reg_winlogon_path -Name DefaultPassword -ErrorAction SilentlyContinue
```

该脚本的工作原理是检查需要安装哪些程序（例如.NET Framework 4.5.2）以及需要什么样的PowerShell版本。如果**需要重新启动**并且设置了`username`和`password`参数，则脚本将在重新启动时自动重新启动并登录。该脚本将继续，直到不再需要执行任何操作且PowerShell版本与目标版本匹配为止。如果未设置`username`和 `password`参数，脚本将提示用户手动重新引导并在需要时登录。当用户下次登录时，脚本将从停止的位置继续，并且该过程将继续，直到不再需要其他操作为止。

> :exclamation:
>
> - 如果在Server 2008上运行，则必须安装SP2。如果在Server 2008 R2或Windows 7上运行，则必须安装SP1。
> - Windows Server 2008只能安装PowerShell 3.0; 指定较新的版本将导致脚本失败。
> - `username`和`password`参数都是存储在注册表中的纯文本。确保在脚本完成后运行清理命令，以确保主机上仍未存储凭据。

#### WinRM内存补丁

在PowerShell v3.0上运行时，WinRM服务存在一个错误，它限制了WinRM可用的内存量。如果未安装此补丁，Ansible将无法在Windows主机上执行某些命令。这些补丁应作为系统引导或映像过程的一部分安装。[Install-WMF3Hotfix.ps1](https://github.com/jborean93/ansible-windows/blob/master/scripts/Install-WMF3Hotfix.ps1)脚本可用于在受影响的主机上安装此修补程序。

以下PowerShell命令将安装此修补程序：

```powershell
$url = "https://raw.githubusercontent.com/jborean93/ansible-windows/master/scripts/Install-WMF3Hotfix.ps1"
$file = "$env:temp\Install-WMF3Hotfix.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
powershell.exe -ExecutionPolicy ByPass -File $file -Verbose
```

#### WinRM设置

一旦Powershell升级到至少3.0版本，最后一步是配置WinRM服务，以便Ansible可以连接到它。WinRM服务有两个主要组件，用于管理Ansible如何与Windows主机连接：`listener`和`service`配置设置。

可以在下面阅读有关每个组件的详细信息，也可以使用脚本[ConfigureRemotingForAnsible.ps1](https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1)来进行基本设置。此脚本使用自签名证书设置HTTP和HTTPS侦听器，并在服务上启用`Basic` 身份验证选项。

要使用此脚本，请在PowerShell中运行以下命令：

```powershell
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)

powershell.exe -ExecutionPolicy ByPass -File $file
```

> :exclamation:
>
> ConfigureRemotingForAnsible.ps1脚本仅用于培训和开发目的，不应在生产环境中使用，因为它启用了`Basic` 这本质上不安全（如身份验证）。

#### WinRM Listener

WinRM服务侦听一个或多个端口上的请求。每个端口都必须创建并配置一个侦听器。

要查看在WinRM服务上运行的当前侦听器，请运行以下命令：

```powershell
winrm quickconfig
winrm enumerate winrm/config/Listener
```

运行后输出如下:

```powershell
Listener
    Address = *
    Transport = HTTP
    Port = 5985
    Hostname
    Enabled = true
    URLPrefix = wsman
    CertificateThumbprint
    ListeningOn = 10.0.2.15, 127.0.0.1, 192.168.56.155, ::1, fe80::5efe:10.0.2.15%6, fe80::5efe:192.168.56.155%8, fe80::
ffff:ffff:fffe%2, fe80::203d:7d97:c2ed:ec78%3, fe80::e8ea:d765:2c69:7756%7

Listener
    Address = *
    Transport = HTTPS
    Port = 5986
    Hostname = SERVER2016
    Enabled = true
    URLPrefix = wsman
    CertificateThumbprint = E6CDAA82EEAF2ECE8546E05DB7F3E01AA47D76CE
    ListeningOn = 10.0.2.15, 127.0.0.1, 192.168.56.155, ::1, fe80::5efe:10.0.2.15%6, fe80::5efe:192.168.56.155%8, fe80::
ffff:ffff:fffe%2, fe80::203d:7d97:c2ed:ec78%3, fe80::e8ea:d765:2c69:7756%7
```

修改winrm配置，启用远程连接认证

```powershell
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
```

#### windows 防火墙配置

配置防火墙:

1. 添加防火墙信任规则，允许5985-5986端口通过
2. 打开防火墙高级配置，选择**入站规则**，在点击新建规则
3. 填写一下信息
    1. **TCP**
    2. 信任端口**5985-5986**
4. 填写新建规则名称

## Ansible服务器端配置并管理Windows

添加windows客户端连接信息: 编辑`/etc/ansible/hosts`, 添加客户端主机信息(ansible服务端的配置)

```ansible
[windows]

192.168.2.2 ansible_user="Administrator" ansible_password="Password" ansible_port=5986 ansible_connection="winrm" ansible_winrm_server_cert_validation=ignore ansible_winrm_transport=basic
```

### ping 远程windows主机

```bash
$ ansible 192.168.2.2 -m win_ping
192.168.2.2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### 创建目录

```bash
$ ansible 192.168.2.2 -m win_file -a 'path=D:\\test state=directory'
192.168.2.2 | CHANGED => {
    "changed": true
}
```

### 下发文件

```bash
$ ansible 192.168.2.2 -m win_copy -a 'src=/etc/hosts dest=D:\\hosts.txt'
192.168.2.2 | CHANGED => {
    "changed": true,
    "checksum": "f6d471689e1233342a8e43a130ff40a6ea0b9f51",
    "dest": "D:\\hosts.txt",
    "operation": "file_copy",
    "original_basename": "hosts",
    "size": 635,
    "src": "/etc/hosts"
}
```

### 删除文件

```bash
# ansible 192.168.2.2 -m win_file -a 'dest=d:\\config_dir\\hosts.txt state=absent'
```

### 删除目录

```bash
# ansible 192.168.2.2 -m win_file -a 'dest=d:\\config_dir2 state=absent'
```

### 执行cmd命令

```bash
# ansible 192.168.2.2 -m win_shell -a 'ipconfig'
```

### 重启windows

```bash
# ansible 192.168.2.2 -m win_reboot
# ansible 192.168.2.2 -m win_shell -a 'shutdown -r -t 0'
```

### 创建用户

远程在windows客户端上创建用户

```bash
# ansible 192.168.2.2 -m win_user -a "name=testuser1 passwd=123456"
```

### windows服务管理

```bash
# ansible 192.168.2.2 -m win_shell -a “net stop|start zabbix_agent”
```

> :notebook:
>
> 完整的windows module见: [Windows modules](https://docs.ansible.com/ansible/latest/modules/list_of_windows_modules.html)
