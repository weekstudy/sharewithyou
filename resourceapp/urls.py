#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
@author:Jaunezhou
@file:urls.py
@NAME:sharewithyou
@time:2021/12/30
@IDE: PyCharm
 
"""

from django.urls import path, re_path

from . import views
app_name = 'resourceapp'

urlpatterns = [
    path('downloads/', views.downloads, name='downloads'),
    # path('downloads/1706-transformer.pdf', views.preview, name='pre_pdf'),
    path('uploads/', views.uploads, name='uploads'),
    # re_path(r'downloads/图像分割论文.JPG/', views.downloads, name='3'),
    # re_path(r'downloads/数学之美第二版.pdf/', views.downloads, name='2'),
    # re_path(r'downloads/emoji.txt/', views.downloads, name='emoji.txt'),
    re_path(r'downloads/.*?', views.downloads, name='res'),
    # re_path(r'downloads/resources/.*?', views.preview, name='preview'),

]

