import os
from unittest import skipUnless

import swapper
from django.test import TestCase

from django_freeradius.tests.base.test_admin import BaseTestAdmin
from django_freeradius.tests.base.test_batch_add_users import BaseTestCSVUpload
from django_freeradius.tests.base.test_commands import BaseTestCommands
from django_freeradius.tests.base.test_models import (
    BaseTestNas, BaseTestRadiusAccounting, BaseTestRadiusCheck, BaseTestRadiusGroup,
    BaseTestRadiusGroupCheck, BaseTestRadiusGroupReply, BaseTestRadiusGroupUsersModel,
    BaseTestRadiusPostAuth, BaseTestRadiusReply, BaseTestRadiusUserGroup,
)

RadiusGroupReply = swapper.load_model("django_freeradius", "RadiusGroupReply")
RadiusGroupCheck = swapper.load_model("django_freeradius", "RadiusGroupCheck")
RadiusGroupUsers = swapper.load_model("django_freeradius", "RadiusGroupUsers")
RadiusUserGroup = swapper.load_model("django_freeradius", "RadiusUserGroup")
RadiusReply = swapper.load_model("django_freeradius", "RadiusReply")
RadiusCheck = swapper.load_model("django_freeradius", "RadiusCheck")
RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
Nas = swapper.load_model("django_freeradius", "Nas")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
RadiusGroup = swapper.load_model("django_freeradius", "RadiusGroup")
RadiusBatch = swapper.load_model("django_freeradius", "RadiusBatch")


_SUPERUSER = {'username': 'gino', 'password': 'cic', 'email': 'giggi_vv@gmail.it'}
_RADCHECK_ENTRY = {'username': 'Monica', 'value': 'Cam0_liX',
                   'attribute': 'NT-Password'}
_RADCHECK_ENTRY_PW_UPDATE = {'username': 'Monica', 'new_value': 'Cam0_liX',
                             'attribute': 'NT-Password'}


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestNas(BaseTestNas, TestCase):
    nas_model = Nas


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusAccounting(BaseTestRadiusAccounting, TestCase):
    radius_accounting_model = RadiusAccounting


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusCheckModelTest(BaseTestRadiusCheck, TestCase):
    radius_check_model = RadiusCheck


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusReplyModelTest(BaseTestRadiusReply, TestCase):
    radius_reply_model = RadiusReply


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroupReplyModelTest(BaseTestRadiusGroupReply, TestCase):
    radius_groupreply_model = RadiusGroupReply


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroupCheckModelTest(BaseTestRadiusGroupCheck, TestCase):
    radius_groupcheck_model = RadiusGroupCheck


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusUserGroupModelTest(BaseTestRadiusUserGroup, TestCase):
    radius_usergroup_model = RadiusUserGroup


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusPostAuthModelTest(BaseTestRadiusPostAuth, TestCase):
    radius_postauth_model = RadiusPostAuth


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroupModelTest(BaseTestRadiusGroup, TestCase):
    radius_group_model = RadiusGroup


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroupUsersModelTest(BaseTestRadiusGroupUsersModel, TestCase):
    radius_groupusers_model = RadiusGroupUsers


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestAdmin(BaseTestAdmin, TestCase):
    app_name = "sample_radius"
    nas_model = Nas
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    radius_check_model = RadiusCheck
    radius_group_model = RadiusGroup
    radius_groupcheck_model = RadiusGroupCheck
    radius_groupreply_model = RadiusGroupReply
    radius_groupusers_model = RadiusGroupUsers
    radius_postauth_model = RadiusPostAuth
    radius_reply_model = RadiusReply
    radius_usergroup_model = RadiusUserGroup


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestCommands(BaseTestCommands, TestCase):
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    radius_postauth_model = RadiusPostAuth


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestCSVUpload(BaseTestCSVUpload, TestCase):
    radius_batch_model = RadiusBatch
