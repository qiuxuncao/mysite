from django.shortcuts import render
from .models import ArticleColumn
from utils.decorators import login_wrapper
# Create your views here.


@login_wrapper
def article_column(request):
    columns = ArticleColumn.objects.filter(user=request.user)
    return render(request, "article/column/article_column.html", {'columns': columns})