from django.contrib import admin

from management_service.models import Client, Message, Mailing, MailingLogs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_status', 'message', 'id',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('attempt_status',)
