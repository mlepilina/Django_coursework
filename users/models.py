from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    username = None

    email = models.EmailField(verbose_name='контактный email', unique=True)
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    name = models.CharField(max_length=100, verbose_name='имя')
    patronymic = models.CharField(max_length=100, verbose_name='отчество (если есть)', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email_confirmed = models.BooleanField('Почта пользователя подтверждена', default=False)
    email_confirm_key = models.CharField(verbose_name='Ключ подтверждения для почты пользователя', max_length=250, **NULLABLE)
