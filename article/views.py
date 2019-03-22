from django.shortcuts import render,HttpResponse
from .models import ArticleColumn
from utils.decorators import login_wrapper
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import ArticleColumnForm
# Create your views here.


@csrf_exempt
@login_wrapper
def article_column(request):
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
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
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
