from django.shortcuts import render
from MyBlog.models import *
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseServerError, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import time

# Home Page
@require_GET
def index(request):
    author_list = Author.objects.all()
    tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
    category_list = Category.objects.exclude(category='about').exclude(category='book_list')
    projects = Project.objects.all()
    friends = Friend.objects.all()

    articles_normal = Article.objects.exclude(url_suffix='about').exclude(url_suffix='book_list').filter(
        top=False).order_by('-year', '-month', '-day', '-upload_time')
    articles_top = Article.objects.exclude(url_suffix='about').exclude(url_suffix='book_list').filter(
        top=True).order_by('-year', '-month', '-day', '-upload_time')

    paginator = Paginator(articles_normal, 10)
    page = request.GET.get('page')
    content = paginator.get_page(page)

    return render(request, 'index.html', {
        'author_list': author_list,
        'tag_list': tag_list,
        'category_list': category_list,
        'projects': projects,
        'friends': friends,
        'articles_top': articles_top,
        'content': content,
    })


# Admin Login Page
@require_GET
def admin_login(request):
    return render(request, 'login.html')


# Article Upload Page
@require_GET
@login_required(redirect_field_name='', login_url='/admin_login/')
def add_article(request):
    author_list = Author.objects.all()
    tag_list = Tag.objects.all()
    category_list = Category.objects.all()

    return render(request, 'add_article.html', {
        'author_list': author_list,
        'tag_list': tag_list,
        'category_list': category_list,
    })


# Article Detail Page (Dynamic)
@require_GET
def article_detail(request, year, month, day, suffix):
    try:
        a = Article.objects.get(year=year, month=month, day=day, url_suffix=suffix)
        a.click_increase()

        author_list = Author.objects.all()
        tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
        category_list = Category.objects.exclude(category='about').exclude(category='book_list')
        projects = Project.objects.all()
        friends = Friend.objects.all()

        return render(request, 'article_detail.html', {
            'a': a,
            'author_list': author_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'projects': projects,
            'friends': friends,
        })
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    except MultipleObjectsReturned:
        return HttpResponseServerError()


# Online Edit Page (Dynamic)
@require_GET
@login_required(redirect_field_name='', login_url='/admin_login/')
def online_edit(request, year, month, day, suffix):
    try:
        a = Article.objects.get(year=year, month=month, day=day, url_suffix=suffix)

        author_list = Author.objects.all()
        tag_list = Tag.objects.all()
        category_list = Category.objects.all()

        return render(request, 'online_edit.html', {
            'a': a,
            'author_list': author_list,
            'tag_list': tag_list,
            'category_list': category_list,
        })
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    except MultipleObjectsReturned:
        return HttpResponseServerError()


# Image Upload Page
@require_GET
@login_required(redirect_field_name='', login_url='/admin_login/')
def add_image(request):
    return render(request, 'add_image.html')


# Images Display Page
@require_GET
@login_required(redirect_field_name='', login_url='/admin_login/')
def images(request):
    imgs = Image.objects.all()
    return render(request, 'images.html', {'images': imgs})


# Archive Page
@require_GET
def archive(request):
    articles = Article.objects.exclude(url_suffix='about').exclude(url_suffix='book_list').order_by(
        '-year', '-month', '-day', '-upload_time')

    author_list = Author.objects.all()
    tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
    category_list = Category.objects.exclude(category='about').exclude(category='book_list')
    projects = Project.objects.all()
    friends = Friend.objects.all()

    return render(request, 'archive.html', {
        'articles': articles,
        'author_list': author_list,
        'tag_list': tag_list,
        'category_list': category_list,
        'projects': projects,
        'friends': friends,
    })


# Tag Page
@require_GET
def tag(request):
    author_list = Author.objects.all()
    tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
    category_list = Category.objects.exclude(category='about').exclude(category='book_list')
    projects = Project.objects.all()
    friends = Friend.objects.all()

    return render(request, 'tag.html', {
        'author_list': author_list,
        'tag_list': tag_list,
        'category_list': category_list,
        'projects': projects,
        'friends': friends,
    })


# Tag Detail Page (Dynamic)
@require_GET
def tag_detail(request, slug):
    try:
        author_list = Author.objects.all()
        tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
        category_list = Category.objects.exclude(category='about').exclude(category='book_list')
        projects = Project.objects.all()
        friends = Friend.objects.all()

        t = Tag.objects.get(tag=slug)
        articles = t.article_set.order_by('-year', '-month', '-day')

        return render(request, 'tag_detail.html', {
            'author_list': author_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'projects': projects,
            'friends': friends,
            't': t,
            'articles': articles,
        })
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    except MultipleObjectsReturned:
        return HttpResponseServerError()


# Category Page
@require_GET
def category(request):
    author_list = Author.objects.all()
    tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
    category_list = Category.objects.exclude(category='about').exclude(category='book_list')
    projects = Project.objects.all()
    friends = Friend.objects.all()

    return render(request, 'category.html', {
        'author_list': author_list,
        'tag_list': tag_list,
        'category_list': category_list,
        'projects': projects,
        'friends': friends,
    })


# Category Detail Page (Dynamic)
@require_GET
def category_detail(request, slug):
    try:
        author_list = Author.objects.all()
        tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
        category_list = Category.objects.exclude(category='about').exclude(category='book_list')
        projects = Project.objects.all()
        friends = Friend.objects.all()

        c = Category.objects.get(category=slug)
        articles = c.article_set.order_by('-year', '-month', '-day')

        return render(request, 'category_detail.html', {
            'author_list': author_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'projects': projects,
            'friends': friends,
            'c': c,
            'articles': articles,
        })
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    except MultipleObjectsReturned:
        return HttpResponseServerError()


# Author Page
@require_GET
def author(request):
    author_list = Author.objects.all()
    tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
    category_list = Category.objects.exclude(category='about').exclude(category='book_list')
    projects = Project.objects.all()
    friends = Friend.objects.all()

    return render(request, 'author.html', {
        'author_list': author_list,
        'tag_list': tag_list,
        'category_list': category_list,
        'projects': projects,
        'friends': friends,
    })


# Author Detail Page (Dynamic)
@require_GET
def author_detail(request, slug):
    try:
        author_list = Author.objects.all()
        tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
        category_list = Category.objects.exclude(category='about').exclude(category='book_list')
        projects = Project.objects.all()
        friends = Friend.objects.all()

        au = Author.objects.get(author=slug)
        articles = au.article_set.order_by('-year', '-month', '-day')

        return render(request, 'author_detail.html', {
            'author_list': author_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'projects': projects,
            'friends': friends,
            'au': au,
            'articles': articles,
        })
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    except MultipleObjectsReturned:
        return HttpResponseServerError()


# About Page
@require_GET
def about(request):
    try:
        t = Tag.objects.get(tag='about')
        c = Category.objects.get(category='about')
        a = Article.objects.get(url_suffix='about', tags=t, categories=c)
        a.click_increase()

        author_list = Author.objects.all()
        tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
        category_list = Category.objects.exclude(category='about').exclude(category='book_list')
        projects = Project.objects.all()
        friends = Friend.objects.all()

        return render(request, 'about.html', {
            'a': a,
            'author_list': author_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'projects': projects,
            'friends': friends,
        })
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    except MultipleObjectsReturned:
        return HttpResponseServerError()


# Books (List) Page
@require_GET
def books(request):
    try:
        t = Tag.objects.get(tag='book_list')
        c = Category.objects.get(category='book_list')
        a = Article.objects.get(url_suffix='book_list', categories=c, tags=t)
        a.click_increase()

        cm = Category.objects.get(category='book')
        articles = Article.objects.filter(categories=cm).order_by('-year', '-month', '-day', '-upload_time')

        author_list = Author.objects.all()
        tag_list = Tag.objects.exclude(tag='about').exclude(tag='book_list')
        category_list = Category.objects.exclude(category='about').exclude(category='book_list')
        projects = Project.objects.all()
        friends = Friend.objects.all()

        return render(request, 'books.html', {
            'a': a,
            'articles': articles,
            'author_list': author_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'projects': projects,
            'friends': friends,
        })
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    except MultipleObjectsReturned:
        return HttpResponseServerError()


# API List
# API Login (admin)
@require_POST
@csrf_exempt
def api_login(request):
    if request.is_ajax():
        if request.method == 'POST':
            name = request.POST['username']
            pwd = request.POST['password']
            user = authenticate(username=name, password=pwd)
            if user is not None and user.is_active:
                login(request, user)
                return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': 0})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()


# API Logout (admin)
@require_POST
@csrf_exempt
@login_required(redirect_field_name='', login_url='/admin_login/')
def api_logout(request):
    if request.is_ajax():
        if request.method == 'POST':
            msg = request.POST['msg']
            if msg == 'logout':
                logout(request)
                return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': 0})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()


# API Add Article
@require_POST
@csrf_exempt
@login_required(redirect_field_name='', login_url='/admin_login/')
def api_add_article(request):
    if request.is_ajax():
        if request.method == 'POST':
            # 获取请求数据
            md_code = request.POST['md_code']
            file = request.FILES.get('md_file')
            suffix = request.POST['url_suffix']
            title = request.POST['title']
            authors = request.POST.getlist('authors')
            tags = request.POST.getlist('tags')
            categories = request.POST.getlist('categories')
            top = request.POST['top']
            # 转换为布尔值
            if top == 'true':
                top = True
            elif top == 'false':
                top = False

            # 防止文章重复
            try:
                Article.objects.get(url_suffix=suffix)
                return JsonResponse({'status': 0, 'message': 'url后缀重复'})
            except MultipleObjectsReturned:
                return JsonResponse({'status': 0, 'message': '存在意外的url后缀相同的文章'})
            except ObjectDoesNotExist:
                try:
                    Article.objects.get(title=title)
                    return JsonResponse({'status': 0, 'message': '文章标题重复'})
                except MultipleObjectsReturned:
                    return JsonResponse({'status': 0, 'message': '存在意外的标题相同的文章'})
                except ObjectDoesNotExist:
                    # 简单的处理数据
                    md_file = None
                    if md_code:
                        md_file = ContentFile(md_code, name='editor.md')
                    if file is not None:
                        md_file = file
                    y = int(time.strftime('%Y'))
                    m = int(time.strftime('%m'))
                    d = int(time.strftime('%d'))

                    a = Article.objects.create(url_suffix=suffix, title=title, year=y, month=m, day=d, top=top, md_file=md_file)

                    for au in authors:
                        author = Author.objects.get(author=au)
                        author.article_set.add(a)

                    for t in tags:
                        tag = Tag.objects.get(tag=t)
                        tag.article_set.add(a)

                    for c in categories:
                        category = Category.objects.get(category=c)
                        category.article_set.add(a)

                    return JsonResponse({'status': 1, 'message': '文章发布成功'})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()


# API Edit Article
@require_POST
@csrf_exempt
@login_required(redirect_field_name='', login_url='/admin_login/')
def api_edit_article(request):
    if request.is_ajax():
        if request.method == 'POST':
            # 获取请求数据
            md_code = request.POST['md_code']
            file = request.FILES.get('md_file')
            suffix = request.POST['url_suffix']
            title = request.POST['title']
            authors = request.POST.getlist('authors')
            tags = request.POST.getlist('tags')
            categories = request.POST.getlist('categories')
            top = request.POST['top']
            # 转换为布尔值
            if top == 'true':
                top = True
            elif top == 'false':
                top = False

            # 获取要修改的文章
            try:
                a = Article.objects.get(url_suffix=suffix)

                md_file = None
                if md_code:
                    md_file = ContentFile(md_code, name='editor.md')
                if file is not None:
                    md_file = file

                a.md_file = md_file
                a.title = title
                a.top = top
                a.save()

                a.author.clear()
                a.tags.clear()
                a.categories.clear()

                for au in authors:
                    author = Author.objects.get(author=au)
                    a.author.add(author)

                for t in tags:
                    tag = Tag.objects.get(tag=t)
                    a.tags.add(tag)

                for c in categories:
                    category = Category.objects.get(category=c)
                    a.categories.add(category)

                return JsonResponse({'status': 1, 'message': '文章修改成功'})
            except MultipleObjectsReturned:
                return JsonResponse({'status': 0, 'message': '存在意外url后缀相同的重复文章'})
            except ObjectDoesNotExist:
                return JsonResponse({'status': 0, 'message': '目标文章不存在'})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()


# API Add New Author/Tag/Category
@require_POST
@csrf_exempt
@login_required(redirect_field_name='', login_url='/admin_login/')
def api_add_info(request):
    if request.is_ajax():
        if request.method == 'POST':
            msg = request.POST['msg']
            new = request.POST['new']

            if msg == 'add_author':
                obj, created = Author.objects.get_or_create(author=new)
                if created:
                    message = '新的作者 ' + new + ' 添加成功'
                    return JsonResponse({'status': 1, 'message': message})
                else:
                    message = '作者 ' + new + ' 已存在'
                    return JsonResponse({'status': 0, 'message': message})

            if msg == 'add_tag':
                obj, created = Tag.objects.get_or_create(tag=new)
                if created:
                    message = '新的标签 ' + new + ' 添加成功'
                    return JsonResponse({'status': 1, 'message': message})
                else:
                    message = '标签 ' + new + ' 已存在'
                    return JsonResponse({'status': 0, 'message': message})

            if msg == 'add_category':
                obj, created = Category.objects.get_or_create(category=new)
                if created:
                    message = '新的分类 ' + new + ' 添加成功'
                    return JsonResponse({'status': 1, 'message': message})
                else:
                    message = '分类 ' + new + ' 已存在'
                    return JsonResponse({'status': 0, 'message': message})
            else:
                return JsonResponse({'status': 0, 'message': '添加指令有误'})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()


# API Add Images
@require_POST
@csrf_exempt
@login_required(redirect_field_name='', login_url='/admin_login/')
def api_add_images(request):
    if request.is_ajax():
        if request.method == 'POST':
            images = request.FILES.getlist('images')

            for image in images:
                Image.objects.create(username=request.user, image=image)

            return JsonResponse({'status': 1, 'message': '图片上传成功'})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseServerError()
