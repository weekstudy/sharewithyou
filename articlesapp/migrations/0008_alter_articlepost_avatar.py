# Generated by Django 3.2.5 on 2021-12-27 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articlesapp', '0007_articlepost_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='avatar',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
