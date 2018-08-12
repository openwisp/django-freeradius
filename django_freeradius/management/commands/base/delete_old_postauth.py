from datetime import timedelta

import swapper
from django.core.management import BaseCommand
from django.utils.timezone import now

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")


class BaseDeleteOldPostauthCommand(BaseCommand):
    help = "Delete post-auth logs older than <days>"

    def add_arguments(self, parser):
        parser.add_argument('number_of_days', type=int)

    def handle(self, *args, **options):
        if options['number_of_days']:
            days = now() - timedelta(days=options['number_of_days'])
            RadiusPostAuth.objects.filter(date__lt=days).delete()
            self.stdout.write('Deleted post-auth logs older than {} days'.format(options['number_of_days']))
