import csv
from datetime import datetime

from django.core.management import BaseCommand, CommandError

from django_freeradius.models import RadiusBatch
from django_freeradius.settings import BATCH_DEFAULT_PASSWORD_LENGTH


class Command(BaseCommand):
    help = "Add a batch of users from a file"

    def add_arguments(self, parser):
        parser.add_argument('--file',
                            action='store',
                            help='Will import users from the file')
        parser.add_argument('--expiration',
                            action='store',
                            default=None,
                            help='Will deactivate users after this date')
        parser.add_argument('--password-length',
                            action='store',
                            default=BATCH_DEFAULT_PASSWORD_LENGTH,
                            type=int)

    def handle(self, *args, **options):
        try:
            csvfile = open(options['file'], 'rt')
        except IOError:
            raise CommandError('File does not exist')
        reader = csv.reader(csvfile, delimiter=',')
        expiration_date = options['expiration']
        if expiration_date:
            expiration_date = datetime.strptime(expiration_date, '%d-%m-%Y')
        batch = RadiusBatch.objects.create(expiration_date=expiration_date)
        batch.add(reader, options['password_length'])
        self.stdout.write('Added a batch of users to csv file')
        csvfile.close()
