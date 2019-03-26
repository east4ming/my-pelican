Title: 腾讯云服务器初始化操作
Date: 2019-03-26 21:09
Status: published
Category: DevOps
Tags: 腾讯云, 云, centos, 监控, 告警, 可观察性, 安全, 密钥, git, shell
Slug: initialize-my-tencentyun-server
Author: 东风微鸣
Summary: 腾讯云服务器初始化操作, 包括: 重装系统; 配置监控; 安全加固; 更新软件; 安装git和安装oh-my-zsh
Image: /images/tencentyun.jpg
Related_posts: build-ide-on-tencentyun

[TOC]

## 重装系统

> :notebook: 说明:
>
> 因为我买的时候, CentOS最新只提供到7.3, 我希望使用CentOS 7.5. 看到镜像库里有(什么毛病, 买的时候为啥不提供), 所有重新安装下系统.

1. 选中实例, 点击**更多**, 选择**重装系统**:

   ![重装系统](./images/init_tencentyun_install_os_1.png)

2. 选择**公共镜像** -> **CentOS** -> **CentOS 7.5 64位** -> 输入root密码. 点击**开始重装**. 如下图:

   ![重装系统具体选项](./images/init_tencentyun_install_os_2.png)

3. 等待重装完毕即可.

## 设置监控告警

1. 点击**监控**图标:

   ![点击监控](./images/init_tencentyun_monitor_1.png)

2. 有以下监控指标, 如下图, 点击**设置告警**:

   1. CPU
   2. 内存
   3. 宽带(内外网)
   4. 磁盘IO
   5. 分区使用请看

   ![设置告警](./images/init_tencentyun_monitor_2.png)

3. 根据自己的需要, 定制告警策略. 示例如下:

   ![告警策略](./images/init_tencentyun_monitor_3.png)

4. 要配置告警通知渠道, 需要先**新增用户组**. 如下(我和其他人合用, 所以建立一个用户组还是有必要的):

   ![新增用户组](./images/init_tencentyun_monitor_4.png)

5. 新增用户组的操作如下, 先直接使用预设策略 - 管理员就可以了.

   ![新增用户组](./images/init_tencentyun_groupuser_3.png)

6. 接下来关联到具体的用户组

   ![关联接受组](./images/init_tencentyun_monitor_5.png)

7. 点击**完成**, 配置完成后如下所示: (可以把默认的禁用掉了)

   ![告警策略](./images/init_tencentyun_monitor_6.png)

## 创建密钥并绑定主机

1. 在**SSH密钥** 菜单, 点击**创建密钥**:

   ![创建密钥](./images/init_tencentyun_key_1.png)

2. 创建密钥(:exclamation:  密钥请妥善保存, 勿外传).

   ![创建密钥](./images/init_tencentyun_key_2.png)

3. 创建后, 先关闭主机(关闭后的主机才能绑定密钥, 很好, 关机也受到告警了👌), 再选择**绑定/解绑实例**, 如下图:

   ![绑定实例](./images/init_tencentyun_key_3.png)

## 安全组配置

> :notebook: 备注:
>
> 类似于防火墙权限.

1. 点击**安全组** -> **新建**. 如下图:

   ![新建安全组](./images/init_tencentyun_securegroup_1.png)

2. 选择**立即设置规则**. 具体原因如下图:

   ![设置规则](./images/init_tencentyun_securegroup_2.png)

3. 可以先关联到我自己的云主机实例. 如下图:

   ![关联到实例](./images/init_tencentyun_securegroup_3.png)

4. 然后再配置出/入站规则, 先配置入站, 先选择**一键放通**. 放通以下:

   1. Linux SSH登录: 22端口
   2. Windows登录: 3389
   3. ping: ICMP协议
   4. HTTP: 80
   5. HTTPS: 443
   6. FTP: 20和21

   ![一键放通入站](./images/init_tencentyun_securegroup_4.png)

5. 再根据自己需要添加规则, 如下: (放通TCP的8000端口)

   ![自定义规则](./images/init_tencentyun_securegroup_5.png)

6. 最后配置出站规则, 选择**一键放通**. 以后再慢慢细化, 如下:

   ![一键放通出栈](./images/init_tencentyun_securegroup_6.png)

   

至此, 控制台上该配置的就配置的差不多了, 接下来登录主机进行配置.

## CentOS 7.5 优化配置

### 用户/登录相关优化

#### 创建普通用户 基于公钥登录

1. 创建普通用户: `useradd -m  -p yourpassword casey`

2. 普通用户基于公钥登录: (因为之前**创建密钥并绑定主机**, 公钥已经存在于主机上了, 所以不需要keygen了, 直接复制就可以了)

   ```shell
   cp /root/.ssh/authorized_keys /home/casey/.ssh && chown -R casey:casey /home/casey/.ssh/
   ```

3. 确认基于ssh公钥的登录是否工作

> :notebook: 备注:
>
> 完整的**基于公钥**登录的步骤如下: (前提是刚开始该账户能通过账号密码方式登录)
>
> 1. 在云主机上创建普通用户: `useradd -m -p yourpassword hellowordomain`
> 2. 使用 ssh-keygen命令在云主机上创建密匙对: `ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_tencent_$(date +%Y-%m-%d) -C "tencent key for hellowordomain"`
> 3. 使用 ssh-copy-id 命令安装公匙：` ssh-copy-id -i /path/to/public-key-file user@host`
> 4. 确认基于ssh公钥的登录是否工作

#### 普通用户配置sudo权限

**在 CentOS/RHEL 系统中如何将用户 vivek 添加到 sudo 组中**

在 CentOS/RHEL 和 Fedora 系统中允许 wheel 组中的用户执行所有的命令。使用 usermod 命令将用户 vivek 添加到 wheel 组中：

```shell
$ sudo usermod -aG wheel vivek
$ id vivek
```

**sudo无需输入密码**

```shell
# root用户
visudo

# 修改如下内容后保存退出
## Allows people in group wheel to run all commands
# %wheel        ALL=(ALL)       ALL

## Same thing without a password
%wheel  ALL=(ALL)       NOPASSWD: ALL
```

测试并确保用户 vivek 可以以 root 身份登录执行以下命令：

```shell
sudo -i  # 切换到root用户
sudo systemctl status sshd  # 查看sshd的状态
```

#### `sshd_config` 优化

```
# 禁用root登录
PermitRootLogin no
ChallengeResponseAuthentication no
PasswordAuthentication no
UsePAM no
# 禁用密码登录 仅留下公匙登录
AuthenticationMethods publickey
PubkeyAuthentication yes
# 禁用空密码
PermitEmptyPasswords no
```

最后测试 `sshd_config` 文件并重启/重新加载 SSH 服务

```shell
sudo sshd -t
sudo systemctl restart sshd.service
```

### 更新系统和软件

```shell
sudo yum upgrade -y  # 升级所有软件
sudo yum clean all -y  # 清理缓存
```

### 安装及配置 Git

1. 安装Git

   ```shell
   sudo yum install -y --setopt=tsflags=nodocs git
   ```

2. 配置git

   ```shell
   git config --global user.name "east4ming"
   git config --global user.email "cuikaidong@foxmail.com"
   ssh-keygen -t rsa -b 4096 -C "cuikaidong@foxmail.com"  # 已有私钥也可以重复使用
   
   ```

3. `cat .ssh/id_rsa.pub` 并复制 (id_rsa.pub是对应的公钥信息)

4. 打开github网页登入账户进入账户settings左边找到SSH，可以清理一下没用的SSH keys，然后新建一个 ，取名任意，粘贴进去cat产生的所有字符。保存即可。

5. 缓存HTTPS方式的密码: 

   ```shell
   $ git config --global credential.helper 'cache --timeout=3600'
   # Set the cache to timeout after 1 hour (setting is in seconds)
   
   ```

   

### 优化配置shell

#### 安装zsh

```shell
sudo yum install -y --setopt=tsflags=nodocs zsh
zsh --version
sudo chsh -s $(which zsh)
# 注销

```

安装powerline

```shell
pip install powerline-status --user

```

#### 安装[**oh-my-zsh**](https://github.com/robbyrussell/oh-my-zsh)

```shell
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

```

## Using Oh My Zsh

> 以下内容来自 oh-my-zsh github

### Plugins

Oh My Zsh comes with a shitload of plugins to take advantage of. You can take a look in the [plugins](https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins) directory and/or the [wiki](https://github.com/robbyrussell/oh-my-zsh/wiki/Plugins)to see what's currently available.

#### Enabling Plugins

Once you spot a plugin (or several) that you'd like to use with Oh My Zsh, you'll need to enable them in the `.zshrc` file. You'll find the zshrc file in your `$HOME` directory. Open it with your favorite text editor and you'll see a spot to list all the plugins you want to load.

```
vi ~/.zshrc

```

For example, this might begin to look like this:

```
plugins=(
git
bundler
dotenv
osx
rake
rbenv
ruby
)

```

#### Using Plugins

Most plugins (should! we're working on this) include a **README**, which documents how to use them.

### Themes

We'll admit it. Early in the Oh My Zsh world, we may have gotten a bit too theme happy. We have over one hundred themes now bundled. Most of them have [screenshots](https://wiki.github.com/robbyrussell/oh-my-zsh/themes) on the wiki. Check them out!

#### Selecting a Theme

*Robby's theme is the default one. It's not the fanciest one. It's not the simplest one. It's just the right one (for him).*

Once you find a theme that you'd like to use, you will need to edit the `~/.zshrc` file. You'll see an environment variable (all caps) in there that looks like:

```shell
ZSH_THEME="robbyrussell"

```

To use a different theme, simply change the value to match the name of your desired theme. For example:

```shell
ZSH_THEME="agnoster" # (this is one of the fancy ones)
# see https://github.com/robbyrussell/oh-my-zsh/wiki/Themes#agnoster
 
```

*Note: many themes require installing the Powerline Fonts in order to render properly.*

Open up a new terminal window and your prompt should look something like this:

![Agnoster theme](https://cloud.githubusercontent.com/assets/2618447/6316862/70f58fb6-ba03-11e4-82c9-c083bf9a6574.png)

In case you did not find a suitable theme for your needs, please have a look at the wiki for [more of them](https://github.com/robbyrussell/oh-my-zsh/wiki/External-themes).

If you're feeling feisty, you can let the computer select one randomly for you each time you open a new terminal window.

```
ZSH_THEME="random" # (...please let it be pie... please be some pie..)

```

And if you want to pick random theme from a list of your favorite themes:

```
ZSH_THEME_RANDOM_CANDIDATES=(
"robbyrussell"
"agnoster"
)

```

