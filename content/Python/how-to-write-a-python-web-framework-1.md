Title: 如何编写Python Web框架（一）
Date: 2019-03-01 14:44
Status: published
Category: Python
Tags: python, web框架
Slug: write-python-framework-part-one
Author: 东风微鸣
Summary: 编写自己的Python Web框架, 实现: WSGI兼容; 请求处理程序; 路由：简单和参数化
Image: /images/web-frameworks.jpg

# 如何编写Python Web框架（一）

> 译文:
>
> 原文链接: [How to write a Python web framework. Part I.](http://rahmonov.me/posts/write-python-framework-part-one/)
>
> 作者: Jahongir Rahmonov

“不要重新发明轮子”是我们每天听到的最常见的咒语之一。但是如果我想了解更多有关车轮的信息怎么办？如果我想学习如何制作这个该死的车轮怎么办？我认为为了学习而重新发明它是一个好主意。因此，在这些系列中，我们将编写自己的Python Web框架，以了解在Flask，Django和其他框架中如何完成所有这些魔术。

在本系列的第一部分中，我们将构建框架中最重要的部分。最后，我们将有请求处理程序(request handlers)（类似Django 视图 views）和路由(routing)：既有简单（如`/books/`）请求也有参数化（如`/greet/{name}`）请求。

在我开始做新事物之前，我想考虑最终结果。在这种情况下，在一天结束时，我们希望能够在生产中使用此框架，因此我们希望我们的框架由快速，轻量级的生产级应用程序服务器提供服务。在过去的几年里，我一直在我的所有项目中使用[gunicorn](https://gunicorn.org/)，我对结果非常满意。那么，让我们一起来用`gunicorn`吧。

`Gunicorn`是一个[WSGI](http://rahmonov.me/posts/what-the-hell-is-wsgi-anyway-and-what-do-you-eat-it-with/) HTTP服务器，因此它需要应用程序的特定入口点。如果你不知道什么`WSGI`是什么, [可以阅读这篇文章](http://rahmonov.me/posts/what-the-hell-is-wsgi-anyway-and-what-do-you-eat-it-with/)，我会等待。否则，你无法理解这篇博文的大部分内容。

您是否了解了WSGI是什么？如果了解了。那我们就继续吧。

要与WSGI兼容，我们需要一个可调用的对象（函数或类），它需要两个参数（`environ`和`start_response`）并返回一个WSGI兼容的响应。那么，让我们开始写代码。

> :notebook: 译者注:
>
> 编程环境: Linux或MacOS (windows系统不适用该教程)

想一个框架的名称并创建具有该名称的文件夹。我把它命名为`bumbo`：

```shell
mkdir bumbo
```

进入此文件夹，创建一个虚拟环境并激活它：

```shell
cd bumbo
python3.6 -m venv venv
source venv/bin/activate
```

现在，创建一个名为`app.py` 的文件，我们将在这个文件里存储我们的`gunicorn`入口点：

```shell
touch app.py
```

在这个`app.py`内部，让我们编写一个简单的函数来查看它是否可以和`gunicorn`一起工作：

```python
# app.py

def app(environ, start_response):
    response_body = b"Hello, World!"
    status = "200 OK"
    start_response(status, headers=[])
    return iter([response_body])
```

如上所述，这个可调用的入口点接收两个参数。其中之一`environ`是存储有关请求的各种信息，例如请求方法，URL，查询参数等。第二个`start_response`顾名思义是开始响应的。现在，让我们尝试用`gunicorn`运行此代码。对于`gunicorn`安装和运行如下：

```
pip install gunicorn
gunicorn app:app
```

第一个`app`是我们创建的文件，第二个`app`是我们刚刚编写的函数的名称。如果一切都很好，您将在输出中看到如下内容：

```
[2019-02-09 17:58:56 +0500] [30962] [INFO] Starting gunicorn 19.9.0
[2019-02-09 17:58:56 +0500] [30962] [INFO] Listening at: http://127.0.0.1:8000 (30962)
[2019-02-09 17:58:56 +0500] [30962] [INFO] Using worker: sync
[2019-02-09 17:58:56 +0500] [30966] [INFO] Booting worker with pid: 30966
```

如果您看到此内容，请打开浏览器并转到`http://localhost:8000`。你应该看到我们的老朋友：`Hello, World!`信息。真棒！

现在，让我们将这个函数变成一个类，因为我们需要很多辅助方法，并且它们更容易在类中编写。创建一个`api.py`文件：

```shell
touch api.py
```

在此文件中，创建以下`API`类。我会解释一下它的作用：

```python
# api.py

class API:
    def __call__(self, environ, start_response):
        response_body = b"Hello, World!"
        status = "200 OK"
        start_response(status, headers=[])
        return iter([response_body])
```

现在，删除`app.py`里面的所有内容并编写以下内容：

```python
# app.py
from api import API

app = API()

```

重新启动`gunicorn`并在浏览器中检查结果。它应该和以前一样，因为我们只是简单地将我们的`app`函数改为一个被调用的类`API`并在调用此类实例时覆盖它的`__call__`方法：

```
app = API()
app()   #  this is where __call__ is called

```

现在我们创建了我们的类，我希望使代码更加优雅，因为所有这些字节（`b"Hello World"`）和`start_response`似乎让我感到困惑。值得庆幸的是，有一个名为[WebOb](https://docs.pylonsproject.org/projects/webob/en/stable/index.html)的酷包，它通过包装`WSGI`请求环境和响应状态，标题和正文来为HTTP请求和响应提供对象。通过使用这个包，我们可以通过此包中提供的类传递`environ`和`start_response`，而不必自己处理。在我们继续之前，我建议你看一下[WebOb](https://docs.pylonsproject.org/projects/webob/en/stable/index.html)的[文档](https://docs.pylonsproject.org/projects/webob/en/stable/index.html)来理解我在说什么以及`WebOb`更多的API 。

以下是我们将如何重构此代码。首先，安装`WebOb`：

```
pip install webob

```

在`api.py`文件开头导入`Request`和`Response`类：

```python
# api.py
from webob import Request, Response

...

```

现在我们可以在`__call__`方法中使用它们：

```python
# api.py
from webob import Request, Response

class API:
    def __call__(self, environ, start_response):
        request = Request(environ)

        response = Response()
        response.text = "Hello, World!"

        return response(environ, start_response)

```

看起来好多了！重新启动`gunicorn`，您应该看到与以前相同的结果。最好的部分是我不必解释这里正在做什么。这一切都是不言自明的。我们正在创建一个请求，一个响应，然后返回该响应。真棒！我必须注意到`request`这里还没有使用，因为我们没有对它做任何事情。所以，让我们利用这个机会来使用请求对象。另外，让我们将`response`创建重构为它自己的方法。我们稍后会看到为什么这么做会更好：

```python
# api.py
from webob import Request, Response

class API:
    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        user_agent = request.environ.get("HTTP_USER_AGENT", "No User Agent Found")

        response = Response()
        response.text = f"Hello, my friend with this user agent: {user_agent}"

        return response

```

重启你的`gunicorn`，你应该在浏览器中看到这条新消息。你看见了吗？酷。我们继续。

此时，我们以相同的方式处理所有请求。无论我们收到什么请求，我们只返回在`handle_request`方法中创建的相同响应。最终，我们希望它是动态的。也就是说，我们希望提供的来自`/home/`的请求不同于来自`/about/`的。

为此，在`app.py`内部，让我们创建两个处理这两个请求的方法：

```python
# app.py
from api.py import API

app = API()


def home(request, response):
    response.text = "Hello from the HOME page"


def about(request, response):
    response.text = "Hello from the ABOUT page"

```

现在，我们需要以某种方式将这两种方法与上述路径联系起来：`/home/`和`/about/`。我喜欢Flask的做法，看起来像这样：

```python
# app.py
from api.py import API

app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"

```

你觉得怎么样？看起来不错？然后让我们实现这个bad boy吧！

如您所见，该`route`方法是一个装饰器，接受一个路径并包装方法。实施起来应该不会太难：

```python
# api.py

class API:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    ...

```

这是我们在这里所做的。在该`__init__`方法中，在被调用的`self.routes`的地方我们简单地定义了一个`dict`，我们将路径存储为键, 处理程序handlers作为值。它看起来像这样：

```python
print(self.routes)

{
    "/home": <function home at 0x1100a70c8>,
    "/about": <function about at 0x1101a80c3>
}

```

在该`route`方法中，我们将路径作为参数，并且在装饰器方法中，只需将`self.routes`路径作为键放在字典中，将处理程序作为值。

在这一点上，我们有所有的拼图。我们有处理程序和与之关联的路径。现在，当一个请求进来时，我们需要检查它的`path`，找到一个合适的处理程序，调用该处理程序并返回一个适当的响应。我们这样做：

```python
# api.py
from webob import Request, Response

class API:
    ...

    def handle_request(self, request):
        response = Response()

        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response

    ...

```

不是太难了，是吗？我们简单地迭代`self.routes`，将路径与请求的路径进行比较，如果存在匹配，则调用与该路径关联的处理程序。

重新启动`gunicorn`并在浏览器中尝试这些路径。首先，访问`http://localhost:8000/home/`，然后去`http://localhost:8000/about/`。您应该看到相应的消息。很酷，对吗？

下一步，我们可以回答“如果找不到路径会怎么样？”的问题。让我们创建一个返回“Not found.”的简单HTTP响应的方法。状态代码为404：

```python
# api.py
from webob import Request, Response

class API:
    ...

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    ...

```

现在，让我们在我们的`handle_request`方法中使用它：

```python
# api.py
from webob import Request, Response

class API:
    ...

    def handle_request(self, request):
        response = Response()

        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response

        self.default_response(response)
        return response

    ...

```

重新启动`gunicorn`并尝试一些不存在的路由。你应该看到这个可爱的“Not found.” 页。现在，为了便于阅读，让我们重构一下找到自己方法的处理程序：

```python
# api.py
from webob import Request, Response

class API:
    ...

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if path == request_path:
                return handler

    ...

```

就像之前一样，它只是迭代`self.route`，将路径与请求路径进行比较，如果路径相同则返回对应处理程序。如果没有找到处理程序，则返回`None`。现在，我们可以在我们的`handle_request`方法中使用它：

```python
# api.py
from webob import Request, Response

class API:
    ...

    def handle_request(self, request):
        response = Response()

        handler = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)

        return response

    ...

```

我认为它看起来好多了，并且非常容易解释。重启`gunicorn`，看看一切都像以前一样有效。

此时，我们有路由和处理程序。它非常棒，但我们的路径很简单。它们不支持url路径中的关键字参数。如果我们想拥有`@app.route("/hello/{person_name}")`这条路径并且能够在我们的处理程序中使用`person_name`这样的内容：

```python
def say_hello(request, response, person_name):
    response.text = f"Hello, {person_name}"

```

为此，如果有人访问`/hello/Matthew/`，我们需要能够将`/hello/{person_name}/`路径与已注册的路径匹配并找到适当的处理程序。值得庆幸的是，已经有一个名为`parse`的包正确地为我们做了。让我们继续安装它：

```
pip install parse

```

让我们试一下:

```python
>>> from parse import parse
>>> result = parse("Hello, {name}", "Hello, Matthew")
>>> print(result.named)
{'name': 'Matthew'}

```

如您所见，它解析了字符串`Hello, Matthew`，并能够识别出`Matthew`是与我们提供的字符串`{name}`相对应的字符串。

让我们在我们的`find_handler`方法中使用它，不仅可以找到与路径对应的方法，还可以找到提供的关键字参数：

```python
# api.py
from webob import Request, Response
from parse import parse

class API:
    ...

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    ...

```

我们仍在迭代`self.routes`，现在不是比较请求路径的路径，而是尝试解析它，如果有结果，我们将处理程序和关键字参数作为字典返回。现在，我们可以在`handle_request`内部使用这个将这些参数传递给处理程序，如下所示：

```python
# api.py
from webob import Request, Response
from parse import parse

class API:
    ...

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    ...

```

唯一的变化是，我们得到了两个`handler`和`kwargs`从`self.find_handler`，并传递一个`kwargs`像这样的处理`**kwargs`。

让我们用这种类型的路径编写一个处理程序并试一试：

```python
# app.py
...

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"

...

```

重启你的`gunicorn`访问`http://localhost:8000/hello/Matthew/`。你应该有这个美妙的信息: `Hello, Matthew`。太棒了吧？再添加几个这样的处理程序。您还可以指出给定参数的类型。例如，您可以将处理程序内的`@app.route("/tell/{age:d}")`参数`age`作为数字。

## 结论

这是一个漫长的旅程，但我认为这很棒。我写这篇文章时亲自学到了很多东西。如果你喜欢这篇博文，请在评论中告诉我们我们应该在框架中实现的其他功能。我在考虑基于类的处理程序，支持模板和静态文件。

Fight on!

> *在[这里]({filename}how-to-write-a-python-web-framework-2.md)查看第二部分*
