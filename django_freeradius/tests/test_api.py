import os
from unittest import skipIf

import swapper
from django.test import TestCase

from .base.test_api import BaseTestApi

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestApi(BaseTestApi, TestCase):
    radius_postauth_model = RadiusPostAuth
    radius_accounting_model = RadiusAccounting
