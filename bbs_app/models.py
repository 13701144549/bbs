from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 建立用户信息表
class UserInfo(AbstractUser):
    id = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, verbose_name='用户手机号', null=True, unique=True)
    create_time = models.DateTimeField(verbose_name='用户注册时间', auto_now_add=True)
    avatar = models.FileField(upload_to='avatars/', default='/avatars/default.png')
    blog = models.OneToOneField(to='Blog', to_field='id', null=True)

    def __str__(self):
        return self.username


# 创建博客信息表
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=32)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32)
    theme = models.CharField(verbose_name='个人博客主题', max_length=32)

    def __str__(self):
        return self.title


# 建立文章信息表
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='文章标题')
    desc = models.TextField(verbose_name='文章描述')
    create_time = models.DateTimeField(verbose_name='文章发布时间', auto_now_add=True)
    comment_count = models.IntegerField(default=0, verbose_name='文章评论数')
    up_count = models.IntegerField(default=0, verbose_name='文章点赞数')
    down_count = models.IntegerField(default=0, verbose_name='文章踩灭数')
    category = models.ForeignKey(to='Category', to_field='id', verbose_name='文章所属分类', null=True)
    user = models.ForeignKey(verbose_name='文章作者', to='UserInfo', to_field='id')
    tags = models.ManyToManyField(
        to='Tag',
        through='ArticleToTag',
        through_fields=('article', 'tag'),
        verbose_name='文章标签'
    )

    def __str__(self):
        return self.title


# 建立文章详情表
class ArticleDetail(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章具体内容')
    article = models.OneToOneField(to='Article', to_field='id', verbose_name='文章')


# 建立文章和标签多对多第三方表
class ArticleToTag(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='id')
    tag = models.ForeignKey(verbose_name='标签', to='Tag', to_field='id')

    class Meta:
        unique_together = (('article', 'tag'),)

    def __str__(self):
        return self.article.title + '--' + self.tag.title


# 建立分类表
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='分类标题')
    blog = models.ForeignKey(verbose_name='分类所属个人博客', to='Blog', to_field='id')

    def __str__(self):
        return self.title


# 建立标签表
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='标签名')
    blog = models.ForeignKey(to='Blog', to_field='id', verbose_name='标签所属个人博客')

    def __str__(self):
        return self.title


# 文章点赞和踩灭表
class ArticleUpDown(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(null=True, to='UserInfo', verbose_name='点赞和踩灭表一对多关联用户id')
    article_id = models.ForeignKey(null=True, to='Article', verbose_name='点赞和踩灭表一对多关联文章id')
    is_up = models.BooleanField(verbose_name='是否点赞', default=True)

    class Meta:       # 创建联合唯一关系
        unique_together = (('user_id', 'article_id'),)


# 建立评论表
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(to='UserInfo', verbose_name='评论一对多关联用户表')
    article_id = models.ForeignKey(to='Article', verbose_name='评论一对多关联文章表')
    create_time = models.DateTimeField(verbose_name='评论发表时间', auto_now_add=True)
    content = models.TextField(verbose_name='评论内容')
    parent_comment = models.ForeignKey("self", null=True, default=None, verbose_name='评论一对多关联自身')

    def __str__(self):
        return self.content