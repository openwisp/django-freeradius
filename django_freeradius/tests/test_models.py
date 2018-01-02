import os
from unittest import skipIf

from django.test import TestCase

from django_freeradius.models import (
    Nas, RadiusAccounting, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
    RadiusPostAuth, RadiusReply, RadiusUserGroup,
)

from .base.test_models import (
    BaseTestNas, BaseTestRadiusAccounting, BaseTestRadiusCheck, BaseTestRadiusGroup,
    BaseTestRadiusGroupCheck, BaseTestRadiusGroupReply, BaseTestRadiusGroupUsersModel,
    BaseTestRadiusPostAuth, BaseTestRadiusReply, BaseTestRadiusUserGroup,
)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestNas(BaseTestNas, TestCase):
    nas_model = Nas


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusAccounting(BaseTestRadiusAccounting, TestCase):
    radius_accounting_model = RadiusAccounting


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusCheck(BaseTestRadiusCheck, TestCase):
    radius_check_model = RadiusCheck


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusReply(BaseTestRadiusReply, TestCase):
    radius_reply_model = RadiusReply


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroupReply(BaseTestRadiusGroupReply, TestCase):
    radius_groupreply_model = RadiusGroupReply


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroupCheck(BaseTestRadiusGroupCheck, TestCase):
    radius_groupcheck_model = RadiusGroupCheck


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusUserGroup(BaseTestRadiusUserGroup, TestCase):
    radius_usergroup_model = RadiusUserGroup


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusPostAuth(BaseTestRadiusPostAuth, TestCase):
    radius_postauth_model = RadiusPostAuth


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroup(BaseTestRadiusGroup, TestCase):
    radius_group_model = RadiusGroup


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroupUsersModel(BaseTestRadiusGroupUsersModel, TestCase):
    radius_groupusers_model = RadiusGroupUsers
