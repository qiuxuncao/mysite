from .models import ArticleColumn, ArticlePost
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

    # def save(self, *args, **kwargs):
    #     '''
    #     重写form的save()方法，使其可以根据是否存在旧数据，而进行修改
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     '''
    #     # if not self.pk:


