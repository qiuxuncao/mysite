from django.shortcuts import render, get_object_or_404
from .models import BlogArticles
from django.http import HttpResponse
from utils.decorators import login_wrapper
# Create your views here.


def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/title.html", {'blogs': blogs})


def blog_content(request, article_id):
    # article = BlogArticles.objects.get(id=article_id)
    # 没有找到对象显示404页面
    article = get_object_or_404(BlogArticles, id= article_id)
    return render(request, "blog/content.html", {'article': article})


@login_wrapper
def blog_about(request):

    return HttpResponse("关于本站，只有登录才能看哦")


@login_wrapper
def blog_course(request):

    return HttpResponse('恭喜你，进入到了秘密花园')