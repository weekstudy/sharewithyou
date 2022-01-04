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

app_name = 'articlesapp'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('articles/', views.article_list, name='articles'),
    path('show-article/<int:id>/', views.show_article, name='show_article'),
    path('articles/create/', views.article_create, name='article_create'),
    # 删除文章
    path('articles/delete/<int:id>/', views.article_delete, name='article_delete'),
    # 更新文章
    path('articles/update/<int:id>/', views.article_update, name='article_update'),
    path('articles/search/', views.search, name='search'),
]




