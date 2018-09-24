import os
from unittest import skipUnless

import swapper
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from django_freeradius.tests import ApiParamsMixin, CallCommandMixin, CreateRadiusObjectsMixin, FileMixin
from django_freeradius.tests.base.test_admin import BaseTestAdmin
from django_freeradius.tests.base.test_api import BaseTestApi, BaseTestApiReject
from django_freeradius.tests.base.test_batch_add_users import BaseTestCSVUpload
from django_freeradius.tests.base.test_commands import BaseTestCommands
from django_freeradius.tests.base.test_models import (
    BaseTestNas, BaseTestRadiusAccounting, BaseTestRadiusBatch, BaseTestRadiusCheck, BaseTestRadiusGroup,
    BaseTestRadiusPostAuth, BaseTestRadiusReply,
)
from django_freeradius.tests.base.test_utils import BaseTestUtils

RadiusGroup = swapper.load_model('django_freeradius', 'RadiusGroup')
RadiusGroupReply = swapper.load_model('django_freeradius', 'RadiusGroupReply')
RadiusGroupCheck = swapper.load_model('django_freeradius', 'RadiusGroupCheck')
RadiusUserGroup = swapper.load_model('django_freeradius', 'RadiusUserGroup')
RadiusReply = swapper.load_model('django_freeradius', 'RadiusReply')
RadiusCheck = swapper.load_model('django_freeradius', 'RadiusCheck')
RadiusPostAuth = swapper.load_model('django_freeradius', 'RadiusPostAuth')
Nas = swapper.load_model('django_freeradius', 'Nas')
RadiusAccounting = swapper.load_model('django_freeradius', 'RadiusAccounting')
RadiusBatch = swapper.load_model('django_freeradius', 'RadiusBatch')


_SUPERUSER = {'username': 'gino', 'password': 'cic', 'email': 'giggi_vv@gmail.it'}
_RADCHECK_ENTRY = {'username': 'Monica', 'value': 'Cam0_liX',
                   'attribute': 'NT-Password'}
_RADCHECK_ENTRY_PW_UPDATE = {'username': 'Monica', 'new_value': 'Cam0_liX',
                             'attribute': 'NT-Password'}


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestNas(BaseTestNas, TestCase, CreateRadiusObjectsMixin):
    nas_model = Nas


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusAccounting(BaseTestRadiusAccounting, TestCase, CreateRadiusObjectsMixin):
    radius_accounting_model = RadiusAccounting


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusCheck(BaseTestRadiusCheck, TestCase, CreateRadiusObjectsMixin):
    radius_check_model = RadiusCheck


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusReply(BaseTestRadiusReply, TestCase, CreateRadiusObjectsMixin):
    radius_reply_model = RadiusReply


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroup(BaseTestRadiusGroup, TestCase, CreateRadiusObjectsMixin):
    radius_group_model = RadiusGroup
    radius_groupcheck_model = RadiusGroupCheck
    radius_groupreply_model = RadiusGroupReply
    radius_usergroup_model = RadiusUserGroup


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusPostAuth(BaseTestRadiusPostAuth, TestCase, CreateRadiusObjectsMixin):
    radius_postauth_model = RadiusPostAuth


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusBatch(BaseTestRadiusBatch, TestCase, CreateRadiusObjectsMixin):
    radius_batch_model = RadiusBatch


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestAdmin(BaseTestAdmin, TestCase, CreateRadiusObjectsMixin,
                FileMixin, CallCommandMixin):
    app_name = 'sample_radius'
    nas_model = Nas
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    radius_check_model = RadiusCheck
    radius_groupcheck_model = RadiusGroupCheck
    radius_groupreply_model = RadiusGroupReply
    radius_postauth_model = RadiusPostAuth
    radius_reply_model = RadiusReply
    radius_usergroup_model = RadiusUserGroup
    radius_group_model = RadiusGroup


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestApi(BaseTestApi, TestCase, CreateRadiusObjectsMixin, ApiParamsMixin):
    radius_postauth_model = RadiusPostAuth
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    user_model = get_user_model()
    auth_header = 'Bearer {}'.format(settings.DJANGO_FREERADIUS_API_TOKEN)
    token_querystring = '?token={}'.format(settings.DJANGO_FREERADIUS_API_TOKEN)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestCommands(BaseTestCommands, TestCase, CreateRadiusObjectsMixin,
                   FileMixin, CallCommandMixin):
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    radius_postauth_model = RadiusPostAuth


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestCSVUpload(BaseTestCSVUpload, TestCase,
                    CreateRadiusObjectsMixin, FileMixin):
    radius_batch_model = RadiusBatch


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestUtils(BaseTestUtils, TestCase, CreateRadiusObjectsMixin, FileMixin):
    pass


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestApiReject(BaseTestApiReject, TestCase, CreateRadiusObjectsMixin):
    auth_header = 'Bearer {}'.format(settings.DJANGO_FREERADIUS_API_TOKEN)
