from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear, TruncDay
from django.db.models.functions import ExtractYear
from django.urls import path, re_path
import markdown

from articlesapp.models import ArticlePost, Category, TaggableManager

from articlesapp.views import article_list

MONTH = {'1': 'January', '2': 'February', '3': 'March', '4': 'April',
         '5': 'May', '6': 'June', '7': 'July', '8': 'August',
         '9': 'September', '10': 'October', '11': 'November', '12': 'December'}


# Create your views here.

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


def get_recent_years_articles(request, a=2, y=4):
    all_articles = ArticlePost.objects.all().order_by('-created')
    articles_by_year, articles_by_month_years = archives_order_by_year(all_articles)
    res_art = []
    if len(articles_by_year) >= y:
        for key in list(articles_by_year.keys())[:y]:
            if len(articles_by_year[key]) >= a:
                res_art += articles_by_year[key][:a]
            else:
                res_art += articles_by_year[key]
    else:
        for key in articles_by_year.keys():
            if len(articles_by_year[key]) >= a:
                res_art += articles_by_year[key][:a]
            else:
                res_art += articles_by_year[key]

    return res_art


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


def filter_by_request(request):
    """
    返回过滤后的所有文章
    :param request:
    :return:
    """

    all_articles = ArticlePost.objects.all()
    articles_by_year, articles_by_month_years = archives_order_by_year(all_articles)

    # 显示每年的最新的5篇文章，
    # 两种case.第一种某年不止5篇，第二种某年小于5篇
    # {years: [article1, article2]}
    # 得到每年的全部文章
    tmp_articles = []
    # 取出每年的5篇文章，不足的年份全取
    for y, art in articles_by_year.items():
        if len(art) > 2:
            tmp_articles += art[:2]
        else:
            tmp_articles += art
    # 将取出来的进行分页
    paginator = Paginator(tmp_articles, 8)
    # 获取 url 中的页码
    page = request.GET.get('page', 1)
    page_num = paginator.num_pages
    if int(page) > page_num:
        page = page_num
    elif int(page) <= 0:
        page = 1
    # 得到当前页的文章数
    cur_articles = paginator.get_page(page)

    page_articles = cur_articles
    cur_articles_queryset = []
    for i in page_articles:
        cur_articles_queryset.append(i)
    # 得到当前页的年份:文章数
    cur_articles_by_year, cur_articles_by_month_years = archives_order_by_year(cur_articles_queryset)
    context = get_context(request)
    context['cur_articles_by_year'] = cur_articles_by_year
    context['cur_articles_by_month_years'] = cur_articles_by_month_years
    context['articles_by_year'] = articles_by_year
    context['articles_by_month_years'] = articles_by_month_years
    context['page_articles'] = page_articles
    context['page_num'] = page_num
    context['info_by_month_years'] = recents_month_articles(request)
    return context


def archives(request):
    # 返回字典：{years: [article1, article2]}
    # all_articles = ArticlePost.objects.all()
    # TODO 显示每年的最新的2篇文章，一页显示4年
    context = filter_by_request(request)
    search = request.GET.get('search', None)
    if search:
        # TODO 如果有search，可以在所有文章或者某一年或者某一年的某一个月搜索
        all_articles = ArticlePost.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
        cur_page_articles, _ = get_paginator(request, all_articles, 6)
        context['cur_page_articles'] = cur_page_articles
        return render(request, "homeapp/index.html", context)
    else:
        # print('=====',context)
        return render(request, "homeapp/archives.html", context)


def archives_by_year_month(request):
    url = request.path.strip('/').split('/')
    all_articles = ArticlePost.objects.all()
    articles_by_year, articles_by_month_years = archives_order_by_year(all_articles)
    context = get_context(request)
    # info_by_month_years = recents_month_articles(request)
    cur_year = None
    cur_month = None
    tmp_articles = None
    if len(url) == 2:
        cur_year = url[1]
        tmp_articles = articles_by_year.get(int(cur_year), None)
        cur_month = ''
    elif len(url) == 3:
        cur_year = url[1]
        cur_month = int(url[2])
        context['cur_month'] = str(url[2])
        if cur_month <= 0:
            cur_month = 1
        elif cur_month > 12:
            cur_month = 12
        tmp_articles = articles_by_month_years.get(str(cur_month)+' '+str(cur_year), None)
        # print('=====258=====', tmp_articles)
    if tmp_articles is None:
        return Http404('当前未发表文章，请看看其他的吧')
    cur_page_articles, page_num = get_paginator(request, tmp_articles, 1)
    # print('=====262===', cur_page_articles)
    # paginator = Paginator(tmp_articles, 10)
    # # 获取 url 中的页码
    # page = request.GET.get('page', 1)
    # page_num = paginator.num_pages
    # if int(page) > page_num:
    #     page = page_num
    # elif int(page) <= 0:
    #     page = 1
    # # 得到当前页的文章数
    # cur_articles = paginator.get_page(page)
    # page_articles = cur_articles
    # context['info_by_month_years'] = info_by_month_years
    # context['page_articles'] = cur_articles
    # print('=====275====', context['info_by_month_years'])
    context['cur_page_articles'] = cur_page_articles
    context['cur_year'] = cur_year
    context['page_num'] = page_num
    context['year_month'] = MONTH.get(str(cur_month), '')+' ' + cur_year
    return render(request, "homeapp/archives_detail.html", context)


def archives_by_month(request):
    url = request.path.strip('/').split('/')
    assert len(url) == 3
    month_year = str(url[2]) + ' ' + str(url[1])
    context = filter_by_request(request)
    # 显示最近10个月的文章
    info_by_month_years = recents_month_articles(request)
    all_articles = ArticlePost.objects.all()
    articles_by_year, articles_by_month_years = archives_order_by_year(all_articles)
    context['info_by_month_years'] = info_by_month_years
    tmp_articles = articles_by_month_years.get(month_year, None)
    paginator = Paginator(tmp_articles, 10)
    # 获取 url 中的页码
    page = request.GET.get('page', 1)
    page_num = paginator.num_pages
    if int(page) > page_num:
        page = page_num
    elif int(page) <= 0:
        page = 1
    cur_articles = paginator.get_page(page)
    page_articles = cur_articles
    context = get_context(request)
    context['page_articles'] = page_articles
    context['cur_year'] = str(url[1])
    context['cur_month'] = str(url[2])
    context['month_year'] = MONTH[str(url[2])] + ' ' + str(url[1])
    context['page_num'] = page_num
    context['info_by_month_years'] = info_by_month_years

    return render(request, "homeapp/archives_detail.html", context)


def get_paginator(request, articles, page_per=5):
    """
    用来分页，主要是用来中间栏显示的内容
    :param request:
    :param articles:
    :param page_per:
    :return:
    """
    new_articls=[]
    for i in articles:

        i.body = markdown.markdown(i.body[:100],
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
        # i.body = md.convert(article.body)

        new_articls.append(i)

    paginator = Paginator(new_articls, page_per)

    # 获取 url 中的页码
    page = request.GET.get('page', 1)
    page_num = paginator.num_pages
    if int(page) > page_num:
        page = page_num
    elif int(page) <= 0:
        page = 1
    cur_articles = paginator.get_page(page)
    return cur_articles, page_num


def get_params(request):
    search = request.GET.get('search', None)
    order = request.GET.get('order', None)
    column = request.GET.get('column', None)
    tag = request.GET.get('tag', None)
    return search, order, column, tag


def home(request):
    context = get_context(request)

    all_articles = ArticlePost.objects.all()
    search = request.GET.get('search', None)
    cur_page_articles, _ = get_paginator(request, all_articles, 6)
    context['cur_page_articles'] = cur_page_articles


    if search:
        context = search_keyword(request)
    return render(request, "homeapp/index.html", context)


def categories(request):
    context = get_context(request)

    search, order, column, tag = get_params(request)
    if search:
        context = search_keyword(request)
        return render(request, "homeapp/index.html", context)
    else:
        # print('=====583==', context)
        return render(request, "homeapp/categories.html", context)


def category_detail(request):
    url = request.path
    url_list = url.strip('/').split('/')
    assert len(url_list) == 2
    # 得到当前的分类
    cur_category = url_list[1].replace('_', ' ')
    cur_category_q = Category.objects.filter(title=cur_category)
    assert len(cur_category_q) == 1
    cur_category_id = cur_category_q[0].id
    # print('=====598=====', cur_category)
    # 公共区域的数据
    context = get_context(request)
    cur_articles = ArticlePost.objects.filter(column=cur_category_id)

    cur_page_articles, _ = get_paginator(request, cur_articles, page_per=1)
    # print('======611======', cur_page_articles)
    context['cur_page_articles'] = cur_page_articles
    context['column'] = cur_category
    search, order, column, tag = get_params(request)
    if search:
        context = search_keyword(request)
        return render(request, "homeapp/index.html", context)
    else:
        return render(request, "homeapp/category_detail.html", context)


def tag_detail(request):
    """
    过滤出含tag的文章
    :param request:
    :return:
    """
    url = request.path
    url_list = url.strip('/').split('/')
    assert len(url_list) == 2
    tag_name = url_list[1]
    context = get_context(request)
    if tag_name == 'other':
        cur_articles = context['tags_articles'][tag_name][1:]
    else:
        cur_articles = context['tags_articles'][tag_name][1:][0]
    cur_page_articles, _ = get_paginator(request, cur_articles, page_per=10)
    context['cur_page_articles'] = cur_page_articles
    if tag_name.isalpha():
        tag_name = tag_name[0].upper()+tag_name[1:]
    context['tag_name'] = tag_name
    search, order, column, tag = get_params(request)
    if search:
        context = search_keyword(request)
        return render(request, "homeapp/index.html", context)
    else:
        return render(request, 'homeapp/tag_detail.html', context)


def tags(request):

    context = get_context(request)

    search, order, column, tag = get_params(request)
    # search = request.GET.get('search', None)
    if search:
        context = search_keyword(request)
        return render(request, "homeapp/index.html", context)
    else:
        return render(request, "homeapp/tags.html", context)

def about(request):
    context = get_context(request)
    search, order, column, tag = get_params(request)
    if search:
        context = search_keyword(request)
        return render(request, "homeapp/index.html", context)
    else:
        return render(request, "homeapp/about.html", context)


def search_keyword(request):
    context = get_context(request)
    search, order, column, tag = get_params(request)
    all_articles = ArticlePost.objects.filter(
        Q(title__icontains=search) |
        Q(body__icontains=search)
    )
    cur_page_articles, _ = get_paginator(request, all_articles, 6)
    context['cur_page_articles'] = cur_page_articles
    return context


def download(request):
    return render(request, 'homeapp/download.html')


def js(request):
    return render(request, 'test/js.html')