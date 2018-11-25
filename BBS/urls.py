"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from bbs_app import views
from django.views.static import serve
from BBS import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^login/', views.login, name='login'),  # 登录界面
    url(r'^system_home/', views.system_home, name='system_home'),  # 系统主界面
    url(r'^register/', views.register, name='register'),  # 注册界面
    url(r'^reset/', views.reset, name='reset'),  # 重置密码界面
    url(r'^help/', views.help, name='help'),  # 帮助界面
    url(r'^logout/', views.logout, name='logout'),  # 注销函数

    # url(r"backstage/$", views.backstage),  # 后台管理
    # url(r"article_add/$", views.article_add),  # 新增文章

    url(r'^get_valid_img/', views.get_valid_img, name='get_valid_img'),       # 图片验证码函数
    url(r'^pc-geetest/register', views.pc_get_captcha, name='pcgetcaptcha'),  # 滑动验证码函数

    url(r'^bbs_app/', include('bbs_app.urls')),  # 连接子url




    url(r'^$', views.login),  # 默认返回登陆页面

    # media 配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),


    # 配置上传照片路径
    url(r'^upload_img/$', views.upload_img),
]
