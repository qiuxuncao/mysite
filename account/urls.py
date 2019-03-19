from django.conf.urls import url
from .import views
from django.contrib.auth import views as auth_views

urlpatterns=[

    #系统自带的登录方法
    # url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='user_login'),
    #使用自己定义的登录方法
    url(r'^login2/$', views.user_login, name='user_login'),
    # url(r'^logout/$', auth_views.logout, {'template_name': 'account/logout.html'}, name='user_logout'),
    url(r'^logout/$', auth_views.logout, name='user_logout'),
    url(r'^register/$',views.register, name='user_register'),
    url(r'my-infomation/$', views.myself, name='my_infomation'),
]