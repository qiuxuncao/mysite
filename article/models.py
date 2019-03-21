from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ArticleColumn(models.Model):
    # 用户与栏目是“一对多”关系，所以用ForeignKey,一个用户可以设置多个栏目,此处的user字段对应实际表中的user_id,来自于User表中主键
    user = models.ForeignKey(User, related_name='article_column')
    column = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

