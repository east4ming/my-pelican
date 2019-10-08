Title: Ansible 新手指南 - 如何批量管理 NGINX
Status: published
Tags: python, devops, ansible, linux
Date: 2019-10-08 18:30
Author: 东风微鸣
Slug: how-to-manager-nginx-using-ansible
Summary: Ansible 新手向教程. 如何配置免密, 安装ansible, 初步使用; 以及使用ansible 批量安装, 启动, 卸载, 更新NGINX.
Image: /images/ansible_logo_black-1024x138.png

[TOC]

## 概述

Ansible是自动化运维工具，基于Python开发，实现了批量系统配置、批量程序部署、批量运行命令等功能。Ansible是基于模块(module)和剧本(playbook)工作。

![Ansible Logo](images/ansible_logo_black-1024x138.png)

接下来通过以下几个方面来演示 Ansible 的基本使用:

1. Linux 配置 SSH 免密
2. 安装 Ansible
3. 使用 Ansible 模块
4. 使用 Ansible Playbook
    1. 安装并启动 NGINX
    2. 停止并卸载 NGINX
    3. 配置NGINX 并重启

实验环境如下:

1. 管理端: (安装 Ansible)
    1. 系统: Debian
    2. IP: 192.168.1.1
2. 远程主机1和2:
    1. 系统: Ubuntu
    2. IP: 192.168.1.106和192.168.1.107


> :notebook: 备注:
>
> 为了方便演示, 以下命令都是基于`root`用户

## 免密配置

即: 基于公钥的登陆


```shell
# 1. 创建密钥对(创建后默认位于 ~/.ssh)
ssh-keygen -t ed25519 -C "Login to nginx lab"
# 2. 使用 ssh-copy-id 命令安装公钥
ssh-copy-id -i /root/.ssh/id_ed25519 root@192.168.1.106
ssh-copy-id -i /root/.ssh/id_ed25519 root@192.168.1.107
# 3. 验证免密是否配置成功: (无需输入密码)
ssh root@192.168.1.106 -i /root/.ssh/id_ed25519
ssh root@192.168.1.107 -i /root/.ssh/id_ed25519
```



> :notebook: 备注:
>
> 免密配置有多种情况会导致失败, 本文不一一列举详细失败原因. 如果失败查看远程主机的`/var/log/secure` 日志.

## 安装 Ansible

APT安装方式如下: (其他类似, 不一一列举)

```shell
apt install -y ansible
# 验证
ansible --version
# 输出如下:
#ansible 2.2.1.0
#  config file = /etc/ansible/ansible.cfg
#  configured module search path = Default w/o overrides
```

## 使用 Ansible 模块

> :notebook: 引用:
>
> Ansible附带了许多模块（module 称为“module library”），这些模块可以直接在远程主机上或通过playbooks执行。
>
> 用户也可以编写自己的模块。这些模块可以控制系统资源，比如服务、包或文件（实际上是任何东西），或者处理执行系统命令。

先对`/etc/ansible/hosts`做最基本配置:

```ini
[web]
192.168.1.106
192.168.1.107
```

上文的web就是一个host group, 可以直接通过`web`进行引用. 

### ansible-doc

所有的模块的使用方法可以通过以下命令查询:

```shell
ansible-doc -s <module_name>
ansible-doc -s ping
# - name: Try to connect to host, verify a usable python and return `pong' on success.
#  action: ping
ansible-doc -s command
#- name: Executes a command on a remote node
#  action: command
#      chdir                  # cd into this directory before running the command
#      creates                # a filename or (since 2.0) glob pattern, when it already #exists, this step will *not* be run.
#      executable             # change the shell used to execute the command. Should be #an absolute path to the executable.
#      free_form=             # the command module takes a free form command to run.  #There is no parameter actually named 'free form'. See the examples!
#      removes                # a filename or (since 2.0) glob pattern, when it does not #exist, this step will *not* be run.
#      warn                   # if command warnings are on in ansible.cfg, do not warn #about this particular line if set to no/false.
```

### 使用 Ansible 模块示例

下面以 *command*和*ping* module为例:

```shell
ansible web -a "pwd chdir=/tmp"
ansible web -m ping
```

输出如下:

```
# ansible web -a "pwd chdir=/tmp"
192.168.1.106 | SUCCESS | rc=0 >>
/tmp

192.168.1.107 | SUCCESS | rc=0 >>
/tmp

# ansible web -m ping
192.168.1.106 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
192.168.1.107 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

**简单说明:**

- `web`: 在`/etc/ansible/hosts`中配置的 web 主机组. 包含本次实验的: 远程主机1和2
- `-a "pwd chdir=/tmp"`: ` -a MODULE_ARGS` 模块的参数. 
    - 参数格式为: `key=value`.  如本例中的: `chdir=/tmp`
    - `pwd` 为shell命令.
- `-m ping`: ansible命令参数 - 模块, 后跟模块名. (默认为 `command`). `"pong"` 表示ping成功, 返回不是`"pong"`则连接异常.

## 使用 Ansible Playbook

**Playbook**(剧本)是使用ansible的一种完全不同的形式，非常强大。

简单地说，playbook是一个非常简单的配置管理和多机部署系统的基础，不像任何已经存在的系统，它非常适合部署复杂的应用程序。

在[ansible-examples](https://github.com/ansible/ansible-examples) git仓库中, 有一些完整的playbook具体展示了这些技术。建议可以看看。

### 安装并启动NGINX

创建安装并启动NGINX的 Ansible Playbook YAML文件: `vi nginx_install.yml`

```yaml
---
- hosts: web
  become: true
  tasks:
    - name: install nginx
      apt: name=nginx state=latest
    - name: start nginx
      service:
          name: nginx
          state: started
```

**简单说明:**

- `- hosts: web`: 该playbook首先说明应将其应用于inventory 资源中的`web`主机。
- `become: true`: 告诉Ansible提升权限（如sudo）来执行此playbook中的所有任务。
- `tasks`: 定义实际**tasks**(任务)的部分。第一个任务安装nginx，第二个任务是启动nginx.

执行:

```shell
ansible-playbook nginx_install.yml
```

输出:

```
PLAY [all] *******************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************
ok: [192.168.1.106]
ok: [192.168.1.107]

TASK [ensure nginx is at the latest version] *********************************************************************
changed: [192.168.1.106]
changed: [192.168.1.107]

PLAY RECAP *******************************************************************************************************
192.168.1.106              : ok=2    changed=1    unreachable=0    failed=0
192.168.1.107              : ok=2    changed=1    unreachable=0    failed=0
```

这时NGINX已经安装并启动完毕.

> :notebook: 备注:
>
> 下面几个小章节的`ansible-playbook` 执行结果类似, 就不一一贴出来了.

### 停止并卸载NGINX

创建停止并卸载NGINX的 Ansible Playbook YAML文件: `vi nginx_uninstall.yml`

```yaml
---
- hosts: web
  tasks:
    - name: stop nginx
      service:
          name: nginx
          state: stopped
    - name: uninstall nginx
      apt: name=nginx state=absent
```

再次执行并查看结果.

### 配置NGINX 并重启

**步骤如下:**

1. 创建一个nginx conf的模板文件: `vi static_site.conf.tpl`

```nginx
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        root /usr/share/nginx/html;
        server_name _;
        location / {
    		        index.html index.htm;
        }
}
```

2. 把以上文件放到`/etc/nginx/sites-available/`
3. 在`/etc/nginx/sites-enabled/`里创建个软链接指向该文件.
4. 创建一个`index.html`页面: 

```html
<html>
  <head>
    <title>Hello ansible</title>
  </head>
  <body>
  <h1>Hello World Ansible</h1>

  <p>Running on {{ inventory_hostname }}</p>
  </body>
</html>
```

5. 重启NGINX.



**完整Ansible Playbook**

整合之前的安装, 完整的Ansible Playbook 如下: `vi nginx.yml`

```yaml
---
- hosts: web
  vars:
    src_root: /tmp
  tasks:
    - name: install nginx
      apt: name=nginx state=latest
    - name: start nginx
      service:
          name: nginx
          state: started
      become: yes
    - name: copy nginx conf
      copy:
        src: {{ src_root }}/static_site.conf.tpl
        dest: /etc/nginx/sites-available/static_site.conf
      become: yes
    - name: create symlink
      file:
        src: /etc/nginx/sites-available/static_site.conf
        dest: /etc/nginx/sites-enabled/000-default.conf
        state: link
      become: yes
    - name: copy the html
      copy:
        src: {{ src_root }}/index.html
        dest: /usr/share/nginx/html/index.html
      notify: restart nginx
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
      become: yes
```

再次执行并查看结果. 分别访问: <http://192.168.1.106/> 和 <<http://192.168.1.107/> 查看NGINX运行状态.



**简单说明:**

`index.html`页面, 可以通过`{{ vars }}` 来使用一些变量. 可以使用ansible已有的, 也可以使用后续自定义的. 本例中使用的`inventory_hostname` 为ansible自带的变量.



Ansible Playbook  - `nginx.yml`:

- `vars`: 定义变量，`src_root`以后在任务中使用。
- `tasks`: 分别为:
    - 安装
    - 启动
    - 复制NGINX配置文件
    - 创建软链接
    - 复制html文件
- `nofity`和`handlers`: 用`notify`触发一个在Ansible中称为**处理程序** - `handler`的事件，该事件将在下面用于重启nginx。`notify`引发事件后，将触发相应的处理程序（`restart nginx`）。

## 总结

本文通过批量管理NGINX这样一个实际案例, 介绍了Ansible的基本用法. 你可以在工作中使用类似的语法来创建属于你自己的剧本(playbook). :laughing::laughing::laughing:


