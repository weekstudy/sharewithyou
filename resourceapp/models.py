from django.db import models
from django.urls import reverse
# Create your models here.


class Resources(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name=u"资源名称")
    url = models.CharField(max_length=512, verbose_name="下载链接")
    url2 = models.FileField(upload_to='resources/', default='', verbose_name="下载链接2")
    create_time = models.DateTimeField(auto_created=True)
    update_time = models.DateTimeField(auto_created=True, auto_now=True)
    download_count = models.IntegerField(default='0', verbose_name="下载次数")

    class Meta:
        db_table = 't_resource'
        verbose_name = '资源链接'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)






