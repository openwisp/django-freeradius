import os
from unittest import skipIf

from django.test import TestCase

from .base.test_social import BaseTestSocial


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestSocial(BaseTestSocial, TestCase):
    pass
