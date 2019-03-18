from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.blog_title, name='blog_title'),
    # 文章详情页，?P<article_id>\d匹配一个数字字符并将该字符赋值给参数article_id,传递给视图函数views.blog_content
    url(r'(?P<article_id>\d)/$', views.blog_content, name='blog_content')
]