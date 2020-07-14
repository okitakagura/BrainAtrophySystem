# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone
# Create your models here.

# 用户表
class UserInfo(models.Model):
    user = models.CharField(max_length=20)
    password = models.EmailField(max_length=200)
    email = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    qq = models.IntegerField(default=0)
    login_time = models.CharField(max_length=30)

#文件表
class ImageFile(models.Model):
    filename = models.CharField(max_length=200)
    addtime = models.DateTimeField('保存日期', default=timezone.now)