# Generated by Django 3.2.5 on 2021-12-27 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articlesapp', '0009_remove_articlepost_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='avatar',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
