import swapper
from django.core.management import BaseCommand
from django.utils.timezone import now

RadiusBatch = swapper.load_model("django_freeradius", "RadiusBatch")


class BaseDeactivateExpiredUsersCommand(BaseCommand):
    help = "Deactivating users added in batches which have expired"

    def handle(self, *args, **options):
        radbatches = RadiusBatch.objects.filter(expiration_date__lt=now())
        for batch in radbatches:
            batch.expire()
        self.stdout.write('Deactivated users of batches expired')
