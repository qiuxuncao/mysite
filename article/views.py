from django.shortcuts import render,HttpResponse, get_object_or_404
from .models import ArticleColumn, ArticlePost
from utils.decorators import login_wrapper
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import ArticleColumnForm, ArticlePostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import redis
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
# Create your views here.


@csrf_exempt
@login_wrapper
def article_column(request):
    '''
    GET请求展示栏目，POST请求增加栏目
    :param request:
    :return:
    '''
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html",
                      {'columns': columns, 'column_form': column_form})

    if request.method == 'POST':
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(column=column_name, user_id=request.user.id)
        if columns:
            # 如果数据库中存在
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(column=column_name, user_id=request.user.id)
            return HttpResponse('1')


@csrf_exempt
@login_wrapper
@require_POST
def rename_article_column(request):
    '''
    编辑栏目名称（csrf_exempt装饰器必须放在最上面，否则会403）
    :param request:
    :return:
    '''
    # 获取从前台ajax方式传递的data数据
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        # 根据id查到该条数据
        line = ArticleColumn.objects.get(id=column_id)
        # 将该数据的column字段重新赋值为column_name，即前台的new_column
        line.column = column_name
        # 一定要保存
        line.save()
        return HttpResponse('1')

    except:
        return HttpResponse('0')


@csrf_exempt
@login_wrapper
@require_POST
def delete_article_column(request):
    '''
    删除栏目
    :param request:
    :return:
    '''
    column_id = request.POST['column_id']
    line = ArticleColumn.objects.filter(id=column_id)
    line.delete()
    return HttpResponse('1')


@csrf_exempt
@login_wrapper
def article_post(request):
    '''
    文章发布功能
    :param request:
    :return:
    '''
    if request.method == 'POST':
        # print('已进入article_post视图')
        print('request.FILES的值为：%s' % request.FILES)
        print('request.POST的值为：%s' % request.POST)
        # 实例化表单对象，来自于前端ajax请求
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                # ModelForm 类或者它的子类都具有save()方法，当然实例化后的article_post_form也有此方法，
                # 它的效果是生成该数据对象，并将表单数据保存到数据库
                # commit=False则表示只生成文章数据对象，不保存
                new_article = article_post_form.save(commit=False)
                # 给该文章数据对象设置作者和栏目后再进行保存
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                print('正在更新文章到数据库')
                new_article.avatar = request.FILES.get('avatarrrrr')
                # print('request.POST的值为：%s' % request.POST)
                # print('request.FILES的值为：%s' % request.FILES)
                print('request.FILES的值为：%s' % request.FILES.get('avatarrrrr'))

                print('即将保存')
                new_article.save()
                print('已经保存啦')
                return HttpResponse('1')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('不合法啊')
    else:
        article_post_form = ArticlePostForm()
        # 获取request.user用户的所有栏目article_column为ArticleColumn模型类中的user字段的related_name,其实等价于
        # article_columns = ArticleColumn.objects.filter(user=request.user)
        # 通过user实例，找到其名下所有的ArticleColumn实例
        article_columns = request.user.article_column.all()
        return render(request, 'article/column/article_post.html', {'article_post_form': article_post_form,
                                                                    'article_columns': article_columns})

from django.core.files.uploadedfile import UploadedFile
@csrf_exempt
def upload_img(request):
    if request.method == 'POST':
        print(3333333333333)
        print(request.FILES)
        print('request.FILES的值为：%s' % request.FILES.get('avatarrrrr'))
        # file = request.FILES.values()
        # wrapped_file = UploadedFile(file)
        # upload = ArticlePost.objects.create(avatar=wrapped_file)
        # upload.save()
        return HttpResponse('OK')


@csrf_exempt
@login_wrapper
def article_list(request):
    '''文章列表'''
    articles = ArticlePost.objects.filter(author=request.user)
    # 将articles对象每3条一页
    pageinator = Paginator(articles, 5)
    # 获取前端传来的page参数
    page = request.GET.get('page')
    try:
        # page()为Paginator对象的一个方法，可以获取指定页面内容，参数必须>=1的整数
        current_page = pageinator.page(page)
        # object_list是Page对象的属性，可以返回该页所有对象列表
        articles = current_page.object_list
    except PageNotAnInteger:
        # 当page参数不是整数时，展示第一页
        current_page = pageinator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        # 当page参数值为空或者没有page参数
        current_page = pageinator.page(pageinator.num_pages)
        articles = current_page.object_list
    return render(request, 'article/column/article_list.html', {'articles': articles, 'page': current_page})


@csrf_exempt
@login_wrapper
def delete_article(request):
    '''
    删除文章
    :param request:
    :return:
    '''
    article_id = request.POST['article_id']
    try:
        line = ArticlePost.objects.get(id=article_id)
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


# @login_wrapper
def article_detail(request, id, slug):
    # print(slug,id)
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    # 连接redis
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    # 总的访问次数，访问一次就+1，一般命名规则为"对象类型：对象ID：对象属性"
    total_views = r.incr('article:{}:views'.format(article.id))
    # zincrby(name, amount, value)方法:根据amount设定的步长增加有序集合name中的value的分值（类似于权重）
    # 实现了每访问一次文章就会将article_ranking中的article.id分值增加1
    # article_ranking中存放的是文章的id用来代表文章，每访问一次该文章就会增加文章的分值
    r.zincrby('article_ranking', 1, article.id)
    # 获取分值排名前十的对象
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    # 获取排名前十文章的id列表,使用的是列表推导式，先进行for循环，再将每次的的值带入int()方法运算，将结果放在新的列表中
    article_ranking_ids = [int(id) for id in article_ranking]
    print('文章浏览量对应的id：%s' % article_ranking_ids)
    # 查询出排名在前十的文章对象,并放在list中。注意id__in用法：id在article_ranking_ids列表中
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    print('文章未排序：%s' % most_viewed)
    # 将获得的列表按照下表索引进行排序，lamda为匿名函数，先运算后面表达式，冒号前的x相当于参数，代表most_viewed列表中文章对象
    # 按照文章的id得到对应的下标,再按照下标进行排序
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    print('文章已经排序：%s' % most_viewed)

    # 该作者的所有栏目
    article = ArticlePost.objects.get(id=id)
    print('作者为：%s' % article.author)
    user = User.objects.get(username=article.author)
    print(user.id)
    # 以下两种都行
    # columns = ArticleColumn.objects.filter(user=user)
    columns = ArticleColumn.objects.filter(user=user.id)
    print(columns)
    column_count_dict = {}
    for column in columns:
        column_count = ArticlePost.objects.filter(column=column).count()
        # print(column_count)
        column_count_dict[column]=column_count
        print('%s 栏目的总数是：%s' % (column, column_count))
    print(column_count_dict)
    return render(request, 'article/column/article_detail.html', {'article': article,
                                                                  'total_views': total_views,
                                                                  'most_viewed': most_viewed,
                                                                  'columns': columns,
                                                                  'column_count_dict': column_count_dict})


@csrf_exempt
# @login_wrapper
def re_edit_article(request, article_id):
    '''
    再次编辑文章
    :param request:
    :return:
    '''
    if request.method == 'GET':
        # 获取该用户的所有栏目
        columns = request.user.article_column.all()
        article_columns = ArticleColumn.objects.filter(user=request.user)
        # 注意是get，千万不能写成filter(id=article_id)，否则提示'QuerySet' object has no attribute 'title'
        # article = ArticlePost.objects.filter(id=article_id)
        article = ArticlePost.objects.get(id=article_id)
        # 实例化表单用于前台展示文章原有标题
        this_article_form = ArticlePostForm(initial={'title': article.title})
        return render(request, 'article/column/re_edit_article.html',
                      {'article': article,
                       'article_columns': article_columns,
                       'columns': columns,
                        'this_article_form': this_article_form
                       })
    elif request.method == 'POST':
        article = ArticlePost.objects.get(id=article_id)
        # 从数据库先取出具体的model对象article
        # 将此model对象作为instance的参数值传入form。save(),同时还有request.POST,和request.FILES参数，
        # 这样在save的时候就会update对应的model对象
        article_post_form = ArticlePostForm(request.POST, request.FILES, instance=article)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                # 此处的save有commit=False参数，意思是只生成model对象，而不保存，生成的model对象new_article就可以修改了
                new_article = article_post_form.save(commit=False)
                new_article.avatar = request.FILES.get('avatar')
                new_article.title = request.POST['title']
                new_article.body = request.POST['body']
                new_article.column_id = request.POST['column_id']

                print('开始保存')
                new_article.save()
                # ArticlePost.objects.filter(id=article_id).update(title=title, body=body, column_id=column_id, avatar=avatar)
                print('保存成功')
                return HttpResponse('1')
            except:
                return HttpResponse('2')


def right_lider(request, author):
    # 该作者的所有栏目
    # article = ArticlePost.objects.get(id=id)
    print('作者为：%s' % author)
    user = User.objects.get(username=author)
    print(user.id)
    # 以下两种都行
    # columns = ArticleColumn.objects.filter(user=user)
    columns = ArticleColumn.objects.filter(user=user.id)
    print(columns)
    column_count_dict = {}
    for column in columns:
        column_count = ArticlePost.objects.filter(column=column).count()
        # print(column_count)
        column_count_dict[column] = column_count
        print('%s 栏目的总数是：%s' % (column, column_count))
    print(column_count_dict)
    return column_count_dict
    # return render(request, 'article/right_lider.html', {'column_count_dict': column_count_dict})