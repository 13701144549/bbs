# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-12 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs_app', '0002_auto_20180412_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间'),
        ),
    ]