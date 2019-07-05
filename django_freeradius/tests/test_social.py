import os
from unittest import skipIf

from django.test import TestCase

from django_freeradius.models import RadiusToken

from .base.test_social import BaseTestSocial


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestSocial(BaseTestSocial, TestCase):
    radius_token_model = RadiusToken
