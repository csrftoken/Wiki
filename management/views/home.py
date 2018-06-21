#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/16

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import QueryDict
from django.contrib.auth.decorators import login_required

from kingadmin import views as admin_views

from web import models

from management.forms.home import (
    ChapterModelForm, SectionModelForm
)
from .auth import AuthView


class HomePageView(AuthView):

    """主页"""

    template_name = "management/dashboard.html"


# class TableListView(AuthView):
#
#     """ 展示每个表的数据 """
#
#     template_name = "management/table_obj_list.html"
#
#
# class TableAddView(AuthView):
#
#     """ 添加表数据 """
#
#     template_name = "management/table_obj_add.html"
#
#
# class TableChangeView(AuthView):
#
#     """ 修改表数据 """
#
#     template_name = "management/table_obj_change.html"


@login_required(login_url="/manage/login/")
def table_obj_list(request, app_name, model_name):
    template_data = admin_views.display_table_list(request, app_name, model_name, embed=True)
    if type(template_data) is dict:
        # print("template data",template_data,type(template_data))
        return render(request, 'management/table_obj_list.html', template_data)
    else:  # 调用的视图可能出错了，返回了一个错误页面，这里不做处理，也直接返回
        return template_data


@login_required(login_url="/manage/login/")
def table_obj_add(request, app_name, model_name):
    template_data = admin_views.table_add(request, app_name, model_name, embed=True)
    if type(template_data) is dict:
        # print("template data",template_data,type(template_data))
        return render(request, 'management/table_obj_add.html', template_data)
    else:  # 调用的视图可能出错了，返回了一个错误页面，这里不做处理，也直接返回
        return template_data


@login_required(login_url="/manage/login/")
def table_obj_change(request, app_name, model_name, object_id):
    template_data = admin_views.table_change(request, app_name, model_name, object_id, embed=True)
    if type(template_data) is dict:
        # print("template data",template_data,type(template_data))
        return render(request, 'management/table_obj_change.html', template_data)
    else:  # 调用的视图可能出错了，返回了一个错误页面，这里不做处理，也直接返回
        return template_data


class ChapterManageView(AuthView):
    """ Wiki 书籍章节管理界面 """

    template_name = "management/custom/chapter_manage.html"

    def get_context_data(self, **kwargs):
        context = super(ChapterManageView, self).get_context_data(**kwargs)

        wiki_book = get_object_or_404(models.Book, **{"pk": kwargs.pop("pk")})

        context["wiki_book"] = wiki_book

        # 获取请求类型, 展示不同的界面
        req_type = self.request.GET.get("req_type", "default_")

        # 获取数据对应关联的数据
        data = []
        book_chapters = wiki_book.bookchapter_set.all().order_by("order")

        for item in book_chapters.iterator():
            item_dic = dict()
            item_dic["chapter"] = item
            item_dic["chapter_sections"] = item.booksection_set.all().order_by("order")

            data.append(item_dic)

        context["data"] = data

        req_type, handle = req_type.split("_")

        form = ChapterModelForm if req_type == "chapter" else SectionModelForm

        pk = None

        if handle == "edit":

            pk = self.request.GET.get("pk")  # 如果是编辑提取 `pk`
            instance = get_object_or_404(form.Meta.model.objects.all(), **{"pk": pk})
            form_obj = form(instance=instance)

        elif handle == "add":

            num = int(self.request.GET.get("num"))  # 如果是添加提取 `num`

            fk_instance = get_object_or_404(
                models.Book if req_type == "chapter" else models.BookChapter,
                **{"pk": self.request.GET.get("fk_pk")}
            )

            if req_type == "chapter":
                initial = {
                    "book": fk_instance,
                    "chapter": num,
                    "order": num,
                }
            else:
                initial = {
                    "chapter": fk_instance,
                    "order": num
                }

            form_obj = form(initial=initial)

        else:
            form_obj = None

        # 默认展示所有
        context["show_type"] = req_type

        context["form"] = form_obj

        context["pk"] = pk

        return context

    def post(self, request, pk):

        context = self.get_context_data(**{"pk": pk})

        # 如果 `PK` 不为 None, 则表示编辑, 反之为添加操作
        edit_pk = request.GET.get("pk", None)

        handle_type, *_ = str(request.GET.get("req_type")).split("_")

        # 获取认证 `Form`
        form = ChapterModelForm if handle_type == "chapter" else SectionModelForm

        instance = get_object_or_404(form.Meta.model.objects.all(), **{"pk": edit_pk}) if edit_pk else None

        form_obj = form(request.POST, instance=instance)

        if form_obj.is_valid():
            form_obj.save()
            context["show_type"] = "default"

            context["msg"] = "{}{}成功".format(
                "编辑" if edit_pk else "添加",
                "wiki章节" if handle_type == "chapter" else "wiki课时"
            )

        else:
            context["show_type"] = handle_type
            context['form'] = form_obj

        return self.render_to_response(context)

    def delete(self, request, pk):

        super(ChapterManageView, self).get_context_data(**{"pk": pk})

        data = QueryDict(request.body.decode(settings.DEFAULT_CHARSET))

        pk = data.get("pk")

        model = models.BookChapter if data.get("del_type") == "chapter" else models.BookSection

        model.objects.filter(pk=pk).delete()

        return JsonResponse({"status": True, "msg": ""})
