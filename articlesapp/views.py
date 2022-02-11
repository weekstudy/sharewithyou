import os
import time
import hashlib
import random
import emoji
import tkinter.messagebox  # 弹窗库
from tkinter import *
import markdown
import emoji
import datetime
# 记得导入！
from PIL import Image

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

# 引入 Q 对象
from sharewithyou.settings import MEDIA_ROOT

from .models import ArticlePost, Category
from .forms import ArticlePostForm
from comment.models import Comment
# 引入评论表单
from comment.forms import CommentForm

from utils.utils import *



EMOJI_LIST = [':speak-no-evil_monkey:', ':monkey_face:', ':monkey:', ':dog_face:', ':dog:', ':poodle:', ':wolf:',
              ':cat_face:', ':grinning_cat:', ':grinning_cat_with_smiling_eyes:', ':pouting_cat:', ':cat:',
              ':tiger_face:', ':tiger:', ':leopard:', ':horse_face:', ':horse:', ':cow_face:', ':ox:',
              ':water_buffalo:', ':cow:', ':pig_face:', ':pig:', ':boar:', ':pig_nose:', ':ram:', ':ewe:', ':goat:',
              ':camel:', ':elephant:', ':mouse_face:', ':mouse:', ':rat:', ':hamster:', ':rabbit_face:', ':rabbit:',
              ':bear:', ':koala:', ':panda:', ':paw_prints:', ':chicken:', ':rooster:', ':hatching_chick:',
              ':baby_chick:', ':front-facing_baby_chick:', ':bird:', ':penguin:', ':frog:', ':crocodile:', ':turtle:',
              ':snake:', ':dragon_face:', ':dragon:', ':spouting_whale:', ':whale:', ':dolphin:', ':fish:',
              ':tropical_fish:', ':blowfish:', ':octopus:', ':spiral_shell:', ':snail:', ':bug:', ':ant:', ':honeybee:',
              ':lady_beetle:', ':butterfly:', ':boy:', ':girl:', ':man:', ':woman:', ':old_man:', ':old_woman:',
              ':baby:', ':person_blond_hair:', ':police_officer:', ':person_with_skullcap:', ':person_wearing_turban:',
              ':construction_worker:', ':princess:', ':guard:', ':Santa_Claus:', ':person_with_veil:', ':baby_angel:',
              ':person_getting_massage:', ':person_getting_haircut:', ':person_frowning:', ':person_pouting:',
              ':person_gesturing_NO:', ':person_gesturing_OK:', ':person_tipping_hand:', ':person_raising_hand:',
              ':person_bowing:', ':bust_in_silhouette:', ':busts_in_silhouette:', ':person_walking:',
              ':person_running:', ':people_with_bunny_ears:', ':woman_dancing:', ':woman_and_man_holding_hands:',
              ':men_holding_hands:', ':women_holding_hands:', ':kiss:', ':couple_with_heart:', ':family:', ':grapes:',
              ':melon:', ':watermelon:', ':tangerine:', ':lemon:', ':banana:', ':pineapple:', ':red_apple:',
              ':green_apple:', ':pear:', ':peach:', ':cherries:', ':strawberry:', ':bouquet:', ':cherry_blossom:',
              ':white_flower:', ':rose:', ':hibiscus:', ':sunflower:', ':blossom:', ':tulip:', ':seedling:',
              ':evergreen_tree:', ':deciduous_tree:', ':palm_tree:', ':cactus:', ':sheaf_of_rice:', ':herb:',
              ':four_leaf_clover:', ':maple_leaf:', ':fallen_leaf:', ':leaf_fluttering_in_wind:'
              ]


def get_cate_articles():
    # 取出所有博客文章
    category = Category.objects.all().order_by('title')
    cate_articles = {}

    for tmp_cate in category:
        # print('====17', cate.title, cate.id)
        tmp_n = len(ArticlePost.objects.filter(column=tmp_cate.id))
        # 主要是为了在目录模板中使用
        cate_articles[tmp_cate.title] = [tmp_cate, tmp_n]

    return cate_articles

def transform_md(request, articles):
    new_articls = []
    for i in articles:
        # print('=====',i.body[:100])
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
    return new_articls


# Create your views here.
def article_list(request):
    # 取出所有博客文章

    cate_articles = get_cate_articles()
    cate_num = len(Category.objects.all())
    tags_num = len(ArticlePost.tags.all())
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    # TODO 这里应该把column转成数字
    tag = request.GET.get('tag')

    article_list = ArticlePost.objects.all()
    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # print('======article_list76',article_list)
    # 标签查询集
    if tag and tag != 'None':
        # 注意Django - taggit中标签过滤的写法：filter(tags__name__in=[tag])，
        # 意思是在tags字段中过滤name为tag的数据条目。赋值的字符串tag用方括号包起来。
        article_list = article_list.filter(tags__name__in=[tag])

        # print('tag and tag !:=======', article_list)
    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    # 优化添加分页
    num = len(article_list)
    search = request.GET.get('search', None)
    # print('================================ss=/=++++++++++', search)
    order = request.GET.get('order')
    order = 'normal'
    # 每页显示 1 篇文章
    article_list = transform_md(request, article_list)
    paginator = Paginator(article_list, 4)
    # 获取 url 中的页码
    page = request.GET.get('page', 1)
    page_num = paginator.num_pages
    if int(page) > page_num:
        page = page_num
    elif int(page) <= 0:
        page = 1
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    context = {'articles': articles,
               'num': num,
               'article_list': article_list,
               'order': order,
               'search': search,
               'column': column,
               'tag': tag,
               'cate_num': cate_num,
               'tags_num': tags_num,
               'cate_articles': cate_articles,
               'page_num': page_num,
               }

    return render(request, 'article/all_articles.html', context)


def show_article(request, title):
    """
    展示文章详情
    :param request:
    :param id:
    :return:
    """

    context = get_context(request)
    url = request.path.strip().split('/')
    # print('id--152---', url)
    # article = ArticlePost.objects.get(id=id)
    article = ArticlePost.objects.get(title=title)
    # 取出文章评论
    comments = Comment.objects.filter(article=article.id)

    for comment in comments:
        comment.critic = emoji.emojize(comment.critic)
        # comment.body = markdown.markdown(comment.body,
        #                                  extensions=[
        #                                      # 包含 缩写、表格等常用扩展
        #                                      'markdown.extensions.extra',
        #                                      # 语法高亮扩展
        #                                      'markdown.extensions.codehilite',
        #                                      'markdown.extensions.toc',
        #                                  ])

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    previous_article = None
    next_article = None
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])

    # 修改 Markdown 语法渲染
    # TODO 在网页中让目录随鼠标向下滑动而滑动
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    # 因为文章倒序排列
    next_article = ArticlePost.objects.filter(id__gt=article.id).last()
    previous_article = ArticlePost.objects.filter(id__lt=article.id).last()
    # TODO 为啥要实例化
    comment_form = CommentForm()

    context['previous_article'] = previous_article
    context['article'] = article
    context['next_article'] = next_article
    context['toc'] = md.toc
    context['comments'] = comments
    context['comment_form'] = comment_form

    # 载入模板，并返回context对象
    return render(request, 'article/show_article.html', context)



def article_create(request):
    # 判断用户是否提交数据
    # cate_articles = get_cate_articles()
    # total = len(ArticlePost.objects.all())
    context = get_context(request)
    if request.method == "POST":
        # 增加 request.FILES
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # TODO如果没有上传图片，为什么会报错？？
        # print('=======209', request.FILES.get('avatar_svg', ''))
        # cover_name = request.FILES.get("pic", None)

        # 将提交的数据赋值到表单实例中
        # article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            # TODO 用这种上传方式，在admin后台不能上传，图片跟保存路径没有绑定
            new_article = article_post_form.save(commit=False)
            # if request.FILES.get('avatar2'):
            #     my_file = request.FILES.get('avatar2')
            #     tt = time.strftime("%Y-%m-%d", time.localtime())
            #     filename = get_name() + '.' + my_file.name.split('.').pop()
            #     new_article.avatar = os.path.join('article', tt, filename)
            #     save_dir = os.path.join(MEDIA_ROOT, 'article', tt)
            #     if not os.path.exists(save_dir):
            #         os.makedirs(save_dir)
            #     filename = os.path.join(save_dir, filename)
            #     print('=========229', filename, len(filename))
            #
            #     # new_article.avatar = my_file.name
            #     destination = open(filename, 'wb+')  # 打开特定的文件进行二进制的写操作
            #     for chunk in my_file.chunks():  # 分块写入文件
            #         destination.write(chunk)
            #     destination.close()
            # else:
            #     new_article.avatar = ''

            # 处理类别的
            if request.POST['column'] != 'none':
                new_article.column = Category.objects.get(id=request.POST['column'])
                # 处理类别的
            # if request.FILES.get('avatar') is None:
            #     print('=======225', request.FILES.get('avatar'))
            #     new_article.avatar.url = ''
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=1)
            # 将新文章保存到数据库中
            new_article.save()

            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("articlesapp:articles")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 增加类别
        columns = Category.objects.all()
        # 赋值上下文
        context['article_post_form'] = article_post_form,
        context['columns'] = columns

        # 返回模板
        return render(request, 'article/create.html', context)

# 删文章
def article_delete(request, title):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(title=title)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权删除这篇文章。")

    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("articlesapp:articles")


# 更新文章
def article_update(request, title):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    cate_articles = get_cate_articles()
    total = len(ArticlePost.objects.all())
    # tmp_context = get_context(request)

    # 获取需要修改的具体文章对象
    # article = ArticlePost.objects.get(id=id)
    article = ArticlePost.objects.get(title=title)
    orig_avatar = article.avatar_svg
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 新增处理类别的代码
            if request.POST['column'] != 'none':
                article.column = Category.objects.get(id=request.POST['column'])
            else:
                article.column = None
            # 保存新写入的 title、body 数据并保存
            # tmp = article_post_form.save(commit=False)
            article.title = request.POST['title']
            article.body = request.POST['body']
            new_avatar = request.FILES.get('avatar_svg')
            if new_avatar is not None:
                # 这个是把数据块赋值了吗？？
                article.avatar_svg = request.FILES.get('avatar_svg')
            else:
                article.avatar_svg = orig_avatar
            # print('=====330', request.POST.get('tags'))
            # TODO 修改标签感觉要考虑是中文分割符还是英文分割符
            article.tags.set(request.POST.get('tags').split(','), clear=True)
            # new_article.author = User.objects.get(id=1)
            # print('=======329', request.FILES.get('avatar_svg', ''))
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("articlesapp:show_article", title=article.title)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 类别
        columns = Category.objects.all()
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article,
                   'article_post_form': article_post_form,
                   'total': total,
                   'columns': columns,
                   'tags': ','.join([x for x in article.tags.names()]),
                   'cate_articles': cate_articles,
                   }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


def search(request):
    return render(request, 'search.html')


def upload(request):
    """
    上传图片文件，
    :param request:
    :return:
    """
    context = {'success': True}
    if request.method == "GET":  # 请求
        return render(request, 'test/test_upload.html', )
    elif request.method == "POST":
        # FILES只接收上传信息？？
        my_file = request.FILES.get("pic", None)  # 获取上传的文件，如果没有文件，则默认为None
        # print('my_file.name', my_file.name)
        # print('myfile', my_file)
        # print(type(my_file))
        # # 普通数据还是用POST
        # print(request.POST.get('title'))
        # print(request.POST.get('title'))
        if not my_file:
            return HttpResponse("no files for upload!")
        # destination=open(os.path.join('upload',myFile.name),'wb+')
        filename = get_name() + '.' + my_file.name.split('.').pop()
        save_dir = os.path.join(MEDIA_ROOT, 'test')
        filename = os.path.join(save_dir, filename)
        destination = open(filename, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in my_file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        # tkinter.messagebox.showinfo('提示', '登录成功')
        # mainloop()
        # 这里应该要数据库里面存在了才能设置上传成功
        if filename in os.listdir(save_dir):
            context = {'success': True, 'title': request.POST.get('title'), 'filename': my_file.name}
    else:
        context = {'success': False}

    # messages.success(request,"哈哈哈哈")
    return render(request, 'test/test_upload.html', context)


def get_name():
    md5 = hashlib.md5()
    md5.update(bytes(str(time.perf_counter()), encoding='utf8'))
    # md5 = hashlib.md5()
    # s = "password" + "salt"
    # md5.update(s.encode())
    # md5.hexdigest()
    # 'b305cadbb3bce54f3aa59c64fec00dea'
    return md5.hexdigest()
