import os
import signal
import sys

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Shuts down the Django development server'

    def handle(self, *args, **kwargs):
        os.kill(os.getpid(), signal.SIGINT)
        sys.exit(0)