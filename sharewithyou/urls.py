"""sharewithyou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf.urls.static import static


from sharewithyou import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # namespace 主要是为了防止不同应用的路由name属性相同，在反向解析时无法解析，
    # 也可以不设置，只要保持name不同就行
    path('', include('homeapp.urls', namespace='homeapp')),
    path('', include('articlesapp.urls', namespace='articlesapp')),
    path('', include('userprofile.urls', namespace='userprofile')),
    # 评论
    path('comment/', include('comment.urls', namespace='comment')),
    path('', include('resourceapp.urls', namespace='resourceapp')),

    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
# url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT})