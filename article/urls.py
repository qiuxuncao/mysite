from django.conf.urls import url
from . import views


urlpatterns=[
    url(r'^article-column/$', views.article_column, name='article_column'),
    url(r'^rename-column/$', views.rename_article_column, name='rename_article_column'),
    url(r'^delete-column/$', views.delete_article_column, name='delete_column'),
    url(r'^post-article/$', views.article_post, name='article_post'),
    url(r'^article-list/$', views.article_list, name='article_list'),
    url(r'^delete-article/$', views.delete_article, name='delete_article'),
    url(r'^article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.article_detail, name='article_detail'),
    url(r'^re-edit-article/(?P<article_id>\d+)$', views.re_edit_article, name='re_edit_article'),

]