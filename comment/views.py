from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from article.models import ArticlePost
from comment.forms import CommentForm
from .models import Comment
from utils.decorators import login_wrapper

# Create your views here.

# @login_wrapper
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)
    print(article_id, parent_comment_id)
    # 处理post请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                print('已请求')
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过两级，则转为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                print('评论已写入')
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect('article:list_article_titles')
        else:
            return HttpResponse("表单有误，重新填写")

    elif request.method == 'GET':
        print('获取评论')
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)

    else:
        return HttpResponse("仅接受get或者post请求")