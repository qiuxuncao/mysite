from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from django.utils import timezone
from django.core.urlresolvers import reverse
from PIL import Image
# Create your models here.


class ArticleColumn(models.Model):
    # 用户与栏目是“一对多”关系，所以用ForeignKey,一个用户可以设置多个栏目,此处的user字段对应实际表中的user_id,来自于User表中主键
    user = models.ForeignKey(User, related_name='article_column')
    column = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    # 必须要写此方法，要不外键关系返回ArticleColumn object，而不是具体的column值
    def __str__(self):
        return self.column


class ArticlePost(models.Model):

    author = models.ForeignKey(User, related_name='article')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name='article_column')
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='media/%Y%m%d/', blank=True)



    class Meta:
        ordering = ('title',)
        #对这俩字段建立索引，后面会根据文章id和slug获取文章对象，也能提高读取文章对象速度
        index_together = (('id', 'slug'),)

    def __str__(self):
        # 实例化该类时会返回对象的title
        return self.title

    # 保存时处理图片
    def save(self, *args, **kwargs):
        '''
        每个数据模型都有一个save方法，这里重写该方法，目的是要实现self.slug = slugify(self.title)
        :param args:
        :param kwargs:
        :return:
        '''
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

        # 调用原有的save()方法
        # article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片
        # if self.avatar and not kwargs.get('update_fields'):
        # if self.avatar:
        #     image = Image.open(self.avatar)
        #     (x, y) = image.size
        #     new_x = 400
        #     new_y = int(new_x*(y/x))
        #     resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
        #     resized_image.save(self.avatar.path)
        # return article

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id, self.slug])

