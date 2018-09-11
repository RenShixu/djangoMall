from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import re

class MallConsoleMiddleWare(object):
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        #1.不需要拦截的地址
        urls = ["/console/login",'/console/dologin','/console/loginout','/console/verify']
        path = request.path
        print(path)
        if re.match("/console",path) and (path not in urls):
            # 2.判断是否登录
            if "consoleuser" not in request.session:
                # 3.重定向
                return redirect(reverse("console_login_index"))
        #通过
        response = self.get_response(request)
        return response
