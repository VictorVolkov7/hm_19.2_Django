from django.core.management import BaseCommand, call_command

from catalog.models import Category, Product
from settings import DATA_PATH


class Command(BaseCommand):
    data_path = DATA_PATH

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        call_command('loaddata', Command.data_path)
