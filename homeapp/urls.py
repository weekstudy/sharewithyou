#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
@author:Jaunezhou
@file:urls.py
@NAME:sharewithyou
@time:2021/12/20
@IDE: PyCharm
 
"""

from django.urls import path, re_path

from . import views
# from homeapp import views

app_name = 'homeapp'
# 如果这里加了app_name.
# 那么在html中使用url解析时需要加homeapp:home

urlpatterns = [
    path('', views.home, name='home'),
    path('js/', views.js, name='js'),
    path('archives/', views.archives, name='archives'),
    re_path(r'^archives/[0-9]{4}/[0-9]*', views.archives_by_year_month, name='archives_by_year_month'),
    # re_path(r'^archives/[0-9]{4}/[0-9]+/$', views.archives_by_month, name='archives_by_month'),


    path('categories/', views.categories, name='categories'),
    # 这个路由其实可以用正则来写,但是在单独逆向解析url怎么办
    re_path(r'^categories/.*?', views.category_detail, name='category_detail'),
    # path('categories/Algorithm/', views.algorithm, name='Algorithm'),
    # path('categories/Deep_Learning/', views.deep_learning, name='Deep Learning'),
    # path('categories/Django/', views.django, name='Django'),
    # path('categories/Face_Recognition/', views.face_recognition, name='Face Recognition'),
    # path('categories/Linux/', views.linux, name='Linux'),
    # path('categories/Machine_Learning/', views.machine_learning, name='Machine Learning'),
    # path('categories/Object_Detection/', views.object_detection, name='Object Detection'),
    # path('categories/Other/', views.other, name='Other'),
    # path('categories/Python/', views.python, name='Python'),
    path('tags/', views.tags, name='tags'),
    re_path(r'^tags/.*?', views.tag_detail, name='tag_detail'),
    path('about/', views.about, name='about'),
]
