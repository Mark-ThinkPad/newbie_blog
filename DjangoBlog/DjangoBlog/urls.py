"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from MyBlog.views import *
from DjangoBlog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 自定义页面
    path('', index, name='index'),
    path('admin_login/', admin_login, name='admin_login'),
    path('add_article/', add_article, name='add_article'),
    path('articles/<int:year>/<int:month>/<int:day>/<slug:suffix>/', article_detail, name='article_detail'),
    path('edit/<int:year>/<int:month>/<int:day>/<slug:suffix>/', online_edit, name='edit'),
    path('add_image/', add_image, name='add_image'),
    path('images/', images, name='images'),
    path('archive/', archive, name='archive'),
    path('tags/', tag, name='tags'),
    path('tags/<slug:slug>/', tag_detail, name='tag_detail'),
    path('categories/', category, name='categories'),
    path('categories/<slug:slug>/', category_detail, name='category_detail'),
    path('authors/', author, name='authors'),
    path('authors/<slug:slug>/', author_detail, name='author_detail'),
    path('about/', about, name='about'),
    path('books/', books, name='books'),
    # 后端API
    path('api_login/', api_login, name='api_login'),
    path('api_logout/', api_logout, name='api_logout'),
    path('api_add_article/', api_add_article, name='api_add_article'),
    path('api_edit_article/', api_edit_article, name='api_edit_article'),
    path('api_add_info/', api_add_info, name='api_add_info'),
    path('api_add_images/', api_add_images, name='api_add_images'),
]

# 配置静态页面
# https://docs.djangoproject.com/zh-hans/2.1/ref/urls/#static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)