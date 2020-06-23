from django.core.management.base import BaseCommand

from scat.distributed.master import Master
from scat.distributed.master import MASTER_SERVER_MODE, SINGLE_SERVER_MODE, MULTI_SERVER_MODE


class Command(BaseCommand):
    help = "start game server."

    def handle(self, *args, **options):
        mode = ''
        server_name = 'master'

        if mode == "single":
            if server_name == "master":
                mode = MASTER_SERVER_MODE
            else:
                mode = SINGLE_SERVER_MODE
        else:
            mode = MULTI_SERVER_MODE
            server_name = ''

        master = Master()
        master.start(server_name, mode)
        master = Master()
        master.start('', 1)
