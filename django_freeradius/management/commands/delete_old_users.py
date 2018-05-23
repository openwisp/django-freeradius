from datetime import timedelta

from django.core.management import BaseCommand
from django.utils.timezone import now

from django_freeradius.models import RadiusBatch
from django_freeradius.settings import DEFAULT_USER_DELETION_DURATION


class Command(BaseCommand):
    help = "Deactivating users added in batches which have expired"

    def add_arguments(self, parser):
        parser.add_argument('--older-than-months',
                            action='store',
                            default=DEFAULT_USER_DELETION_DURATION,
                            help='delete users which have expired before this time')

    def handle(self, *args, **options):
        months = now() - timedelta(days=30*options['older_than_months'])
        batches = RadiusBatch.objects.filter(expiration_date__lt=months)
        for b in batches:
            b.delete()
        self.stdout.write('Deleted accounts older than {} months'.format(options['older_than_months']))
