#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/14

from django.conf.urls import url

from web.views import home

urlpatterns = [
    url(r'^$', home.HomePageView.as_view(), name='home'),

    url(r'^details/(?P<pk>[0-9]+)/$', home.ArticleDetailView.as_view(), name='article-detail'),

    url(r'^book/(?P<book_name>.*)/$', home.BookPageView.as_view(), name='book'),

]

