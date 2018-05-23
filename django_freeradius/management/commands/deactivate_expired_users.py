from django.core.management import BaseCommand
from django.utils.timezone import now

from django_freeradius.models import RadiusBatch


class Command(BaseCommand):
    help = "Deactivating users added in batches which have expired"

    def handle(self, *args, **options):
        radbatches = RadiusBatch.objects.filter(expiration_date__lt=now())
        for batch in radbatches:
            batch.expire()
        self.stdout.write('Deactivated users of batches expired')
