import os
from unittest import skipIf

from django.test import TestCase

from django_freeradius.models import RadiusBatch

from .base.test_batch_add_users import BaseTestCSVUpload


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestCSVUpload(BaseTestCSVUpload, TestCase):
    radius_batch_model = RadiusBatch
