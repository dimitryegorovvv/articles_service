from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    text = models.CharField(max_length=10000, verbose_name='текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    published = models.BooleanField(default=False, verbose_name='опубликовано ли')
    image = models.ImageField(upload_to='photos', blank=True, null=True, verbose_name='изображение')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class Comment(models.Model):
    text = models.CharField(max_length=1000, validators=[MinLengthValidator(1)], verbose_name='комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE, verbose_name='статья')

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


