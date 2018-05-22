import os
from unittest import skipIf

from django.test import TestCase

from ..models import RadiusAccounting, RadiusBatch, RadiusPostAuth
from .base.test_commands import BaseTestCommands


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestCommands(BaseTestCommands, TestCase):
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    radius_postauth_model = RadiusPostAuth
