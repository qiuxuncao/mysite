from django.shortcuts import render
from .models import ArticlePost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def article_titles(request):

    articles = ArticlePost.objects.all()
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles_list = current_page.object_list
        a = current_page
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles_list = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles_list = current_page.object_list
    return render(request, 'article/column/article_titles.html', {'articles': articles_list, 'page': current_page})
