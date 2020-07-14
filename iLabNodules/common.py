# coding=utf-8
from django.contrib import admin
from django.shortcuts import render, redirect, HttpResponse

# 编写装饰器检查用户是否登录
def auth(func):
    def inner(request, *args, **kwargs):
        # 获取session判断用户是否已登录
        if request.session.get('username'):
            # 已经登录的用户...
            return func(request, *args, **kwargs)
        else:
            # 没有登录的用户，跳转刚到登录页面
            return redirect("/login")

    return inner

