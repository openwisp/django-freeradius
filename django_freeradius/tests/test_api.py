import swapper
from django.test import TestCase

from .base.test_api import BaseTestApi

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")


class TestApi(BaseTestApi, TestCase):
    radius_postauth_model = RadiusPostAuth
    radius_accounting_model = RadiusAccounting
