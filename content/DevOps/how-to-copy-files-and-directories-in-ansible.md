Title: 如何在Ansible中复制多个文件和目录
Status: published
Tags: python, devops, ansible, linux, 译文
Date: 2019-10-12 15:00
Author: 东风微鸣
Slug: how-to-copy-files-and-directories-in-ansible
Summary: Ansible copy和fetch模块使用教程. 如何通过这两个模块实现多种文件和目录的复制.
Image: /images/ansible_logo_black-1024x138.png

[TOC]

![Ansible Logo](images/ansible_logo_black-1024x138.png)

> :notebook: 备注:
>
> 本文大部分内容为译文.
>
> 原文地址: <http://www.mydailytutorials.com/how-to-copy-files-and-directories-in-ansible-using-copy-and-fetch-modules/>
>
> Thanks♪(･ω･)ﾉ

Ansible 通过 *copy* 和 *fetch* 模块提供了基本的复制文件和目录的功能.

您可以使用[*copy* 模块](http://docs.ansible.com/ansible/copy_module.html)将文件和文件夹从本地服务器复制到远程服务器，在远程服务器之间（仅文件）复制，更改文件的权限等。

如果您需要在替换变量后复制文件，例如具有IP更改的配置文件，请改用[*template* 模块](http://docs.ansible.com/ansible/template_module.html)。

## 将文件从本地计算机复制到远程服务器

默认情况下，*copy* 模块将检查本地计算机上 `src` 参数中设置的文件。然后它将文件复制到目标路径中指定的远程计算机 `dest` (目标)路径。下面的示例将当前用户（在本地计算机上）的主目录中的sample.txt文件复制到远程服务器上的`/tmp`目录中。由于我们没有为文件指定任何权限，因此远程文件的默认权限设置为`-rw-rw-r–(0664)`

```yaml
- hosts: blocks
  tasks:
  - name: Ansible copy file to remote server
    copy:
      src: ~/sample.txt
      dest: /tmp 
```

> :notebook: 备注1:
>
> 如果该文件已存在于远程服务器上，并且和源文件的内容不同，则在运行任务时，将修改目标文件。您可以通过设置 `force` 参数来控制它。默认设置为`yes`。因此，它默认情况下会修改文件。如果您不希望在源文件不同的情况下修改文件，则可以将其设置为`no`。仅当远程服务器上不存在该文件时，以下任务才会复制该文件。示例如下:

```yaml
- hosts: blocks
  tasks:
  - name: Ansible copy file force
    copy:
      src: ~/sample.txt
      dest: /tmp 
      force: no
```

> :notebook: 备注2:
>
> 如果在本地计算机上找不到该文件，则Ansible将引发类似于以下的错误。
>
> `fatal: [remote-machine-1]: FAILED! => {“changed”: false, “failed”: true, “msg”: “Unable to find ‘~/sample.txt’ in expected paths.”}`

## 将目录从本地计算机复制到远程服务器

您也可以使用Ansible *copy* 模块复制文件夹/目录。如果`src`路径是目录，则将以递归方式复制它。这意味着将复制整个目录。

现在，有两个不同的变体。取决于是否在`src`路径的末尾使用 `/`字符。

第一种方法将**在远程服务器上创建一个目录**，其名称在`src`参数中设置。然后它将复制源文件夹的内容并将其粘贴到该目录。 **如果你想要这个行为，那么不要在src参数路径后加`/`。**

下面的Ansible复制目录示例将首先在远程服务器的`/tmp`中创建一个名为`copy_dir_ex`的目录。查看`tmp`文件夹中会有一个`copy_dir_ex`文件夹。

```
- hosts: blocks
  tasks:
  - name: Ansible copy directory to the remote server
    copy:
      src:/Users/mdtutorials2/Documents/Ansible/copy_dir_ex
      dest:/Users/mdtutorials2/Documents/Ansible/tmp

output
------
Ansible-Pro:Ansible mdtutorials2$ tree tmp
tmp
└── copy_dir_ex
    ├── file1
    ├── file2
    ├── file3
    └── tmp2
        ├── file4
        └── file5
```

第二种方法将仅将文件从源目录复制到远程服务器。它**不会**在远程服务器上**创建目录**。如果您想要这种行为，则**在src参数中的路径之后输入`/`。**

在下面的示例中，`copy_dir_ex`内部的文件将被复制到远程服务器的`/tmp`文件夹中。如您所见，`src`目录未在目标中创建。仅复制目录的内容。

```
- hosts: blocks
  tasks:
  - name: Ansible copy files from a directory to remote server
    copy:
      src:/Users/mdtutorials2/Documents/Ansible/copy_dir_ex/
      dest:/Users/mdtutorials2/Documents/Ansible/tmp

output
------
tmp/
├── file1
├── file2
├── file3
└── tmp2
    ├── file4
    └── file5
```

> :notebook: 备注:
>
> 1. 如果需要设置远程目录的权限，可以使用  `directory_mode`参数来进行设置。仅当远程计算机上不存在目录时，才设置权限。
>
> 2. 您还可以设置目录的组和所有者。您应该将各自的名称赋值给`group`和`owner`的参数。

## 在同一台远程计算机上的不同文件夹之间复制文件

您还可以在远程服务器上的各个位置之间复制文件。您必须将`remote_src`参数设置为`yes`。

以下示例将复制远程服务器的`/tmp`目录中的 *hello6* 文件，并将其粘贴到`/etc/`目录中。

```yaml
- hosts: blocks
  tasks:
  - name: Ansible copy files remote to remote
    copy:
      src: /tmp/hello6
      dest: /etc
      remote_src: yes
```

> :notebook: 备注:
>
> 从Ansible 2.2.1.0开始，不支持在远程服务器中复制目录。如果尝试，将出现以下错误:
>
> `fatal: [remote-machine-1]: FAILED! => {"changed": false, "failed": true, "msg": "Remote copy does not support recursive copy of directory: /tmp/copy_dir_ex"}`

## 使用with_items复制多个文件/目录

如果要复制多个文件，则可以使用`with_items`遍历它们。

以下示例将复制 home 目录列表给出的多个文件。

```yaml
- hosts: blocks
  tasks:
  - name: Ansible copy multiple files with_items
    copy:
      src: ~/{{item}}
      dest: /tmp
      mode: 0774
    with_items:
      ['hello1','hello2','hello3','sub_folder/hello4']
```

## 复制具有不同权限/目的地设置的多个文件

在上述任务中，我们正在复制多个文件，但是所有文件都具有相同的权限和相同的目的地。但是有时我们想为不同的文件设置权限，或者每个文件的目标文件夹都不同。这可以通过与字典结构一起使用`with_items`来实现。

在以下任务中，我试图将3个文件复制到2个不同的文件夹中。此外，每个文件的文件权限也不同。我提供了一个字典结构，其中提到了每个文件的不同设置。

从输出中可以看到，文件已复制到给定的文件夹，并且权限设置正确。

```yaml
- hosts: all
  tasks:
  - name: Copy multiple files in Ansible with different permissions
    copy:
      src: "{{ item.src }}"
      dest: "{{ item.dest }}"
      mode: "{{ item.mode }}"
    with_items:
      - { src: '/home/mdtutorials2/test1',dest: '/tmp/devops_system1', mode: '0777'}
      - { src: '/home/mdtutorials2/test2',dest: '/tmp/devops_system2', mode: '0707'}
      - { src: '/home/mdtutorials2/test3',dest: '/tmp2/devops_system3', mode: '0575'}
```

```
output
======
mdtutorials2@system01:~$ ls -lrt /tmp
drwxrwxrwx 2 root          root          4096 Oct  9 14:28 devops_system1
drwx---rwx 2 root          root          4096 Oct  9 14:28 devops_system2

mdtutorials2@system01:~$ ls -lrt /tmp2
-r-xrwxr-x 1 root root 0 Oct  9 14:33 devops_system3
```

## 复制与pattern（通配符）匹配的文件夹中的所有文件

如果需要复制目录中与通配符匹配的所有文件，则可以使用`with_fileglob`。

在以下示例中，将本地计算机/ tmp目录中所有以'hello'开头的文件复制到远程服务器。

```yaml
- hosts: blocks
  tasks:
  - name: Ansible copy multiple files with wildcard matching.
    copy:
      src: "{{ item }}"
      dest: /etc
    with_fileglob:
      - /tmp/hello*
```

## 复制之前在远程服务器中创建文件备份

复制文件时，可能会发生错误。您可能会复制错误的文件，写入错误的内容等。这将造成很多麻烦。因此，如果在远程服务器上创建远程文件的备份将很有帮助。

Ansible复制模块为此提供了一个`backup`参数。如果远程文件存在且与复制的文件不同，则将创建一个新文件。新文件将通过附加时间戳和原始文件名来命名。备份参数的默认值为`no`。

例如，以下示例将在远程服务器的`/tmp`目录中创建`helloworld.txt`的备份。它将被命名为`helloworld.txt.8925.2019-10-12@14:53:13`。

```yaml
- hosts: blocks
  tasks:
  - name: ansible copy file backup example
    copy:
      src: ~/helloworld.txt
      dest: /tmp
      backup: yes
```

## 使用临时(Ad-hoc)方法复制文件

以上大多数任务也可以以 Ad-hoc 方式完成。

```shell
ansible blocks -m copy -a "src=~/sample.txt dest=/tmp" -i inventory.ini
ansible blocks -m copy -a "src=~/copy_dir_ex dest=/tmp" -i inventory.ini
ansible blocks -m copy -a "src=/tmp/hello6 dest=/tmp/hello7 remote_src=yes" -s -i inventory.ini
```

## 将文件从远程计算机复制到本地计算机

您还可以将文件从远程服务器复制到本地计算机。这可以使用Ansible *fetch*模块完成。当您要将某些日志文件从远程服务器复制到本地计算机时，这很有用。

默认情况下，将在目标目录（本地计算机）中创建一个以您正在连接的每个主机命名的目录。提取的文件将被复制到此处。如果远程服务器上不存在该文件，则默认情况下不会引发任何错误。

在以下示例中，我在 remote-server-1 上运行任务。该文件将被复制到 本地计算机的`/etc/remote-server-1/tmp`目录中。

```yaml
- hosts: blocks
  tasks:
  - name: Ansible fetch files from remote server to the local machine using Ansible fetch module
    fetch:
      src: /tmp/hello2
      dest: /etc
      mode: 0774
```

如果您不希望出现这种情况，并且需要将文件直接复制到目标目录，则应使用`flat`参数。

```yaml
- hosts: blocks
  tasks:
  - name: Ansible fetch directory example with flat parameter set
    fetch:
      src: /tmp/hello2
      dest: /tmp/
      mode: 0774
      flat: yes
```

> :notebook: 备注:
>
> 1. 如果您使用`flat`参数，并且文件名不是唯一的，则每次获取文件时都会替换现有文件。
> 2. 如果您希望在源文件丢失的情况下引发错误，则将`fail_on_missing`参数设置为`yes`。如果远程文件不存在，以下示例将引发错误。

```yaml
- hosts: blocks
  tasks:
  - name: Ansible fetch example with fail_on_missing set
    fetch:
      src: /tmp/fetch.txt
      dest: /tmp/
      mode: 0774
      fail_on_missing: yes
```

> :notebook: 备注:
>
> 如果尝试将目标路径`dest`设置为目录，请在路径末尾添加“`\`。否则Ansible将运行该任务，就像目标路径`dest`是一个文件一样, 并尝试替换它。您可能会收到以下错误: (**只针对加参数`flat`的情况**)
>
> `fatal: [remote-machine-1]: FAILED! => {“failed”: true, “msg”: “dest is an existing directory, use a trailing slash if you want to fetch src into that directory”}`

## 使用 copy 模块写入文件

您还可以使用Ansible *copy* 模块中的`contents`参数写入文件。以下示例将给`content`参数提供的值写入check4.txt文件。

```yaml
- hosts: all
  tasks:
  - name: Ansible write to a file example
  - copy:
      content: |
        Content parameter example.
        Check4.txt will be created after this task is executed.
      dest: /Users/mdtutorials2/Documents/Ansible/check4.txt
      backup: yes
```

## copy 模块的返回值

*copy* 模块为每个任务返回一些值。完整列表可在[Ansible文档中找到](http://docs.ansible.com/ansible/copy_module.html#return-values)。

例：

```yaml
    "changed": true, 
    "checksum": "98d8fb24e8b2c2cec9c5ae963bd65c3657f50b16", 
    "dest": "/tmp/sample.txt", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "ce83d23d6eb6bf079e1fc5c448ea9a9f", 
    "mode": "0644", 
    "owner": "root", 
    "size": 13, 
    "src": "/home/mdtutorials2/.ansible/tmp/ansible-tmp-1489974916.02-178756727263160/source", 
    "state": "file", 
    "uid": 0
```

## 将查找到的文件复制

使用 *find* 模块递归查找`/appl/scripts/inq`下的所有符合`patterns="inq.Linux*"`的文件, 并将这些文件赋值到`/usr/local/bin` 目录.

```yaml
- hosts: lnx
  tasks:
    - find: paths="/appl/scripts/inq" recurse=yes patterns="inq.Linux*"
      register: file_to_copy
    - copy: src={{ item.path }} dest=/usr/local/sbin/
      owner: root
      mode: 0775
      with_items: "{{ files_to_copy.files }}"
```

*find* 模块的返回值如下:

| Key                       | Returned | 描述                                                         |
| ------------------------- | -------- | ------------------------------------------------------------ |
| **examined** 类型:integer | success  | 查找的文件系统对象数. **示例**: 34                           |
| **files** 类型: list      | success  | 找到符合指定条件的所有匹配项 **示例:**`[{'path': '/var/tmp/test1', 'mode': '0644', '...': '...', 'checksum': '16fac7be61a6e4591a33ef4b729c5c3302307523'}, {'path': '/var/tmp/test2', '...': '...'}]` |
| **matched** 类型: integer | success  | 匹配数量 **示例:**14                                         |

具体解释:

- `register: file_to_copy` 所有返回值注册为`file_to_copy` 对象
- `files_to_copy.files` 即找到的符合指定条件的所有匹配项 **示例:**`[{'path': '/var/tmp/test1', 'mode': '0644', '...': '...', 'checksum': '16fac7be61a6e4591a33ef4b729c5c3302307523'}, {'path': '/var/tmp/test2', '...': '...'}]`
- `item.path`: 具体的符合的文件路径, 即: `/var/tmp/test1` `/var/tmp/test2`...
