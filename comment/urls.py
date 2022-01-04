#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
@author:Jaunezhou
@file:urls.py
@NAME:sharewithyou
@time:2021/12/24
@IDE: PyCharm
 
"""



from django.urls import path

from . import views

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
]