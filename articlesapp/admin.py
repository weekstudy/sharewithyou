from django.contrib import admin
from .models import ArticlePost, Category
# from .models import Tag
# from .models import Category
# from .models import Cover


# Register your models here.
admin.site.register(ArticlePost)
# admin.site.register(Tag)
admin.site.register(Category)
# admin.site.register(Cover)
