from django.core.management.base import BaseCommand, CommandError
from lectures.make_database import FakeDatabase


class Command(BaseCommand):
    help = 'Fill database with fake data'

    def handle(self, *args, **options):
        FakeDatabase().make()
