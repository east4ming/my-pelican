Title: 如何编写Python Web框架（二）
Date: 2019-03-01 15:51
Status: published
Category: Python
Tags: python, web框架
Slug: write-python-framework-part-two
Author: 东风微鸣
Summary: 编写自己的Python Web框架, 实现: 检查重复的路径; 基于类的处理程序; 单元测试

![]({static}/images/Python-Web-Development-Tutorials.jpg)
# 如何编写Python Web框架（二）

> 本文为译文
>
> 原文链接: [How to write a Python web framework. Part II.](http://rahmonov.me/posts/write-python-framework-part-two/)
>
> 作者: Jahongir Rahmonov
>
> Github仓库: [alcazar](https://github.com/rahmonov/alcazar)

在[第一部分中]({filename}how-to-write-a-python-web-framework-1.md)，我们开始编写自己的Python框架并实现以下功能：

- WSGI兼容
- 请求处理程序
- 路由：简单和参数化

请务必在此之前阅读系列的[第一部分]({filename}how-to-write-a-python-web-framework-1.md)。

这部分同样令人兴奋，我们将在其中添加以下功能：

- 检查重复的路径
- 基于类的处理程序
- 单元测试

Ready? 让我们开始吧。

## 重复的路径

现在，我们的框架允许添加任意次数相同的路由。因此，以下内容将起作用：

```python
@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/home")
def home2(request, response):
    response.text = "Hello from the SECOND HOME page"
```

框架不会抱怨，因为我们使用Python字典来存储路由，只有最后一个才能使用`http://localhost:8000/home/`。显然，这并不好。我们希望确保框架在用户尝试添加现有路由时会抛出信息。您可以想象，实施起来并不是很困难。因为我们使用Python dict来存储路由，所以我们可以简单地检查字典中是否已存在给定路径。如果是，我们抛出异常，如果不是，我们让它添加一个路由。在我们编写任何代码之前，让我们回忆下我们的主要`API`类：

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

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."
```

我们需要更改`route`函数，以便在再次添加现有路由时抛出异常：

```python
# api.py

def route(self, path):
    if path in self.routes:
        raise AssertionError("Such route already exists.")

    def wrapper(handler):
        self.routes[path] = handler
        return handler

    return wrapper
```

现在，尝试添加相同的路径两次并重新启动你的gunicorn。您应该看到抛出以下异常：

```
Traceback (most recent call last):
...
AssertionError: Such route already exists.
```

我们可以重构它以将其减少到一行：

```python
# api.py

def route(self, path):
    assert path not in self.routes, "Such route already exists."

    ...
```

完工！进入下一个功能。

## 基于类的处理程序

如果你了解Django，你知道它支持基于函数和基于类的视图（即我们的处理程序）。我们已经有了基于函数的处理程序。现在我们将添加基于类的，适用于更复杂, 更大的处理程序。我们基于类的处理程序将如下所示：

```python
# app.py

@app.route("/book")
class BooksHandler:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

    ...
```

这意味着我们存储路径的dict:  `self.routes`可以包含类和函数作为值。因此，当我们在`handle_request()`方法中找到一个处理程序时，我们需要检查处理程序是一个函数还是一个类。如果它是一个函数，它应该像现在一样工作。如果它是一个类，根据请求方法，我们应该调用该类的对应方法。也就是说，如果请求方法是`GET`，我们应该调用类的`get()`方法，如果是`POST`我们应该调用`post`方法等。这是`handle_request()`方法现在的样子：

```python
# api.py

def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        handler(request, response, **kwargs)
    else:
        self.default_response(response)

    return response
```

我们要做的第一件事是检查找到的处理程序是否是一个类。为此，我们使用`inspect`模块：

```python
# api.py

import inspect

...

def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        if inspect.isclass(handler):
            pass   # class based handler is being used
        else:
            handler(request, response, **kwargs)
    else:
        self.default_response(response)

    return response

...
```

现在，如果正在使用基于类的处理程序，我们需要根据请求方法找到类的适当方法。为此，我们可以使用内置的`getattr`函数：

```python
# api.py

def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        if inspect.isclass(handler):
            handler_function = getattr(handler(), request.method.lower(), None)
            pass
        else:
            handler(request, response, **kwargs)
    else:
        self.default_response(response)

    return response
```

`getattr`接受一个对象实例作为第一个参数，将属性名称作为第二个参数。第三个参数是如果没有找到则返回的值。因此，`GET`将返回`get`，`POST`返回`post`, `some_other_attribute`返回`None`。如果`handler_function`是`None`，则表示此类函数未在类中实现，并且不允许此请求方法：

```python
if inspect.isclass(handler):
    handler_function = getattr(handler(), request.method.lower(), None)
    if handler_function is None:
        raise AttributeError("Method not allowed", request.method)
```

如果实际找到了handler_function，那么我们只需调用它：

```python
if inspect.isclass(handler):
    handler_function = getattr(handler(), request.method.lower(), None)
    if handler_function is None:
        raise AttributeError("Method now allowed", request.method)
    handler_function(request, response, **kwargs)
```

现在整个方法看起来像这样：

```python
def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        if inspect.isclass(handler):
            handler_function = getattr(handler(), request.method.lower(), None)
            if handler_function is None:
                raise AttributeError("Method now allowed", request.method)
            handler_function(request, response, **kwargs)
        else:
            handler(request, response, **kwargs)
    else:
        self.default_response(response)
```

我不喜欢我们有两个`handler_function`和`handler`。我们可以重构它们以使它更优雅：

```python
def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        if inspect.isclass(handler):
            handler = getattr(handler(), request.method.lower(), None)
            if handler is None:
                raise AttributeError("Method now allowed", request.method)

        handler(request, response, **kwargs)
    else:
        self.default_response(response)

    return response
```

就是这样。我们现在可以测试对基于类的处理程序的支持。首先，如果你还没有, 请将此处理程序添加到`app.py`：

```python
@app.route("/book")
class BooksHandler:
    def get(self, req, resp):
        resp.text = "Books Page"
```

现在，重新启动你的gunicorn并转到页面`http://localhost:8000/book`，你应该看到消息`Books Page`。就这样, 我们增加了对基于类的处理程序的支持。可以试试实现其他方法(例如`post`和`delete`)。

进入下一个功能！

## 单元测试

如果没有单元测试，哪个项目是可靠的，对吧？所以让我们添加几个。我喜欢使用`pytest`，所以让我们安装它：

```shell
pip install pytest
```

并创建一个文件，我们将编写测试：

```shell
touch test_bumbo.py
```

提醒一下，`bumbo`是框架的名称。您可能以不同的方式命名。另外，如果您不知道[pytest](https://docs.pytest.org/en/latest/)是什么，我强烈建议您查看它以了解如何编写单元测试。

首先，让我们为我们的`API`类创建一个我们可以在每个测试中使用的工具：

```python
# test_bumbo.py
import pytest

from api import API


@pytest.fixture
def api():
    return API()
```

现在，对于我们的第一次单元测试，让我们从简单的开始。让我们测试一下我们是否可以添加路径。如果它没有抛出异常，则表示测试成功通过：

```python
def test_basic_route(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"
```

像这样运行测试：`pytest test_bumbo.py`你应该看到如下内容：

```
collected 1 item

test_bumbo.py .                                                                                                                                                            [100%]

====== 1 passed in 0.09 seconds ======
```

现在，让我们测试它是否会在我们尝试添加现有路由时抛出异常：

```python
# test_bumbo.py

def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO"
```

再次运行测试，您将看到它们都通过了。

我们可以添加更多测试，例如默认响应，参数化路由，状态代码等。但是，所有测试都要求我们向处理程序发送HTTP请求。为此，我们需要一个测试客户端。但是如果我们在这里做的话，我认为这篇文章会变得太大了。我们将在这些系列的下一篇文章中完成。我们还将添加对模板和其他一些有趣内容的支持。所以，请继续关注。

像往常一样，如果您想看一些功能实现，请在评论部分告诉我。

P.S. 这些博客文章基于我正在构建的[Python Web框架](https://github.com/rahmonov/alcazar)。因此，[请在这儿](https://github.com/rahmonov/alcazar)查看博客中的内容，一定要通过star该repo来表达你的喜爱。

Fight on!
