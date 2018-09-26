import os
from unittest import skipIf

import swapper
from django.contrib.auth import get_user_model
from django.test import TestCase

from django_freeradius import settings as app_settings

from . import CreateRadiusObjectsMixin, PostParamsMixin
from .base.test_api import BaseTestApi, BaseTestApiReject

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
RadiusBatch = swapper.load_model("django_freeradius", "RadiusBatch")


class ApiTestCase(PostParamsMixin, CreateRadiusObjectsMixin, TestCase):
    pass


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestApi(BaseTestApi, ApiTestCase):
    radius_postauth_model = RadiusPostAuth
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    user_model = get_user_model()
    auth_header = "Bearer {}".format(app_settings.API_TOKEN)
    token_querystring = "?token={}".format(app_settings.API_TOKEN)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestApiReject(BaseTestApiReject, ApiTestCase):
    auth_header = "Bearer {}".format(app_settings.API_TOKEN)
    token_querystring = "?token={}".format(app_settings.API_TOKEN)
