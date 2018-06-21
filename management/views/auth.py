#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/17

from django.views.generic.base import TemplateView

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.conf import settings


class AuthView(TemplateView, ):
    """认证基类, 如果要为其它的视图添加权限之类的, 可继续累加装饰器

    FormView,

    ...

    """

    @method_decorator(login_required(login_url=settings.LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url=settings.LOGIN_URL)
def acc_logout(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)


def acc_login(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or settings.LOGIN_REDIRECT_URL)
        else:
            error = "Wrong username or password!"

    return render(request, 'management/login.html', {'error': error})
