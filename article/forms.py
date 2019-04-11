from .models import ArticleColumn, ArticlePost
from django import forms


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('column',)
        ordering = ('-created',)


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        # fields = ('title', 'body')
        fields = ('title', 'body', 'avatar')
        ordering = ('updated',)
