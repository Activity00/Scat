from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a game service template."

    def add_arguments(self, parser):
        parser.add_argument('dirname', nargs='?')

    def handle(self, *args, **options):
        dirname = options['dirname']
        print(dirname)
