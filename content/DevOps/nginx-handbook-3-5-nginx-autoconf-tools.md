Title: NGINX 实战手册-运维-使用Puppet/Chef/Ansible/SaltStack部署
Category: DevOps
Date: 2019-06-19 20:28
Tags: nginx, devops, 译文, 最佳实践, docker
Summary: NGINX 实战手册系列文章的运维部分. 本文主要介绍如何使用Puppet/Chef/Ansible/SaltStack部署.
Image: /images/docker_nginx-750x410.png

## 3.5 使用Puppet/Chef/Ansible/SaltStack

### 3.5.0 介绍

在云的时代, 配置管理工具是无价之宝. 大规模web应用的工程师无法通过代码手把手配置servers, 但是使用其中任何一个配置管理工具都可以做到. 配置管理工具允许工程师一次写入配置和代码到很多有相同配置的server, 通过使用一种可重复, 可测试, 模块化的方式. 本章讨论几个流行的配置管理工具, 以及如何使用他们安装NIGINX和从模版创建一个基本配置. 这些例子非常基础, 但是展示了如何通过每个平台来启动NGINX.

### 3.5.1 使用Puppet安装

#### 问题

你需要通过Puppet安装和配置NGINX, 以代码形式管理NGINX配置, 并确认你的其他Puppet配置.

#### 解决方案

创建一个模块, 用于安装NGINX, 管理你需要的文件, 确保NGINX在运行:

```ruby
class nginx {
    package {"nginx": ensure => 'installed',}
    service {"nginx":
        ensure => 'true',
        hasrestart => 'true',
        restart => '/etc/init.d/nginx reload',
    }
    file { "nginx.conf":
        path    => '/etc/nginx/nginx.conf',
        require => Package['nginx'],
        notify  => Service['nginx'],
        content => template('nginx/templates/nginx.conf.erb'),
        user=>'root',
        group=>'root',
        mode='0644';
    }
}
```

该模块使用包管理工具来确保NGINX被安装. 也会确保NGINX在启动时在运行和可用. 该配置通知Puppet, 该服务有重启命令, 通过`hasrestart`指令, 并且我们用NGINX reload命令覆盖`restart`命令. 它通过内置Ruby(ERB)模版语言来管理和模板化`nginx.conf`文件. 文件的模板化会发生在NGINX包被安装之后(通过`require`指令). 但是, 它会通过`notify`指令通知NGINX服务来reload. 该模版化配置文件没有包括. 另外, 它可以简单安装一个默认的NGINX配置文件, 或是使用内置Ruby(ERB)或内置Puppet(EPP)模版语言的循环和变量替换.

#### 讨论

Puppet是基于Ruby语言的配置管理工具. 模块被构建进一个特定域的语言, 并通过定义给定server配置的manifest文件调用. Puppet可以用主从或masterless模式运行. 使用Puppet, manifest运行在master上, 然后发到slave上. 这很重要, 因为它确保slave只是被交付对它有用的配置, 对其他server的其他配置是不会给这个slave的. Puppet有很多非常高级的公用模块. 通过这些模块, 会在配置上帮助你飞起. 在GitHub上来自voxpupuli的公共NGINX模块会为你模板化NGINX配置.

#### 参见

[Puppet documentation](https://docs.puppet.com/)

[Puppet package documentation](http://bit.ly/2jfgpm4)

[Puppet service documentation](http://bit.ly/2jMq2cx)

[Puppet file documentation](http://bit.ly/2jMz4q3)

[Puppet templating documentation](http://bit.ly/2isqAlP)

[Voxpupuli NGINX module](http://bit.ly/2jMspMn)

### 3.5.2 使用Chef安装

> 略

### 3.5.3 使用Ansible安装

#### 问题

你需要使用Ansible来安装和配置NGINX, 以代码形式管理NGINX配置, 并确认你的其他Ansible配置.

#### 解决方案

创建一个安装NGINX和管理*nginx.conf*文件playbook. 下列是一个示例的任务文件.

```yaml
- name: NGINX | Installing NGINX
  package: name=nginx state=present

- name: NGINX | Starting NGINX
  service:
    name: nginx
    state: started
    enabled: yes
- name: Copy nginx configuration in place.
  template:
    src: nginx.conf.j2
    dest: "/etc/nginx/nginx.conf"
    owner: root
    group: root
    mode: 0644
  notify:
    - reload nginx
```

`package`块安装NGINX. `service`块确保NGINX在启动时被启动和可用. `template`块模板化一个*Jinja2*文件, 并把结果以root用户和组放到`/etc/nginx.conf`中. 该模版块也设置*mode*为644, 并通知nginx服务reload. 模板化配置文件没有包含在内. 但是, 可以通过默认的NGINX配置文件来简单, 或者通过Jinja2模版语言的循环和变量替换生成很复杂的模版.

#### 讨论

Ansible是用Python编写的广泛使用的强大配置管理工具. 任务配置使用YAML, 使用Jinja2模版语言生成文件模版. Ansible提供一个有master的叫做Ansible Tower的订阅版. 但是, 它经常用于本地机器或构建服务器直接到客户端或者使用masterless模式. Ansible打包SSH到它的server并运行配置. 和其他配置工具类似, 有很多社区提供的公共roles, Ansible把它叫做Ansible Galaxy. 你可以找到可以用于你的playbook的非常复杂的roles.

#### 参见

[Ansible documentation](http://docs.ansible.com/)

[Ansible packages](http://bit.ly/2jfiwGv)

[Ansible service](http://bit.ly/2jMGF7E)

[Ansible template](http://bit.ly/2j8j526)

[Ansible Galaxy](https://galaxy.ansible.com/)

### 3.5.4 使用SaltStack安装

#### 问题

你需要使用SaltStack来安装和配置NGINX, 以代码形式管理NGINX配置, 并确认你的其他SaltStack配置.

#### 解决方案

```yaml
nginx:
  pkg:
    - installed
  service:
    - name: nginx
    - running
    - enable: True
    - reload: True
    - watch:
      - file: /etc/nginx/nginx.conf

/etc/nginx/nginx.conf:
  file:
    - managed
    - source: salt://path/to/nginx.conf
    - user: root
    - group: root
    - template: jinja
    - mode: 644
    - require:
      - pkg: nginx
```
