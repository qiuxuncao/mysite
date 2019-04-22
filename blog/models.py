from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class BlogArticles(models.Model):

    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, related_name="blog_posts")
    body = models.TextField()
    #故意写成now(),看看是否报错----会报错
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        # BlogArticles实例对象在后台展示时，按照publish字段倒序排列
        ordering = ("-publish",)


    # 先不写这里
    # def __str__(self):
    #     return self.title


class Contact(models.Model):

    name = models.CharField(max_length=20)
    content = models.TextField()
    email = models.EmailField(null=True)