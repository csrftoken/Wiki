#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/19

from django import template
from django.utils import six


register = template.Library()


@register.inclusion_tag("management/inclusion/handle.html")
def get_handle(event_type, num, fk_pk):
    # 获取排序序号
    num = (0 if not six.text_type(num).isdigit() else int(num)) + 1
    # 获取操作的识别符号
    handle_msg = "添加章节" if event_type == "chapter_add" else "添加课时"
    # 构建上下文
    return {
        "event_type": event_type,
        "num": num,
        "fk_pk": fk_pk,
        "handle_msg": handle_msg
    }
