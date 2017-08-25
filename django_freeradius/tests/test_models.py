import os
from unittest import skipIf

from django.test import TestCase

from ..models import (
    Nas, RadiusAccounting, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
    RadiusPostAuth, RadiusReply, RadiusUserGroup,
)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestNas(TestCase):
    def test_string_representation(self):
        nas = Nas(name='entry nasname')
        self.assertEqual(str(nas), nas.name)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusAccounting(TestCase):
    def test_string_representation(self):
        radiusaccounting = RadiusAccounting(unique_id='entry acctuniqueid')
        self.assertEqual(str(radiusaccounting), radiusaccounting.unique_id)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusCheck(TestCase):
    def test_string_representation(self):
        radiuscheck = RadiusCheck(username='entry username')
        self.assertEqual(str(radiuscheck), radiuscheck.username)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusReply(TestCase):
    def test_string_representation(self):
        radiusreply = RadiusReply(username='entry username')
        self.assertEqual(str(radiusreply), radiusreply.username)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroupReply(TestCase):
    def test_string_representation(self):
        radiusgroupreply = RadiusGroupReply(groupname='entry groupname')
        self.assertEqual(str(radiusgroupreply), radiusgroupreply.groupname)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroupCheck(TestCase):
    def test_string_representation(self):
        radiusgroupcheck = RadiusGroupCheck(groupname='entry groupname')
        self.assertEqual(str(radiusgroupcheck), radiusgroupcheck.groupname)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusUserGroup(TestCase):
    def test_string_representation(self):
        radiususergroup = RadiusUserGroup(username='entry username')
        self.assertEqual(str(radiususergroup), radiususergroup.username)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusPostAuth(TestCase):
    def test_string_representation(self):
        radiuspostauthentication = RadiusPostAuth(username='entry username')
        self.assertEqual(str(radiuspostauthentication), radiuspostauthentication.username)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroup(TestCase):
    def test_string_representation(self):
        radiusgroup = RadiusGroup(groupname='entry groupname')
        self.assertEqual(str(radiusgroup), radiusgroup.groupname)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestRadiusGroupUsersModel(TestCase):
    def test_string_representation(self):
        radiusgroupusers = RadiusGroupUsers(username='entry groupname')
        self.assertEqual(str(radiusgroupusers), radiusgroupusers.username)
