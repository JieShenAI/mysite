from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from django.http.response import JsonResponse


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL /login/
        if request.path_info in ["/home/", "/user/login/", "/image/code/", "/user/register/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登陆过，就可以继续向后走。
        # info_dict = request.session.get("info")
        # print(info_dict)
        # print(request.path_info)
        token = request.headers.get("token")
        if token is not None:
            return

        # 2.没有登录过，重新回到登录页面
        # return redirect('/#/user/login/')
        return JsonResponse({"code": "404", "data": {"msg": "未登录"}})
