import os
from unittest import skipIf

from django.test import TestCase

from django_freeradius.models import (
    Nas, RadiusAccounting, RadiusBatch, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply,
    RadiusPostAuth, RadiusReply, RadiusToken, RadiusUserGroup,
)

from . import CreateRadiusObjectsMixin
from .base.test_models import (
    BaseTestNas, BaseTestRadiusAccounting, BaseTestRadiusBatch, BaseTestRadiusCheck, BaseTestRadiusGroup,
    BaseTestRadiusPostAuth, BaseTestRadiusReply, BaseTestRadiusToken,
)


class BaseTests(CreateRadiusObjectsMixin, TestCase):
    pass


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestNas(BaseTestNas, BaseTests):
    nas_model = Nas


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusAccounting(BaseTestRadiusAccounting, BaseTests):
    radius_accounting_model = RadiusAccounting


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusCheck(BaseTestRadiusCheck, BaseTests):
    radius_check_model = RadiusCheck


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusReply(BaseTestRadiusReply, BaseTests):
    radius_reply_model = RadiusReply


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroup(BaseTestRadiusGroup, BaseTests):
    radius_group_model = RadiusGroup
    radius_groupreply_model = RadiusGroupReply
    radius_groupcheck_model = RadiusGroupCheck
    radius_usergroup_model = RadiusUserGroup


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusPostAuth(BaseTestRadiusPostAuth, BaseTests):
    radius_postauth_model = RadiusPostAuth


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusBatch(BaseTestRadiusBatch, BaseTests):
    radius_batch_model = RadiusBatch


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusToken(BaseTestRadiusToken, BaseTests):
    radius_token_model = RadiusToken
