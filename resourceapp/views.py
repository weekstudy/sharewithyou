#! python3.8
# -*-coding:utf-8 -*-

from django.shortcuts import render,redirect
from django.http import HttpResponse, StreamingHttpResponse,FileResponse
from .models import Resources
from sharewithyou.settings import MEDIA_URL
from homeapp.views import *

# Create your views here.


def downloads(request):
    context = get_context(request)
    info_by_month_years = recents_month_articles(request)
    context['info_by_month_years'] = info_by_month_years

    url = request.path.strip('/').split('/')
    if len(url) == 1:
        resources = Resources.objects.all()
        for i in resources:
            print(i.name, i.url)
        context['resources'] = resources
        return render(request, 'homeapp/download.html', context)
    elif len(url) == 3:
        # 找出要下载的文件
        res = Resources.objects.get(name=url[2])
        path = res.url

        def file_iterator(file_path, chunk_size=512):
            """
            文件生成器,防止文件过大，导致内存溢出
            :param file_path: 文件绝对路径
            :param chunk_size: 块大小
            :return: 生成器
            """
            with open(file_path, mode='rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        response = StreamingHttpResponse(file_iterator(path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(res.name)
        res.download_count = res.download_count + 1
        res.save()
        # return response
        new_url = '/' + res.url
        # print('=======47====', new_url)
        return redirect(new_url)

def preview(request):
    import json
    # 直接弹出下载框
    # file = open('./media/resources/数学之美第二版.pdf', 'rb')
    # response = HttpResponse(file)
    # response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    # response['Content-Disposition'] = 'attachment;filename="数学之美第二版.pdf"'
    with open('./media/resources/1706-transformer.pdf', 'rb+') as pdf:
        res = pdf.read()
        # print('-===58===',res)
        # response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        # return response
    response = dict()
    # res = Resources.objects.filter(id=4)
    response['status'] = 'success'
    response['data'] = list(res)
    return HttpResponse(json.dumps(response))
    # return render(request, 'downloads/download.html',)

def pre_pdf(request):
  file=open('./media/resources/数学之美第二版.pdf', 'rb')
  response =FileResponse(file)
  response['Content-Type'] = 'application/octet-stream'
  response['Content-Disposition'] = 'attachment;filename="数学之美第二版.pdf"'
  test = Resources.objects.filter(url='media/resources/1706-transformer.pdf')

  return response


# def preview(request):
#     file = open('./media/resources/数学之美第二版.pdf', 'rb')
#     response = FileResponse(file)
#     response['Content-Type'] = 'application/octet-stream'
#     response['Content-Disposition'] = 'attachment;filename="数学之美第二版.pdf"'
#
#     context = {'response': response}
#     return render(request,'downloads/download.html', context)


def uploads(request):
    return HttpResponse('暂时还未完成上传文件功能')
