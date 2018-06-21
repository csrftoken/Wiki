#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/16

from django.conf.urls import url

from management.views import (
    auth,
    home,
)

urlpatterns = [

    # BASE
    url(r'^$', home.HomePageView.as_view(), name='dashboard'),

    url(r'^table/(\w+)/(\w+)/$', home.table_obj_list, name="table_list"),
    url(r'^table/(\w+)/(\w+)/add/$', home.table_obj_add, name="table_obj_add"),
    url(r'^table/(\w+)/(\w+)/change/(\d+)/$', home.table_obj_change, name="table_obj_change"),

    url(r'^login/$', auth.acc_login),
    url(r'^logout/$', auth.acc_logout, name="logout"),


    url(r'chapter/manage/(?P<pk>\d+)/', home.ChapterManageView.as_view(), name="chapter_manage")

]
