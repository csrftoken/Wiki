#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/14

from django.db.models import F
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView


from web import models


class HomePageView(RedirectView, TemplateView):

    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):

        book = models.Book.objects.first()

        section = models.BookSection.objects.filter(chapter__book=book).first()

        kwargs["pk"] = section.pk

        return super(HomePageView, self).get_redirect_url(*args, **kwargs)


class BookPageView(RedirectView, TemplateView):

    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):

        book = get_object_or_404(models.Book, **{'name': kwargs.pop('book_name')})

        section = models.BookSection.objects.filter(chapter__book=book).first()

        kwargs['pk'] = section.pk

        return super(BookPageView, self).get_redirect_url(*args, **kwargs)


class ArticleDetailView(TemplateView):

    template_name = 'web/detail.html'

    def get_context_data(self, **kwargs):

        context = super(ArticleDetailView, self).get_context_data(**kwargs)

        section = get_object_or_404(models.BookSection, pk=kwargs['pk'])

        # 更新 `pv`
        section.pv = F('pv') + 1

        # 更新 `uv`
        # 策略: 依据 `session`
        session = self.request.session
        visit_date = session.get(self.request.path)
        current_date = now().strftime('%Y-%m-%d')
        update_uv_status = False
        if visit_date:
            if visit_date != current_date:
                del session[self.request.path]
                update_uv_status = True
        else:
            update_uv_status = True

        if update_uv_status:
            section.uv = F('uv') + 1
            session[self.request.path] = current_date

        section.save(update_fields=('pv', 'uv', ))
        section.refresh_from_db()

        context['section'] = section

        return context
