#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/6/19

from django import forms

from ckeditor.widgets import CKEditorWidget

from web import models


class ChapterModelForm(forms.ModelForm):

    class Meta:
        model = models.BookChapter
        fields = "__all__"
        error_messages = {
            "chapter": {"required": "章节数字不能为空"},
            "name": {"required": "章节名称不能为空", "max_length": "章节名不能大于128位"}
        },
        labels = {
            "book": "Wiki名称",
            "name": "章节名称(*)",
            "chapter": "第几章节"
        },
        help_texts = {
            "chapter": "默认已排好序，如需排序，请先添加章节，返回首页进行排序操作"
        },
        widgets = {
            "name": forms.widgets.Input(attrs={'class': 'form-control'}),
            "chapter": forms.widgets.Input(attrs={'class': 'form-control'}),
            'brief': forms.widgets.Input(attrs={'class': 'form-control'}),
            'book': forms.widgets.Select(attrs={'class': 'form-control'}),
            'order': forms.widgets.Input(attrs={'class': 'form-control'}),
        }


class SectionModelForm(forms.ModelForm):

    class Meta:
        model = models.BookSection
        fields = (
            "chapter",
            "name",
            "status",
            "order",
            "memo",
            "content",
        )

        widgets = {
            "chapter": forms.widgets.Select(attrs={'class': 'form-control'}),
            'name': forms.widgets.Input(attrs={'class': 'form-control'}),
            'status': forms.widgets.CheckboxInput(),
            'content': CKEditorWidget(attrs={'class': 'form-control'}),
            'order': forms.widgets.Input(attrs={'class': 'form-control'}),
            'memo': forms.widgets.Input(attrs={'class': 'form-control'}),
        }
