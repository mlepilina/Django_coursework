from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mass_mail
from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='контактный email', unique=True)
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    name = models.CharField(max_length=100, verbose_name='имя')
    patronymic = models.CharField(max_length=100, verbose_name='отчество (если есть)', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    owner = models.ForeignKey(
        User, to_field='email', db_column="owner", on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE
    )

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    message_subject = models.TextField(verbose_name='тема сообщения')
    message_text = models.TextField(verbose_name='текст сообщения')

    def __str__(self):
        return f'{self.message_subject}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):

    class STATUS_CHOICES(models.TextChoices):
        FINISHED = ('завершена', 'завершена')
        CREATED = ('создана', 'создана')
        STARTED = ('запущена', 'запущена')

    class FREQUENCY_CHOICES(models.TextChoices):
        EVERYDAY = ('раз в день', 'раз в день')
        EVERY_WEEK = ('раз в неделю', 'раз в неделю')
        EVERY_MONTH = ('раз в месяц', 'раз в месяц')

    mailing_time = models.TimeField(verbose_name='время рассылки')
    mailing_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES.choices, verbose_name='периодичность рассылки')
    mailing_status = models.CharField(max_length=50, choices=STATUS_CHOICES.choices, default='создана', verbose_name='статус рассылки')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='клиенты')

    owner = models.ForeignKey(
        User, to_field='email', db_column="owner", on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE
    )

    def __str__(self):
        return f'{self.message.message_subject} | {self.mailing_status}: {self.mailing_frequency}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def execute(self):
        """
        Документация по отправке писем: https://docs.djangoproject.com/en/4.2/topics/email/
        """
        mailing_log = MailingLogs(
            last_attempt_date_time=timezone.now(),
            mailing=self,
            attempt_status=MailingLogs.STATUS_OK
        )
        message = self.message
        messages = []
        for client in self.clients.all():
            messages.append(
                (
                    message.message_subject,
                    message.message_text,
                    settings.EMAIL_HOST_USER,
                    [client.email],
                )
            )

        try:
            send_mass_mail(messages, fail_silently=False)
        except SMTPException as exc:
            mailing_log.mail_server_response = f'Ошибка при отправке: {exc}'
            mailing_log.attempt_status = MailingLogs.STATUS_FAILED
        finally:
            mailing_log.save()


class MailingLogs(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    last_attempt_date_time = models.DateTimeField(verbose_name='дата и время последней попытки')
    attempt_status = models.CharField(max_length=50, choices=STATUSES, verbose_name='статус попытки')
    mail_server_response = models.TextField(verbose_name='ответ почтового сервера (если был)', **NULLABLE)

    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name='mailing_logs', verbose_name='рассылка'
    )

    def __str__(self):
        return f'{self.attempt_status} - {self.last_attempt_date_time}'

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылки'

