#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
@author:Jaunezhou
@file:urls.py
@NAME:sharewithyou
@time:2021/12/22
@IDE: PyCharm
 
"""
from django.urls import path

from . import views
# from homeapp import views

app_name = 'userprofile'
# 如果这里加了app_name.
# 那么在html中使用url解析时需要加homeapp:home

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]
