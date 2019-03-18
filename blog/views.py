from django.shortcuts import render, get_object_or_404
from .models import BlogArticles
# Create your views here.


def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/title.html", {'blogs': blogs})


def blog_content(request, article_id):
    # article = BlogArticles.objects.get(id=article_id)
    # 没有找到对象显示404页面
    article = get_object_or_404(BlogArticles, id= article_id)
    return render(request, "blog/content.html", {'article': article})
