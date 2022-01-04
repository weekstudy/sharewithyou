#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
@author:Jaunezhou
@file:forms.py
@NAME:sharewithyou
@time:2021/12/24
@IDE: PyCharm
 
"""

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 定义表单包含的字段
        # 模型中的2个外键将通过视图逻辑自动填写，
        # 所以这里只需要提交body就足够了
        fields = ['body']

