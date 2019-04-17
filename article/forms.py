from .models import ArticleColumn, ArticlePost, Comments
from django import forms


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('column',)


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        # fields = ('title', 'body')
        fields = ('title', 'body', 'avatar')


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body',)
