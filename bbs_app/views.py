import os
import json
import random
from PIL import Image
from BBS import settings
from utils import mypage
from django.db.models import F
from django.contrib import auth
from django.db.models import Count
from django.db import transaction
from PIL import ImageDraw, ImageFont
from bbs_app.geetest import GeetestLib
from bbs_app.forms import ResetForm, RegisterForm
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import UserInfo, Article, Category, Tag, ArticleDetail, ArticleUpDown, Comment, Blog


# Create your views here.


# 图片验证码版登陆函数
# def login(request):
#     if request.is_ajax():
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         valid_code = request.POST.get('valid_code')
#         res = {'state': False, 'msg': None}
#         valid_str = request.session.get('valid_str')
#         if valid_code.upper() == valid_str.upper():
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 res['state'] = True
#                 auth.login(request, user)
#             else:
#                 res['msg'] = '用户名或者密码错误'
#         else:
#             res['msg'] = '验证码错误'
#         return JsonResponse(res)
#     return render(request, 'login.html')


# 生成验证码函数
def get_valid_img(request):
    # 产生随机颜色函数
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    image = Image.new('RGB', (100, 50), get_random_color())  # 给图片画背景颜色
    # 生成五个随机字符做验证图片内容
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('static/font/kumo.ttf', size=32)
    temp = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((3 + i * 20, 6), random_char, get_random_color(), font=font)
        # 保存随机字符
        temp.append(random_char)
        # 噪点噪线
        width = 260
        height = 40
        for i in range(5):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=get_random_color())

        for i in range(10):
            draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

            # 在内存生成图片
    from io import BytesIO
    f = BytesIO()
    image.save(f, 'png')
    data = f.getvalue()
    f.close()

    # 把验证字符存到session中
    valid_str = ''.join(temp)
    request.session['valid_str'] = valid_str

    return HttpResponse(data)


# 系统主页面函数
# @login_required
def system_home(request):
    # if not request.user.username:
    #     return redirect('/login/')
    article_list = Article.objects.all()

    # 分页开始
    data_num = article_list.count()  # 数据的总数
    current_page = request.GET.get("page", 1)
    obj = mypage.Pagination(data_num, current_page, "/system_home/", 10, 10)
    article_list = article_list[obj.start:obj.end]
    page_html = obj.page_html
    # 分页结束

    return render(request, 'system_home.html', locals())


# 滑动验证相关开始
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


def pc_get_captcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 滑动验证版登录
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.session.get('next_url')
        res = {'state': False, 'msg': None, 'next_url': next_url}
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            user = auth.authenticate(username=username, password=password)
            if user:
                res['state'] = True
                auth.login(request, user)
            else:
                res['msg'] = '用户名或者密码错误'
        return JsonResponse(res)
    return render(request, 'login.html')


# 滑动验证相关结束


# 注册函数
def register(request):
    if request.method == 'POST':
        res = {'flag': False, 'error_dict': None}
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            repeat_password = form.cleaned_data.get('repeat_password')
            email = form.cleaned_data.get('email')
            avatar = request.FILES.get('avatar')
            if avatar:
                UserInfo.objects.create_user(username=username, telephone=telephone, password=password, email=email,
                                             avatar=avatar)
            else:
                UserInfo.objects.create_user(username=username, telephone=telephone, password=password, email=email)
            res['flag'] = True
        else:
            res['error_dict'] = form.errors
        return JsonResponse(res)
    form = RegisterForm()
    return render(request, 'register.html', locals())


# 修改密码函数
@login_required
def reset(request):
    if request.method == 'POST':
        res = {'flag': False, 'error_dict': None}
        form = ResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            telephone = form.cleaned_data.get('telephone')
            new_password = form.cleaned_data.get('new_password')
            user_obj = UserInfo.objects.filter(username=username, telephone=telephone).first()
            user_obj.set_password(new_password)
            user_obj.save()
            res['flag'] = True
        else:
            res['error_dict'] = form.errors
        return JsonResponse(res)
    form = ResetForm()
    return render(request, 'reset.html', locals())


# 帮助页面函数
@login_required
def help(request):
    return render(request, 'help.html')


# 注销函数
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')


# 个人主页函数

def personal_home(request, username, **kwargs):
    # 当前用户对象
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'prompt.html')
    # 该用户的个人站点对象
    blog = user.blog
    if not kwargs:
        article_list = Article.objects.filter(user=user)
    else:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'tag':
            article_list = Article.objects.filter(user=user).filter(tags__title=param)
        elif condition == 'category':
            article_list = Article.objects.filter(user=user).filter(category__title=param)
        else:
            import datetime
            year, month = param.split("-")
            start_date = datetime.date(int(year), int(month), 1)
            end_date = datetime.date(int(year), int(month), 30)
            article_list = Article.objects.filter(user=user).filter(create_time__year=year, create_time__month=month)
            # article_list = Article.objects.filter(user=user).filter(create_time__range=(start_date, end_date))
    # 分页开始
    data_num = article_list.count()  # 数据的总数
    current_page = request.GET.get("page", 1)
    obj = mypage.Pagination(data_num, current_page, "/bbs_app/{}/".format(user.username))
    article_list = article_list[obj.start:obj.end]
    page_html = obj.page_html
    # 分页结束

    # 查询当前站点所有的分类
    # cate_list = Category.objects.filter(blog=blog)
    # 查询当前站点每一个分类以及对应的文章数
    # cate_list = Category.objects.filter(blog=blog).annotate(count=Count('article')).values_list('title', 'count')
    # 查询当前站点每一个标签以及对应的文章数
    # tag_list = Tag.objects.filter(blog=blog).annotate(count=Count('article')).values_list('title', 'count')
    # 按照日期归档分类
    # date_list = Article.objects.filter(user=user).extra(
    #     select={'date_time_new': "DATE_FORMAT(create_time, '%%Y-%%m')"}).values('date_time_new').annotate(
    #     count=Count("id")).values_list(
    #     "date_time_new", 'count')
    return render(request, 'personal_home.html', locals())


# 文章详情函数
def article_detail(request, username, article_id):
    next_url = request.path
    request.session['next_url'] = next_url
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    article = Article.objects.filter(pk=article_id).first()
    comment_list = Comment.objects.filter(article_id_id=article_id)
    return render(request, 'article_detail.html', locals())


# 点赞或者踩灭函数
def poll(request):
    is_up = json.loads(request.POST.get('is_up'))
    article_id = request.POST.get('article_id')
    user_id = request.user.pk
    res = {'state': True}
    try:
        with transaction.atomic():
            ArticleUpDown.objects.create(is_up=is_up, article_id_id=article_id, user_id_id=user_id)
            if is_up:
                Article.objects.filter(pk=article_id).update(up_count=F('up_count') + 1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F('down_count') + 1)
    except Exception as e:
        res['state'] = False
        res['first_operate'] = ArticleUpDown.objects.filter(article_id_id=article_id, user_id_id=user_id).first().is_up
    return JsonResponse(res)


# 评论函数
def comment(request):
    article_id_id = request.POST.get('article_id')
    content = request.POST.get('content')
    user_id_id = request.user.pk
    pid = request.POST.get('pid')
    res = {'state': True}
    with transaction.atomic():
        if not pid:
            comment_obj = Comment.objects.create(article_id_id=article_id_id, user_id_id=user_id_id,
                                                 content=content)  # 提交根评论
        else:
            comment_obj = Comment.objects.create(article_id_id=article_id_id, user_id_id=user_id_id, content=content,
                                                 parent_comment_id=pid)  # 提交根评论
        Article.objects.filter(pk=article_id_id).update(comment_count=F('comment_count') + 1)
    create_time = comment_obj.create_time.strftime('%Y-%m-%d %H:%M')
    content = comment_obj.content
    res['create_time'] = create_time
    res['content'] = content
    return JsonResponse(res)


# 评论树函数
def get_comment_tree(request, id):
    res = list(Comment.objects.filter(article_id_id=id).values('pk', 'content', 'create_time', 'user_id__username',
                                                               'parent_comment_id'))
    return JsonResponse(res, safe=False)


# 展示后台管理和删除文章函数
@login_required
def backstage(request, username, **kwargs):
    condition = kwargs.get('condition')
    if condition == 'backstage':
        user = UserInfo.objects.filter(username=username).first()
        article_list = Article.objects.filter(user=user)
        # 分页开始
        data_num = article_list.count()  # 数据的总数
        current_page = request.GET.get("page", 1)
        obj = mypage.Pagination(data_num, current_page, "/bbs_app/{}/backstage".format(user.username))
        article_list = article_list[obj.start:obj.end]
        page_html = obj.page_html
        # 分页结束
        return render(request, 'backstage.html', locals())
    elif condition == 'delete_article':
        id = kwargs.get('id')
        article_obj = Article.objects.filter(pk=id).first()
        article_obj.delete()
        return redirect('/bbs_app/{}/backstage'.format(username))


# 新增和编辑文章函数
@login_required
def article_operation(request, username, **kwargs):
    condition = kwargs.get('condition')
    if condition == 'article_add':
        if request.method == 'POST':
            title = request.POST.get('title')
            article_content = request.POST.get('article_content')
            user = request.user
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(article_content, 'html.parser')
            # 过滤
            for tag in soup.find_all():
                if tag.name == 'script':
                    tag.decompose()
            with transaction.atomic():
                article_obj = Article.objects.create(title=title, user=user, desc=soup.text[0:100])
                ArticleDetail.objects.create(content=soup.prettify(), article=article_obj)
            return redirect('/bbs_app/{}/backstage'.format(username))
        user = UserInfo.objects.filter(username=username).first()
        article_list = Article.objects.filter(user=user)
        return render(request, 'article_add.html', locals())
    elif condition == 'edit_article':
        id = kwargs.get('id')
        article_obj = Article.objects.filter(pk=id).first()
        article_detail_obj = ArticleDetail.objects.filter(article_id=id).first()
        if request.method == 'POST':
            title = request.POST.get('title')
            article_content = request.POST.get('article_content')
            user = request.user
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(article_content, 'html.parser')
            # 过滤
            for tag in soup.find_all():
                if tag.name == 'script':
                    tag.decompose()
            with transaction.atomic():
                article_obj.title = title
                article_obj.user = user
                article_obj.desc = soup.text[0:100]
                article_obj.save()
                article_detail_obj.content = soup.prettify()
                article_detail_obj.article = article_obj
                article_detail_obj.save()
            return redirect('/bbs_app/{}/backstage'.format(username))
        return render(request, 'article_add.html', locals())


# 上传照片存储函数
def upload_img(request):
    img_obj = request.FILES.get('img')
    media_path = settings.MEDIA_ROOT
    path = os.path.join(media_path, 'article_img', img_obj.name)
    f = open(path, 'wb')
    for line in img_obj:
        f.write(line)
    f.close()
    res = {
        'url': '/media/article_img/' + img_obj.name,
        'error': 0
    }
    return HttpResponse(json.dumps(res))



dict = {}
dict.items()
dict.items()
