from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='заголовок')
    content = models.TextField(max_length=2000, verbose_name='текст статьи')
    image = models.ImageField(upload_to='articles/', verbose_name='изображение', **NULLABLE)
    number_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')
    date_of_publication = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    owner = models.ForeignKey(
        User, to_field='email', db_column="owner", on_delete=models.CASCADE, verbose_name='автор', **NULLABLE
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('number_of_views', 'date_of_publication')
