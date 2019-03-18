from django.contrib import admin
from .models import BlogArticles
# Register your models here.


#控制文章在admin后台显示什么字段搜索范围等等
class BlogArticlesAdmin(admin.ModelAdmin):

    list_display = ('title','author','publish')
    list_filter = ('publish', 'author')
    search_fields = ('title', 'body', 'author')


#将BlogArticles类注册到admin，否则后台看不到；也将控制文章展示的类注册到admin
admin.site.register(BlogArticles, BlogArticlesAdmin)