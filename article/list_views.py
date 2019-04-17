from django.shortcuts import render
from .models import ArticlePost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from .views import right_lider, most_viewd, article_detail
from . import views
from .models import ArticleColumn
from django.conf import settings
import redis

def article_titles(request):

    # 从redis中取到由文章id排序的list，通过list的文章id查到文章title，传递给前台展示
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    # 此处的article_ranking键为article_detail()视图中生成的，由于article_ranking的type类型为zset,所以使用zrange获取该键的值
    # zrevrange为按照分值降序排列，zrange按照分值升序排列0代表从下标0开始，-1代表结尾，整体代表全部，如果前十个就是r.zrevrange('article_ranking', 0, 9)
    list_sorted = r.zrevrange('article_ranking', 0, -1)
    print(list_sorted)
    # 定义空的列表，用于存放按照id查出来的文章对象
    articles_list_most_viewed = []
    for i in list_sorted[0:10]:
        print(i)
        i.decode()
        # list的元素是bytes类型,
        print(type(i))
        # 根据id查出文章对象
        article = ArticlePost.objects.get(id=i)
        print(article.title)
        # 将前十个文章对象放进列表中,传递到模板展示
        articles_list_most_viewed.append(article)
        print(articles_list_most_viewed)

    articles = ArticlePost.objects.all()
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
                                                                  'articles_list_most_viewed': articles_list_most_viewed})


def article_titles_by_someone(request, author, *args):
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
    # 查询出该作者所有的文章对象
    column_name = request.GET.get('column')
    print(column_name)
    if column_name:
        column_id = ArticleColumn.objects.get(column=column_name, user=user)
        articles = ArticlePost.objects.filter(author=user, column=column_id)
        # else:
        #     articles = ArticlePost.objects.filter(author=user)
        # print(articles[0].author)
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
                                                                  'author': author
                                                                  })
    else:
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
                                                                      'author': author
                                                                      })