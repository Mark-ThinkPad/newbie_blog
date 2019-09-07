from django.contrib import admin
from MyBlog.models import *

# Article Model Admin
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['url_suffix', 'title', 'show_authors', 'show_tags', 'show_categories', 'year', 'month', 'day', 'upload_time', 'edited_time', 'top', 'click', 'md_file']
    list_filter = ['year', 'month', 'day', 'top']
    list_editable = ['year', 'month', 'day', 'top']
    search_fields = ['url_suffix', 'title']
    filter_horizontal = ['author', 'tags', 'categories']
    ordering = ['-upload_time']

# Author Model Admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author', 'show_articles']

# Tag Model Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'show_articles']

# Category Model Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'show_articles']

# Image Model Admin
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['username', 'image', 'upload_time']
    list_filter = ['username', 'upload_time']
    search_fields = ['username', 'upload_time']
    ordering = ['-upload_time']

# Project Model Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    list_editable = ['url']
    search_fields = ['name', 'url']

# Friend Model Admin
@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'avatar']
    list_editable = ['url', 'avatar']
    search_fields = ['name', 'url']
