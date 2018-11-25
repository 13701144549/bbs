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
from django.conf.urls import url
from django.contrib import admin
from bbs_app import views
from django.views.static import serve
from BBS import settings

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r"poll/$", views.poll),  # 点赞或踩灭
    url(r"comment/$", views.comment),  # 评论楼
    url(r"get_comment_tree/(\d+)$", views.get_comment_tree),  # 评论树



    url("(?P<username>.*)/(?P<condition>tag|category|date)/(?P<param>.*)/$", views.personal_home),  # 个人博客主页面
    url("(?P<username>\w+)/articles/(?P<article_id>\d+)/$", views.article_detail),  # 文章详情页面



    url("(?P<username>.*)/(?P<condition>backstage|delete_article)/(?P<id>.*)$", views.backstage),  # 用户后台系统和删除系统
    url("(?P<username>.*)/(?P<condition>article_add|edit_article)/(?P<id>.*)$", views.article_operation),  # 用户新增文章系统和编辑系统
    # url("(?P<username>.*)/edit_article/(?P<id>\d+)/$", views.edit_article),  # 用户编辑文章系统
    # url("(?P<username>.*)/delete_article/(?P<id>\d+)/$", views.delete_article),  # 用户删除文章系统


    url('(?P<username>.*)/$', views.personal_home, name='personal_home'),  # 个人博客主页面





]
