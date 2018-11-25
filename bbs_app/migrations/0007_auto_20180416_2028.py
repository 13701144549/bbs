# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-16 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs_app', '0006_auto_20180416_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(default=0, verbose_name='文章评论数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='down_count',
            field=models.IntegerField(default=0, verbose_name='文章踩灭数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='up_count',
            field=models.IntegerField(default=0, verbose_name='文章点赞数'),
        ),
    ]