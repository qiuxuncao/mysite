from django.shortcuts import render,HttpResponse
from .models import ArticleColumn, ArticlePost
from utils.decorators import login_wrapper
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import ArticleColumnForm, ArticlePostForm
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
    if request.method == 'POST':
        # 实例化表单对象，data来自于前端ajax请求
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                # ModelForm 类或者它的子类都具有save()方法，它的效果是生成该数据对象，并将表单数据保存到数据库
                # commit=False只生成数据对象，不保存
                new_article = article_post_form.save(commit=False)
                # 给该数据对象设置作者和栏目后再进行保存
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse('1')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else:
        article_post_form = ArticlePostForm()
        # 获取request.user用户的所有栏目
        article_columns = request.user.article_column.all()
        return render(request, 'article/column/article_post.html', {'article_post_form': article_post_form, 'article_columns': article_columns})


@csrf_exempt
@login_wrapper
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    return render(request, 'article/column/article_list.html', {'articles': articles})