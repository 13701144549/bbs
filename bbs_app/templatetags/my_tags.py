from django import template
from bbs_app.models import *
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('menu.html')
def get_menu(username):
    user = UserInfo.objects.filter(username=username).first()
    time = user.create_time
    blog = user.blog
    cate_list = Category.objects.filter(blog=blog).annotate(count=Count('article')).values_list('title', 'count')
    tag_list = Tag.objects.filter(blog=blog).annotate(count=Count('article')).values_list('title', 'count')
    date_list = Article.objects.filter(user=user).extra(
        select={'date_time_new': "DATE_FORMAT(create_time, '%%Y-%%m')"}).values('date_time_new').annotate(
        count=Count("id")).values_list(
        "date_time_new", 'count')
    return {"username": username, "cate_list": cate_list, "tag_list": tag_list, "date_list": date_list, 'time': time,
            'user': user}


@register.inclusion_tag('backstage_menu.html')
def get_backstage_menu(username):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    cate_list = Category.objects.filter(blog=blog).annotate(count=Count('article')).values_list('title', 'count')
    tag_list = Tag.objects.filter(blog=blog).annotate(count=Count('article')).values_list('title', 'count')
    date_list = Article.objects.filter(user=user).extra(
        select={'date_time_new': "DATE_FORMAT(create_time, '%%Y-%%m')"}).values('date_time_new').annotate(
        count=Count("id")).values_list(
        "date_time_new", 'count')
    return {"username": username, "cate_list": cate_list, "tag_list": tag_list, "date_list": date_list,
            'user': user}

