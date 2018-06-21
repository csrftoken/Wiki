#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/15

from django import template

from web import models


register = template.Library()


@register.filter
def section_filter(sections):
    return sections


@register.inclusion_tag("web/inclusion/book_summary.html")
def get_book_summary():

    book = models.Book.objects.all().first()

    return {
        "book": book
    }


@register.inclusion_tag("web/inclusion/book_header.html")
def get_book_header():

    books = models.Book.objects.all()

    return {
        "books": books
    }


@register.inclusion_tag("web/inclusion/book_page.html")
def get_book_page(section):

    # 获取当前课时的上一个课时和下一个课时

    queryset = models.BookSection.objects.filter(chapter=section.chapter)

    return {
        "prev_section": queryset.filter(order__lt=section.order).last(),
        "next_section": queryset.filter(order__gt=section.order).first(),
    }
