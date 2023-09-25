from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='maria36127@gmail.com',
            surname='Admin',
            name='Maria',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('12345')
        user.save()
