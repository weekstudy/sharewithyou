#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
@author:Jaunezhou
@file:utils.py
@NAME:sharewithyou
@time:2022/01/04
@IDE: PyCharm
 
"""

from django.core.paginator import Paginator
from django.db.models import Q, Count
from articlesapp.models import ArticlePost, Category, TaggableManager

MONTH = {'1': 'January', '2': 'February', '3': 'March', '4': 'April',
         '5': 'May', '6': 'June', '7': 'July', '8': 'August',
         '9': 'September', '10': 'October', '11': 'November', '12': 'December'}


def get_context(request):
    article_list = ArticlePost.objects.all()
    # 得到每个tag对应的文章数
    all_tags = ArticlePost.tags.all()
    # article_list = article_list.filter(tags__name__in=[tag])
    # all_articles = ArticlePost.objects.all()
    per_tag_articles = {}

    for tmp_tag in all_tags:
        # print('======427==', tmp_tag)
        tag_articles = article_list.filter(tags__name__in=[tmp_tag])
        per_tag_articles[str(tmp_tag)] = [len(tag_articles), tag_articles, ]

    per_tag_articles['other'] = []
    tmp_c = 0
    for art in article_list:
        if len(art.tags.all()) == 0:
            tmp_c += 1
            per_tag_articles['other'].append(art)
    per_tag_articles['other'].insert(0, tmp_c)
    # [tag:[文章数]]
    # context['tags_articles'] = per_tag_articles

    category = Category.objects.all().order_by('title')
    cate_articles = {}
    for tmp_cate in category:
        # print('====17', cate.title, cate.id)
        tmp_n = len(ArticlePost.objects.filter(column=tmp_cate.id))
        tmp_name = tmp_cate.title.replace(' ', '_')
        cate_articles[tmp_cate.title] = [tmp_cate, tmp_n, tmp_name]

    cate_num = len(Category.objects.all())
    tags_num = len(ArticlePost.tags.all())

    recent_articles = article_list[:5]
    num = len(article_list)

    search = request.GET.get('search', None)
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        article_list = ArticlePost.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''
        article_list = ArticlePost.objects.all()
    order = 'normal'
    # 每页显示 6 篇文章
    paginator = Paginator(article_list, 6)
    # 获取 url 中的页码
    page = request.GET.get('page', 1)
    page_num = paginator.num_pages
    if int(page) > page_num:
        page = page_num
    elif int(page) <= 0:
        page = 1
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    info_by_month_years = recents_month_articles(request)

    context = {'cur_page_articles': None,  # 中间栏显示的内容 不同的页面不一样
               'num': num,  # 总的文章数
               'cate_num': cate_num,  # 总的目录数
               'tags_num': tags_num,  # 总的标签数
               'article_list': article_list,  # 所有的文章
               'order': order,  # 排序
               'search': search,  # 搜索关键字
               'recent_articles': recent_articles,  # 最近的5篇文章
               'category': category,  # 所有目录名字
               'cate_articles': cate_articles,  # 字典{column:[Queryset,文章数,url的名字}
               'info_by_month_years': info_by_month_years,
               'tags_articles': per_tag_articles,  # 字典{tagname:[文章数,Queryset]}
               }  # 保存每个类别有多少文章的列表

    return context

def recents_month_articles(request):
    """
    选出最近10个月的文章
    :param request:
    :return:
    """
    all_articles = ArticlePost.objects.all()
    articles_by_year, articles_by_month_years = archives_order_by_year(all_articles)

    tmp_articles_info = {}
    # print('=======141======', articles_by_month_years)
    i = 0
    # n = len(articles_by_month_years)
    for key in articles_by_month_years.keys():
        if i < 10:
            tmp = key.split(' ')
            # print('======', i, tmp)
            assert len(tmp) == 2
            tmp_month, tmp_year = tmp[0], tmp[1]
            # tmp_articles_info[MONTH[tmp_month]] = [tmp_month, tmp_year, len(articles_by_month_years[key])]
            tmp_articles_info[key] = [MONTH[tmp_month], tmp_month, tmp_year, len(articles_by_month_years[key])]
            i += 1

    # context['articles_by_month_years'] = tmp_articles
    # print('=======152======', tmp_articles_info)
    tmp_list = sorted(tmp_articles_info.items(), key=lambda x: (int(x[1][2]), int(x[1][1])), reverse=True)
    res = {}
    for item in tmp_list:
        res[item[0]] = item[1]
    # print('======166=====',res)
    return res

def archives_order_by_year(cur_articles):
    # all_articles = ArticlePost.objects.all().order_by('-created')
    all_articles = cur_articles
    years = {}
    month_years = {}
    for t in all_articles:
        if t.created.year not in years.keys():
            # years[t.created.year] = 1
            years[t.created.year] = [t, ]
        else:
            # years[t.created.year] += 1
            years[t.created.year].append(t)
        month_year = str(t.created.month) + ' ' + str(t.created.year)
        # print('====97=', t.created.month, t.created.year)
        if month_year not in month_years.keys():
            # month_years[month_year] = 1
            month_years[month_year] = [t, ]
        else:
            # month_years[month_year] += 1
            month_years[month_year].append(t)

    # 感觉应该在文章数据库里设置一个年份外键，月份外键

    # 返回一个字典：{years:[article1,article2]}
    return years, month_years

