from django.core.management.base import BaseCommand, CommandError

from .make_database import populate


class Command(BaseCommand):
    help = 'Populate catalog with fake data'

    

    def handle(self, *args, **options):
        print('filling database with wake data...')
        populate()
        print('Database has been filled')