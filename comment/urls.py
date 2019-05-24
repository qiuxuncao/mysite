from django.conf.urls import url
from . import views

urlpatterns =[
    # 处理一级回复，不传入parent_comment_id则默认值为None
    url(r'^post-comment/(?P<article_id>\d+)', views.post_comment, name='post_comment'),
    # 处理二级回复
    url(r'^post-comment/(?P<article_id>\d+)/(?P<parent_comment_id>\d+)', views.post_comment, name='comment_reply')
]