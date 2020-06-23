from django.core.management.base import BaseCommand
from scat.server import ScatServer


class Command(BaseCommand):
    help = "Create a game service template."

    def add_arguments(self, parser):
        parser.add_argument('dirname', nargs='?')

    def handle(self, *args, **options):
        server_name = ''
        server = ScatServer(server_name)
        server.start()
