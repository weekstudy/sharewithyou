# Generated by Django 3.2.5 on 2021-12-27 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articlesapp', '0006_remove_articlepost_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='article/%Y%m%d/'),
        ),
    ]
