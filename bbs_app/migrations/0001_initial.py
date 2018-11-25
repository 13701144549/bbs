# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-12 13:39
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('telephone', models.BigIntegerField(verbose_name='用户手机号')),
                ('create_time', models.DateField(verbose_name='用户注册时间')),
                ('avatar', models.FileField(default='/avatars/default.png', upload_to='avatars/')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='文章标题')),
                ('desc', models.TextField(verbose_name='文章描述')),
                ('create_time', models.DateTimeField(verbose_name='文章发布时间')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='文章具体内容')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleToTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleUpDown',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_up', models.BooleanField(default=True, verbose_name='是否点赞')),
                ('article_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Article', verbose_name='点赞和踩灭表一对多关联文章id')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞和踩灭表一对多关联用户id')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='个人博客标题')),
                ('site', models.CharField(max_length=32, verbose_name='个人博客后缀')),
                ('theme', models.CharField(max_length=32, verbose_name='个人博客主题')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Blog', verbose_name='分类所属个人博客')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(verbose_name='评论发表时间')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Article', verbose_name='评论一对多关联文章表')),
                ('parent_comment', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Comment', verbose_name='评论一对多关联自身')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论一对多关联用户表')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='标签名')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Blog', verbose_name='标签所属个人博客')),
            ],
        ),
        migrations.AddField(
            model_name='articletotag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Category', verbose_name='文章所属分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='bbs_app.ArticleToTag', to='bbs_app.Tag', verbose_name='文章标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='文章作者'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='blog',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bbs_app.Blog'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='articleupdown',
            unique_together=set([('user_id', 'article_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='articletotag',
            unique_together=set([('article', 'tag')]),
        ),
    ]