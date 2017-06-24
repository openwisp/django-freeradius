import os
from unittest import skipIf

from django.test import TestCase

from ..models import (Nas, RadiusAccounting, RadiusCheck, RadiusGroup,
                      RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
                      RadiusPostAuthentication, RadiusReply, RadiusUserGroup)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class NasModelTest(TestCase):

    def test_string_representation(self):
        nas = Nas(nas_name='entry nasname')
        self.assertEqual(str(nas), nas.nas_name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusAccountingModelTest(TestCase):

    def test_string_representation(self):
        radiusaccounting = RadiusAccounting(acct_unique_id='entry acctuniqueid')
        self.assertEqual(str(radiusaccounting), radiusaccounting.acct_unique_id)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusCheckModelTest(TestCase):

    def test_string_representation(self):
        radiuscheck = RadiusCheck(user_name='entry username')
        self.assertEqual(str(radiuscheck), radiuscheck.user_name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusReplyModelTest(TestCase):

    def test_string_representation(self):
        radiusreply = RadiusReply(user_name='entry username')
        self.assertEqual(str(radiusreply), radiusreply.user_name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusGroupReplyModelTest(TestCase):

    def test_string_representation(self):
        radiusgroupreply = RadiusGroupReply(group_name='entry groupname')
        self.assertEqual(str(radiusgroupreply), radiusgroupreply.group_name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusGroupCheckModelTest(TestCase):

    def test_string_representation(self):
        radiusgroupcheck = RadiusGroupCheck(group_name='entry groupname')
        self.assertEqual(str(radiusgroupcheck), radiusgroupcheck.group_name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusUserGroupModelTest(TestCase):

    def test_string_representation(self):
        radiususergroup = RadiusUserGroup(user_name='entry username')
        self.assertEqual(str(radiususergroup), radiususergroup.user_name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusPostAuthenticationModelTest(TestCase):

    def test_string_representation(self):
        radiuspostauthentication = RadiusPostAuthentication(user_name='entry username')
        self.assertEqual(str(radiuspostauthentication), radiuspostauthentication.user_name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusGroupModelTest(TestCase):

    def test_string_representation(self):
        radiusgroup = RadiusGroup(group_name='entry groupname')
        self.assertEqual(str(radiusgroup), radiusgroup.group_name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class RadiusGroupUsersModelTest(TestCase):

    def test_string_representation(self):
        radiusgroupusers = RadiusGroupUsers(user_name='entry groupname')
        self.assertEqual(str(radiusgroupusers), radiusgroupusers.user_name)
