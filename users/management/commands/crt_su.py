import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mail.ru',
            first_name='Victor',
            last_name='Volkov',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(os.getenv('PSQL_PASS'))
        user.save()
