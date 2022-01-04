# Generated by Django 3.2.5 on 2021-12-30 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_created=True, auto_now=True)),
                ('create_time', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=128, verbose_name='资源名称')),
                ('url', models.CharField(max_length=512, verbose_name='下载链接')),
                ('download_count', models.IntegerField(default='0', verbose_name='下载次数')),
            ],
            options={
                'verbose_name': '资源链接',
                'verbose_name_plural': '资源链接',
                'db_table': 't_resource',
            },
        ),
    ]
