Title: 如何编写Python Web框架（三）
Date: 2019-03-06 11:03
Status: published
Category: Python
Tags: python, web框架
Slug: write-python-framework-part-three
Author: 东风微鸣
Summary: 编写自己的Python Web框架, 实现: 测试客户端; 添加路径的替代方式（如类似Django的实现）; 支持模板
Image: /images/web-frameworks.jpg

# 如何编写Python Web框架（三）

> 本文为译文
>
> 原文链接: [How to write a Python web framework. Part III.](http://rahmonov.me/posts/write-python-framework-part-three/)
>
> 作者: Jahongir Rahmonov
>
> Github仓库: [alcazar](https://github.com/rahmonov/alcazar)

在本系列之前的博客文章中，我们开始编写自己的Python框架并实现以下功能：

- WSGI兼容
- 请求处理程序
- 路由：简单和参数化
- 检查重复的路径
- 基于类的处理程序
- 单元测试

在这部分中，我们将为列表添加一些很棒的功能：

- 测试客户端
- 添加路径的替代方式（如类似Django的实现）
- 支持模板

## 测试客户端

在第[2部分中]({filename}how-to-write-a-python-web-framework-2.md)，我们编写了几个单元测试。但是，当我们需要向处理程序发送HTTP请求时，我们停止了，因为我们没有可以执行此操作的测试客户端。我们先添加一个。

到目前为止，在Python中发送HTTP请求最流行的方式是[Kenneth Reitz](https://twitter.com/kennethreitz)的[`Requests`](https://github.com/kennethreitz/requests)库。但是，为了能够在单元测试中使用它，我们应该始终启动并运行我们的应用程序（即在运行测试之前启动gunicorn）。原因是[`Requests`只附带一个Transport Adaptter: HTTPAdapter](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters)。这违背了单元测试的目的。单元测试应该是自我维持的。对我们来说幸运的是，[Sean Brant](https://github.com/seanbrant)编写了一个[WSGI Transport Adapter，用于](https://github.com/seanbrant/requests-wsgi-adapter)创建测试客户端。让我们先编写代码再进行讨论。

> :exclamation: 译者注:
>
> 先安装2个库:
>
> ```shell
> pip install requests
> pip install requests-wsgi-adapter
> ```
>
> 

将以下方法添加到`api.py`主类`API`中：

```python
# api.py
...
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter


class API:
    ...

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    ...
```

如此[处所述](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters)，要使用Requests WSGI Adapter，我们需要将其mount到Session对象。这样，使用`test_session`,其URL以给定前缀开头的任何请求都将使用给定的RequestsWSGIAdapter。太好了，现在我们可以用`test_session`来创建一个测试客户端。创建一个`conftest.py`文件并将`api` fixture 移动到此文件，使其如下所示：

```python
# conftest.py
import pytest

from api import API


@pytest.fixture
def api():
    return API()
```

此文件的`pytest`默认情况下会查找fixture 。现在，让我们在这里创建测试客户端fixture ：

```python
# conftest.py
...

@pytest.fixture
def client(api):
    return api.test_session()
```

我们的`client`需要`api` fixture 并返回我们之前编写的内容`test_session`。现在我们可以在单元测试中使用这个`client ` fixture 。让我们直接进入`test_bumbo.py`文件并编写一个单元测试，测试是否`client`可以发送请求：

```python
# test_bumbo.py
...

def test_bumbo_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT
```

运行单元测试`pytest test_bumbo.py`并观察。我们看到所有的测试都通过了。让我们为最重要的部分添加几个单元测试：

```python
# test_bumbo.py
...

def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"
```

这个测试我们在url中发送的参数是否正常工作。

```python
# test_bumbo.py
...

def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found."
```

这个测试如果请求被发送到不存在的路由，则返回404（未找到）响应。

剩下的我会留给你。如果您需要任何帮助，请尝试编写更多测试并在评论中告诉我。以下是单元测试的一些想法：

- 测试基于类的处理程序GET请求是否正常运行
- 测试基于类的处理程序POST请求是否正常运行
- 测试如果使用无效的请求方法，基于类的处理程序返回响应`Method Not Allowed.`
- 测试是否正确返回状态码

## 添加路径的替代方式

现在，这是添加路径的方式：

```python
@api.route("/home")
def handler(req, resp):
    resp.text = "YOLO"
```

也就是说，路由被添加为装饰器，就像在Flask中一样。有些人可能喜欢Django注册网址的方式。所以，让我们给他们这样添加路径的选择：

```python
def handler(req, resp):
    resp.text = "YOLO"


def handler2(req, resp):
    resp.text = "YOLO2"

api.add_route("/home", handler)
api.add_route("/about", handler2)

```

`add_route`方法应该做两件事。检查路径是否已经注册，如果没有，则注册：

```python
# api.py

class API:
    ...

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler

```

很简单。这段代码看起来很熟悉吗？这是因为我们已经在`route`装饰器中编写了这样的代码。我们现在可以遵循DRY原则并在`route`装饰器中使用`add_route`方法：

```python
# api.py


class API:
    ...

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler

    def route(self, pattern):
        def wrapper(handler):
            self.add_route(pattern, handler)
            return handler

    return wrapper

```

让我们添加一个单元测试来检查它是否正常工作：

```python
# test_bumbo.py

def test_alternative_route(api, client):
    response_text = "Alternative way to add a route"

    def home(req, resp):
        resp.text = response_text

    api.add_route("/alternative", home)

    assert client.get("http://testserver/alternative").text == response_text

```

运行您的测试，您将看到所有测试都通过。

## 模板支持

当我实现新的东西时，我喜欢做一些叫做README驱动的开发。这是一种技术，您可以在实施之前记下API是什么样子。让我们来实现。假设我们要在我们的处理程序中使用此模板：

```html
<html>
    <header>
        <title>{{ title }}</title>
    </header>

    <body>
        The name of the framework is {{ name }}
    </body>

</html>

```

`{{ title }}`和`{{ name }}`是从处理程序发送的变量，这是处理程序的样子：

```python
api = API(templates_dir="templates")

@api.route("/template")
def handler(req, resp):
    resp.body = api.template("index.html", context={"title": "Awesome Framework", "name": "Alcazar"})

```

我希望它尽可能简单，所以我只需要一个方法，将模板名和上下文作为参数，并用给定的参数呈现该模板。另外，我们希望模板目录可以像上面一样配置。

通过设计API，我们现在可以实现它。

对于模板支持，我认为[Jinja2](http://jinja.pocoo.org/docs/2.10/)是最佳选择。它是一个现代的，设计师友好的Python模板语言，模仿Django的模板。所以，如果你知道Django, 那么使用Jinja2应该感觉一样。

`Jinja2`使用称为模板`Environment`的中心对象。我们将在应用程序初始化和借助此Environment 加载模板的基础上配置此环境。以下是如何创建和配置一个：

```python
from jinja2 import Environment, FileSystemLoader

templates_env = Environment(loader=FileSystemLoader(os.path.abspath("templates")))

```

`FileSystemLoader`从文件系统加载模板。此加载程序可以在文件系统上的文件夹中查找模板，并且是加载它们的首选方法。它将模板目录的路径作为参数。现在我们可以这样使用`templates_env`：

```python
templates_env.get_template("index.html").render({"title": "Awesome Framework", "name": "Alcazar"})

```

既然我们了解了Jinja2中的所有工作原理，那么我们就将其添加到我们自己的框架中。首先，让我们安装jinja2：

```
pip install Jinja2

```

然后，在我们的`API`类的`__init__`方法中创建`Environment` 对象：

```python
# api.py
from jinja2 import Environment, FileSystemLoader
import os


class API:
    def __init__(self, templates_dir="templates"):
        self.routes = {}

        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))

    ...

```

我们做了几乎与上面相同的事情，除了我们为`templates_dir`提供了一个默认值，`templates`以便用户不必写它。现在我们有了实现我们之前设计的`template`方法的所有方法：

```python
# api.py

class API:
    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

```

我认为这里没有必要解释任何事情。你唯一想知道的是为什么我给了`context`一个默认值`None`，检查它是否是`None`，然后将值设置为空字典`{}`。你可能会说我可以在声明中给它默认值`{}`。但是`dict`它是一个可变对象，在Python中将可变对象设置为默认值是一种不好的做法。[在这里](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments)阅读更多相关信息。

随着一切准备就绪，我们可以创建模板和处理程序。首先，创建`templates`文件夹：

```shell
mkdir templates

```

通过执行`touch templates/index.html`创建文件`index.html`并将以下内容放入：

```html
<html>
    <header>
        <title>{{ title }}</title>
    </header>

    <body>
        <h1>The name of the framework is {{ name }}</h1>
    </body>

</html>

```

现在我们可以在我们的`app.py`创建处理程序：

```python
# app.py

@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", context={"name": "Alcazar", "title": "Best Framework"})

```

就是这样（好吧，差不多）。启动`gunicorn`然后访问`http://localhost:8000/template`。你会看到一个大大的`Internal Server Error`。那是因为`resp.body`期望bytes, 而我们的`template`方法返回一个unicode字符串。因此，我们需要对其进行编码：

```python
# app.py

@api.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", context={"name": "Alcazar", "title": "Best Framework"}).encode()

```

重新启动gunicorn，你将看到我们的模板的所有荣耀。在后续的文章中，我们将不再需要`encode`并使我们的API更漂亮。

## 结论

我们在这篇文章中实现了三个新功能：

- 测试客户端
- 添加路径的替代方式（如Django的实现方式）
- 支持模板

请务必在评论中告诉我们应该在本系列中实现的其他功能。对于下一部分，我们肯定会添加对静态文件的支持，但我不确定我们应该添加哪些其他功能。

[*在这里看看第一部分*]({filename}how-to-write-a-python-web-framework-1.md)
[*在这里看看第二部分*]({filename}how-to-write-a-python-web-framework-2.md)

> 稍微提醒一下，这个系列是基于我为学习目的而编写的[Alcazar框架](https://github.com/rahmonov/alcazar)。如果你喜欢这个系列，[请在这儿](https://github.com/rahmonov/alcazar)查看博客中的内容，一定要通过star该repo来表达你的喜爱。

Fight on!
