import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title_text = models.CharField("Название поста", max_length=100)
    text = models.TextField(verbose_name="Содержание поста")
    pub_date = models.DateTimeField("Время и дата публикации")
    photo = models.ImageField("Фото", blank=True, upload_to='photos/%Y/%m/%d/')
    thumbnumber = models.IntegerField(default=0, help_text="Начинается с 1", verbose_name="Количество лайков")
    likedone = models.ManyToManyField(User, verbose_name="Добавивший пользователь", related_name='users_post_main')

    def publish(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))
        self.save()

    def __str__(self):
        return self.title_text

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField("Имя автора", max_length=20)
    text_comment = models.CharField("Текст комментария", max_length=200)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
