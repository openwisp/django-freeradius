import os
from unittest import skipIf

from django.test import TestCase

from django_freeradius.models import (
    Nas, RadiusAccounting, RadiusBatch, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply,
    RadiusPostAuth, RadiusReply, RadiusToken, RadiusUserGroup,
)

from . import CallCommandMixin, CreateRadiusObjectsMixin, FileMixin, PostParamsMixin
from .base.test_admin import BaseTestAdmin


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestAdmin(FileMixin, CallCommandMixin, PostParamsMixin,
                CreateRadiusObjectsMixin, BaseTestAdmin, TestCase):
    app_name = "django_freeradius"
    nas_model = Nas
    radius_accounting_model = RadiusAccounting
    radius_batch_model = RadiusBatch
    radius_check_model = RadiusCheck
    radius_groupcheck_model = RadiusGroupCheck
    radius_groupreply_model = RadiusGroupReply
    radius_postauth_model = RadiusPostAuth
    radius_reply_model = RadiusReply
    radius_group_model = RadiusGroup
    radius_usergroup_model = RadiusUserGroup
    radius_token_model = RadiusToken
