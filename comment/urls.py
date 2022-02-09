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
    # 新增代码，处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
]