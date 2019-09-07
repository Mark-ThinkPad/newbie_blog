from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.utils.safestring import mark_safe
import codecs
import markdown


# Author Model
# 或为多作者铺路
class Author(models.Model):
    author = models.CharField(max_length=40)

    def __str__(self):
        return self.author

    def show_articles(self):
        return ' | '.join([str(a) for a in self.article_set.all()])


# Tag Model
class Tag(models.Model):
    tag = models.CharField(max_length=40)

    def __str__(self):
        return self.tag

    def show_articles(self):
        return ' | '.join([str(a) for a in self.article_set.all()])


# Category Model
class Category(models.Model):
    category = models.CharField(max_length=40)

    def __str__(self):
        return self.category

    def show_articles(self):
        return ' | '.join([str(a) for a in self.article_set.all()])


# Article Model
class Article(models.Model):
    # url后缀
    url_suffix = models.CharField(max_length=40)
    # 文章标题
    title = models.CharField(max_length=40)
    # 支持单篇文章多作者
    author = models.ManyToManyField(Author)
    # 支持单篇文章多标签和多分类
    tags = models.ManyToManyField(Tag)
    categories = models.ManyToManyField(Category)
    # 年月日分开字段存放, 这个设计是为了配合预想的动态url设计, 方便归档页面的按年份分开板块
    year = models.IntegerField(validators=[MinValueValidator(2018), MaxValueValidator(9999)])
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    # 上传时间字段得以保留, 作用转为后台管理用, 方便已存的历史文章迁移管理
    upload_time = models.DateTimeField(auto_now_add=True)
    # 最后修改时间
    edited_time = models.DateTimeField(auto_now=True)
    # 支持文章置顶
    top = models.BooleanField(default=False)
    # 点击量
    click = models.PositiveIntegerField(default=0)
    # markdown文档
    md_file = models.FileField(upload_to='document/%Y')

    def __str__(self):
        return self.title

    def show_authors(self):
        return ' & '.join([str(a) for a in self.author.all()])

    def show_tags(self):
        return ' | '.join([str(t) for t in self.tags.all()])

    def show_categories(self):
        return ' | '.join([str(c) for c in self.categories.all()])

    def click_increase(self):
        self.click += 1
        self.save(update_fields=['click'])

    def getHTML(self):
        input_file = codecs.open(self.md_file.path, mode="r", encoding="utf-8")
        text = input_file.read()
        md_html = markdown.markdown(text)

        return mark_safe(md_html)


# Image Model
class Image(models.Model):
    username = models.CharField(max_length=40)
    image = models.ImageField(upload_to='images/%Y')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url


# Project Model (精选项目)
class Project(models.Model):
    name = models.CharField(max_length=40)
    url = models.URLField(validators=[URLValidator(schemes=['http', 'https'])])

    def __str__(self):
        return self.name


# Friend Model (友情链接)
class Friend(models.Model):
    avatar = models.URLField(validators=[URLValidator(schemes=['http', 'https'])])
    name = models.CharField(max_length=40)
    url = models.URLField(validators=[URLValidator(schemes=['http', 'https'])])

    def __str__(self):
        return self.name
