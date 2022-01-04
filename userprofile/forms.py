#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
@author:Jaunezhou
@file:forms.py
@NAME:sharewithyou
@time:2021/12/22
@IDE: PyCharm
 
"""

from django.db import models
# 引入表单类
from django import forms

# 引入 User 模型
from django.contrib.auth.models import User

# forms.Form则需要手动配置每个字段，
# 它适用于不与数据库进行直接交互的功能。
# 用户登录不需要对数据库进行任何改动，
# 因此直接继承forms.Form就可以了
# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


