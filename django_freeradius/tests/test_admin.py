import os
from unittest import skipIf

from django.test import TestCase

from django_freeradius.models import (
    Nas, RadiusAccounting, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
    RadiusPostAuth, RadiusReply, RadiusUserGroup,
)

from .base.test_admin import BaseTestAdmin


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestAdmin(BaseTestAdmin, TestCase):
    app_name = "django_freeradius"
    nas_model = Nas
    radius_accounting_model = RadiusAccounting
    radius_check_model = RadiusCheck
    radius_group_model = RadiusGroup
    radius_groupcheck_model = RadiusGroupCheck
    radius_groupreply_model = RadiusGroupReply
    radius_groupusers_model = RadiusGroupUsers
    radius_postauth_model = RadiusPostAuth
    radius_reply_model = RadiusReply
    radius_usergroup_model = RadiusUserGroup
