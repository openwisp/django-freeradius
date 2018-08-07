from datetime import timedelta

import swapper
from django.core.management import BaseCommand
from django.utils.timezone import now

RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")


class BaseDeleteOldRadacctCommand(BaseCommand):
    help = "Delete accounting sessions older than <days>"

    def add_arguments(self, parser):
        parser.add_argument('number_of_days', type=int)

    def handle(self, *args, **options):
        if options['number_of_days']:
            days = now() - timedelta(days=options['number_of_days'])
            RadiusAccounting.objects.filter(stop_time__lt=days).delete()
            self.stdout.write('Deleted sessions older than {} days'.format(options['number_of_days']))
