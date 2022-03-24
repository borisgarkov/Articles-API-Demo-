from django.contrib import admin
from .models import Article


# admin.site.register(Article)

@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_filter = ('title', 'description', 'id')
    list_display = ('title', 'description', 'id')
