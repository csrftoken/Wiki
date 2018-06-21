#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/16


from kingadmin.admin_base import BaseKingAdmin
from kingadmin.admin_base import site

from web import models

BaseKingAdmin.base_app_url = "/manage/table"


class BookAdmin(BaseKingAdmin):

    object_add_link = "/manage/table/web/book/add/"
    model_display_name = "课程Wiki列表"
    list_display = ["name", "brief", "status", "date", "chapter_handle"]
    list_filter = ["status", "date", ]

    def chapter_handle(self, ):

        return '<a href="/manage/chapter/manage/{}/"><i class="fa fa-cog" aria-hidden="true"></i> 章节管理</a>'.format(
            self.instance.pk
        )

    chapter_handle.display_name = "操作"


class BookChapterAdmin(BaseKingAdmin):

    object_add_link = "/manage/table/web/bookchapter/add/"
    model_display_name = "课程Wiki章节"
    list_display = ["book", "name", "chapter", "brief", "order", "date"]
    list_filter = ["book", "date", ]


class BookSectionAdmin(BaseKingAdmin):

    object_add_link = "/manage/table/web/booksection/add/"
    model_display_name = "课程Wiki课时"
    list_display = ["name", "pv", "uv", "status", "date", ]
    list_filter = ["status", "date", ]


site.register(models.Book, BookAdmin)
site.register(models.BookChapter, BookChapterAdmin)
site.register(models.BookSection, BookSectionAdmin)
