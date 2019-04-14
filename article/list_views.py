from django.shortcuts import render
from .models import ArticlePost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from .views import right_lider
from .models import ArticleColumn


def article_titles(request):

    # print()
    articles = ArticlePost.objects.all()
    # author = request.GET.get('article.author')
    # print(author)
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles_list = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles_list = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles_list = current_page.object_list
    return render(request, 'article/column/article_titles.html', {'articles': articles_list, 'page': current_page})


def article_titles_by_someone(request, author):
    '''
    该作者的所有文章
    :param request:
    :param author:
    :return:
    '''

    # 该作者的所有栏目
    # article = ArticlePost.objects.get(id=id)
    print('传递过来的作者为：%s' % author)
    user = User.objects.get(username=author)
    print('作者的id是：%s' % user.id)
    # 以下两种都行
    # columns = ArticleColumn.objects.filter(user=user)
    columns = ArticleColumn.objects.filter(user=user.id)
    print('%s拥有的栏目是%s'% (author,columns))
    column_count_dict = {}
    for column in columns:
        column_count = ArticlePost.objects.filter(column=column).count()
        print(column)
        column_count_dict[str(column)] = column_count
        print('【%s】 栏目的总数是：%s' % (column, column_count))
    print(column_count_dict)

    # article = ArticlePost.objects.get(id=5)
    # 因为ArticlePost有一个方法def __str__(self):返回是title，所以打印article为id=5文章的title
    # print(article)

    print('作者是：%s' % author)
    user = User.objects.get(username=author)
    print(user)
    author1 = author
    # 查询出该作者所有的文章对象
    articles = ArticlePost.objects.filter(author=user)
    # else:
    #     articles = ArticlePost.objects.filter(author=user)
    print(articles[0].author)
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles_list = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles_list = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles_list = current_page.object_list
    return render(request, 'article/column/article_titles.html', {'articles': articles_list,
                                                                  'page': current_page,
                                                                  'column_count_dict': column_count_dict,
                                                                  # 此处不能加'author': author，添加后报错，暂时未知原因
                                                                  # Reverse for 'list_article_titles_bysomeone' with arguments '('guchen', <ArticleColumn: django>)' not found.
                                                                  # 1 pattern(s) tried: ['article/list-article-titles-bysomeone/(?P<author>[-\\w]+)/$']
                                                                  # 'author': author
                                                                  })
