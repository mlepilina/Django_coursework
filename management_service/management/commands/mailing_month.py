from django.utils import timezone
from django.core.management import BaseCommand

from management_service.models import Mailing, MailingLogs


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Отправка ежемесячных рассылок.
        """
        print('Start mailing month')

        current_time = timezone.now()
        current_month = current_time.replace(day=1, hour=0, minute=0, second=0)

        mailings = Mailing.objects.filter(
            mailing_frequency=Mailing.FREQUENCY_CHOICES.EVERY_MONTH,
            mailing_status=Mailing.STATUS_CHOICES.STARTED,
            mailing_time__lte=current_time
        ).exclude(
            # this month:00.00.00 > MailingLogs.last_attempt_date_time < current_time
            mailing_logs__last_attempt_date_time__range=(
                current_month, current_time
            ),

            #MailingLogs.attempt_status == MailingLogs.STATUS_OK
            mailing_logs__attempt_status=MailingLogs.STATUS_OK
        )

        for mailing in mailings:
            mailing.execute()

        print('END mailing month')
