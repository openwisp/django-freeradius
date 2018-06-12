from datetime import datetime

from django.core.management import BaseCommand

from django_freeradius.models import RadiusBatch
from django_freeradius.settings import BATCH_DEFAULT_PASSWORD_LENGTH


class Command(BaseCommand):
    help = "Generate a batch of users with usernames starting with a prefix"

    def add_arguments(self, parser):
        parser.add_argument('--name',
                            action='store',
                            help='Name of the event of batch addition')
        parser.add_argument('--prefix',
                            action='store',
                            help='Will generate users using this prefix')
        parser.add_argument('--n',
                            action='store',
                            help='Number of users to be generated',
                            type=int)
        parser.add_argument('--expiration',
                            action='store',
                            default=None,
                            help='Will deactivate users after this date')
        parser.add_argument('--password-length',
                            action='store',
                            default=BATCH_DEFAULT_PASSWORD_LENGTH,
                            type=int)

    def handle(self, *args, **options):
        prefix = options['prefix']
        expiration_date = options['expiration']
        if expiration_date:
            expiration_date = datetime.strptime(expiration_date, '%d-%m-%Y')
        batch = RadiusBatch(name=options['name'], prefix=prefix,
                            expiration_date=expiration_date, strategy='prefix')
        batch.save()
        batch.prefix_add(prefix, options['n'], options['password_length'])
        self.stdout.write('Generated a batch of users with prefix {}'.format(prefix))
