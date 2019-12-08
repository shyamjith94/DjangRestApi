import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django Command to pause execution until the Database available"""
    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting For DataBase')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Data Base Unavailable Waiting For 1 second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Data Base Available'))
