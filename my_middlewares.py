"""
自定义中间件
"""
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect


class MdLogin(MiddlewareMixin):
    # 定义一个白名单列表
    w_list = ['/author_info/', '/press_info/', '/books_info/', '/index/', '/login/']
    # 定义一个黑名单列表
    b_list = ['/author/', '/press/', '/books/', '/wahaha/']
    # 定义一个请求关于请求前的中间件，作用是登陆验证
    def process_request(self, request):
        next_url = request.path_info
        if next_url in self.w_list or request.session.get('login') and request.session.get('user'):
            return
        elif next_url in self.b_list:
            return HttpResponse('这里不欢迎你')
        else:
            return redirect('/login/?next={}'.format(next_url))


