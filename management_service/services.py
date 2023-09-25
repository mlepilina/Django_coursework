from django.conf import settings
from django.core.cache import cache

from management_service.models import Message


def get_cached_messages(mailing_pk):
    if settings.CACHE_ENABLED:
        key = f'message_list{mailing_pk}'
        message_list = cache.get(key)
        if message_list is None:
            message_list = Message.objects.filter(mailing=mailing_pk)
            cache.set(key, message_list)

    else:
        message_list = Message.objects.filter(mailing=mailing_pk)

    return message_list