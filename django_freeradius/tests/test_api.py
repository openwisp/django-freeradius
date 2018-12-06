import os
from unittest import skipIf

import swapper
from django.contrib.auth import get_user_model
from django.test import TestCase

from . import CreateRadiusObjectsMixin, PostParamsMixin
from .. import settings as app_settings
from ..models import RadiusUserGroup
from .base.test_api import BaseTestApi, BaseTestApiReject

RadiusPostAuth = swapper.load_model('django_freeradius', 'RadiusPostAuth')
RadiusAccounting = swapper.load_model('django_freeradius', 'RadiusAccounting')
RadiusBatch = swapper.load_model('django_freeradius', 'RadiusBatch')


class ApiTestCase(PostParamsMixin, CreateRadiusObjectsMixin, TestCase):
    pass


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestApi(BaseTestApi, ApiTestCase):
    radius_postauth_model = RadiusPostAuth
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    user_model = get_user_model()
    radius_usergroup_model = RadiusUserGroup
    auth_header = 'Bearer {}'.format(app_settings.API_TOKEN)
    token_querystring = '?token={}'.format(app_settings.API_TOKEN)

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()
        app_settings.API_ACCOUNTING_AUTO_GROUP = True

    def test_automatic_groupname_account_enabled(self):
        user = self.user_model.objects.create_superuser(
            username='username1', email='admin@admin.com', password='qwertyuiop'
        )
        usergroup1 = self._create_radius_usergroup(groupname='group1', priority=2, username='testgroup1')
        usergroup2 = self._create_radius_usergroup(groupname='group2', priority=1, username='testgroup2')
        user.radiususergroup_set.set([usergroup1, usergroup2])
        self.client.post('/api/v1/accounting/{}'.format(self.token_querystring), {
            'status_type': 'Start',
            'session_time': '',
            'input_octets': '',
            'output_octets': '',
            'nas_ip_address': '127.0.0.1',
            'session_id': '48484',
            'unique_id': '1515151',
            'username': 'username1',
        })
        accounting_created = self.radius_accounting_model.objects.get(username='username1')
        self.assertEquals(accounting_created.groupname, 'group2')
        user.delete()


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestApiReject(BaseTestApiReject, ApiTestCase):
    auth_header = 'Bearer {}'.format(app_settings.API_TOKEN)
    token_querystring = '?token={}'.format(app_settings.API_TOKEN)


class TestAutomaticGroupnameSetting(ApiTestCase):
    radius_accounting_model = RadiusAccounting
    user_model = get_user_model()
    radius_usergroup_model = RadiusUserGroup
    auth_header = 'Bearer {}'.format(app_settings.API_TOKEN)
    token_querystring = '?token={}'.format(app_settings.API_TOKEN)

    @classmethod
    def setUpClass(cls):
        super(TestAutomaticGroupnameSetting, cls).setUpClass()
        app_settings.API_ACCOUNTING_AUTO_GROUP = False

    def test_account_creation_api_automatic_groupname_disabled(self):
        user = self.user_model.objects.create_superuser(
            username='username1', email='admin@admin.com', password='qwertyuiop'
        )
        usergroup1 = self._create_radius_usergroup(groupname='group1', priority=2, username='testgroup1')
        usergroup2 = self._create_radius_usergroup(groupname='group2', priority=1, username='testgroup2')
        user.radiususergroup_set.set([usergroup1, usergroup2])
        self.client.post('/api/v1/accounting/{}'.format(self.token_querystring), {
            'status_type': 'Start',
            'session_time': '',
            'input_octets': '',
            'output_octets': '',
            'nas_ip_address': '127.0.0.1',
            'session_id': '48484',
            'unique_id': '1515151',
            'username': 'username1',
        })
        accounting_created = self.radius_accounting_model.objects.get(username='username1')
        self.assertIsNone(accounting_created.groupname)
        user.delete()
