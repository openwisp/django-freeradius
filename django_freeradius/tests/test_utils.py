import os
from unittest import skipIf

from django.test import TestCase

from . import CreateRadiusObjectsMixin, FileMixin
from .base.test_utils import BaseTestUtils


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestUtils(BaseTestUtils, TestCase, CreateRadiusObjectsMixin, FileMixin):
    pass
