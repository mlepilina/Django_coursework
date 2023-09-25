from django.utils import timezone
from django.core.management import BaseCommand

from management_service.models import Mailing, MailingLogs


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Отправка ежедневных рассылок.
        """
        print('Start mailing day')

        current_time = timezone.now()

        mailings = Mailing.objects.filter(
            mailing_frequency=Mailing.FREQUENCY_CHOICES.EVERYDAY,
            mailing_status=Mailing.STATUS_CHOICES.STARTED,
            mailing_time__lte=current_time
        ).exclude(
            # today:00.00.00 > MailingLogs.last_attempt_date_time < current_time
            mailing_logs__last_attempt_date_time__range=(
                current_time.replace(hour=0, minute=0, second=0), current_time
            ),

            #MailingLogs.attempt_status == MailingLogs.STATUS_OK
            mailing_logs__attempt_status=MailingLogs.STATUS_OK
        )

        for mailing in mailings:
            mailing.execute()

        print('END mailing day')

