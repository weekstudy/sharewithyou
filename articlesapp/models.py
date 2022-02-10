import os
from PIL import Image
from django.http import Http404
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse,path

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

# Create your models here.

def user_directory_path(instance, filename):
    """
    用来设置上传图片路径
    :param instance:
    :param filename:
    :return:
    """
    ext = filename.split('.').pop()
    filename = '{0}{1}.{2}'.format(instance.name, instance.identity_card, ext)
    return os.path.join(instance.major.name, filename)


class Category(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    # 获取
    def get_absolute_url(self):
        # url = 'categories/'+self.title+
        # return path(url)
        # return reverse('homeapp:category_detail')
        if self.title == 'Algorithm':
            return reverse('homeapp:'+self.title)
            # return reverse(url)
        elif self.title == 'Deep Learning':
            return reverse('homeapp:Deep Learning')
        elif self.title == 'Django':
            return reverse('homeapp:Django')
        elif self.title == 'Face Recognition':
            return reverse('homeapp:Face Recognition')
        elif self.title == 'Linux':
            return reverse('homeapp:Linux')
        elif self.title == 'Machine Learning':
            return reverse('homeapp:Machine Learning')
        elif self.title == 'Object Detection':
            return reverse('homeapp:Object Detection')
        elif self.title == 'Other':
            return reverse('homeapp:Other')
        elif self.title == 'Python':
            return reverse('homeapp:Python')
        else:
            return Http404('当前目录没有')


class ArticlePost(models.Model):
    # 应该要有封面图片的路径
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # 这里改为富文本编辑器
    body = models.TextField()
    # body = RichTextField()

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    # 增加一个浏览量字段
    total_views = models.PositiveIntegerField(default=0)

    # 文章栏目的 “一对多” 外键:一篇文章只有一个类别，一个类别对应多个文章？？
    #  TODO 可以多对多
    column = models.ForeignKey(Category, null=True, blank=True,
                               on_delete=models.CASCADE, related_name='article')

    # 文章标签
    tags = TaggableManager(blank=True)

    # 文章标题图
    # 不能接受svg
    avatar_svg = models.FileField(upload_to='article_svg/%Y%m%d/', blank=True)
    # 多个标签最好用英文逗号
    # avatar_img = models.ImageField(upload_to='article_img/%Y%m%d/', blank=True)
    # avatar = models.CharField(max_length=200, blank=True, default='')

    @property
    def avatar_url(self):
        # if self.avatar_img and hasattr(self.avatar_img, 'url'):
        #     return self.avatar_img.url
        if self.avatar_svg and hasattr(self.avatar_svg, 'url'):
            return self.avatar_svg.url

    # # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        # 这里应该进行判断，如果文件是svg,直接保存
        # print('======73', *args, **kwargs)
        article = super(ArticlePost, self).save(*args, **kwargs)
        # # # 固定宽度缩放图片大小
        # if self.avatar_img.url.split('.')[-1].lower() != 'svg':
        #     if self.avatar_img and not kwargs.get('update_fields'):
        #         image = Image.open(self.avatar_img)
        #         (x, y) = image.size
        #         new_x = 400
        #         new_y = int(new_x * (y / x))
        #         resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
        #         resized_image.save(self.avatar_img.path)
        return article

    # 是在用户评论时调用，用来获取文章地址，进行重定向
    def get_absolute_url(self):
        return reverse('articlesapp:show_article', args=[self.id])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
