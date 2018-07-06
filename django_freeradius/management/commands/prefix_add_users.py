import sys
from datetime import datetime

import swapper
from django.core.management import BaseCommand

from django_freeradius.settings import BATCH_DEFAULT_PASSWORD_LENGTH

RadiusBatch = swapper.load_model("django_freeradius", "RadiusBatch")


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
        number_of_users = options['n']
        if expiration_date:
            expiration_date = datetime.strptime(expiration_date, '%d-%m-%Y')
        if number_of_users < 1:
            self.stdout.write("The number of users to be generated should be greater than or equal to 1")
            sys.exit(1)
        batch = RadiusBatch(name=options['name'], prefix=prefix,
                            expiration_date=expiration_date, strategy='prefix')
        batch.save()
        batch.prefix_add(prefix, number_of_users, options['password_length'])
        self.stdout.write('Generated a batch of users with prefix {}'.format(prefix))
