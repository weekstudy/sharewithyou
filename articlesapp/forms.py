#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
@author:Jaunezhou
@file:forms.py
@NAME:sharewithyou
@time:2021/12/23
@IDE: PyCharm
 
"""
# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost
# 表单类继承了forms.ModelForm，
# 这个父类适合于需要直接与数据库交互的功能，比如新建、更新数据库的字段等。
# 如果表单将用于直接添加或编辑Django模型，则可以使用 ModelForm来避免重复书写字段描述
# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'body', 'tags', 'avatar_svg')





