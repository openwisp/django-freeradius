from django.test import TestCase
from .models import (Nas, RadiusAccounting, RadiusCheck, RadiusGroup,
                     RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
                     RadiusPostAuthentication, RadiusReply, RadiusUserGroup)



class Nas(TestCase):

    def test_string_representation(self):
        nas = Nas(nas_name='entry nasname')
        self.assertEqual(str(nas), nas.nas_name)

class RadiusAccounting(TestCase):

    def test_string_representation(self):
        radiusaccounting = RadiusAccounting(acct_unique_id='entry acctuniqueid')
        self.assertEqual(str(radiusaccounting), radiusaccounting.acct_unique_id)

class RadiusCheck(TestCase):

    def test_string_representation(self):
        radiuscheck = RadiusCheck(user_name='entry username')
        self.assertEqual(str(radiuscheck), radiuscheck.user_name)

class RadiusReply(TestCase):

    def test_string_representation(self):
        radiusreply = RadiusReply(user_name='entry username')
        self.assertEqual(str(radiusreply), radiusreply.user_name)

class RadiusGroupReply(TestCase):

    def test_string_representation(self):
        radiusgroupreply = RadiusGroupReply(group_name='entry groupname')
        self.assertEqual(str(radiusgroupreply), radiusgroupreply.group_name)

class RadiusGroupCheck(TestCase):

    def test_string_representation(self):
        radiusgroupcheck = RadiusGroupCheck(group_name='entry groupname')
        self.assertEqual(str(radiusgroupcheck), radiusgroupcheck.group_name)


class RadiusUserGroup(TestCase):

    def test_string_representation(self):
        radiususergroup = RadiusUserGroup(user_name='entry username')
        self.assertEqual(str(radiususergroup), radiususergroup.user_name)


class RadiusPostAuthentication(TestCase):

    def test_string_representation(self):
        radiuspostauthentication = RadiusPostAuthentication(user_name='entry username')
        self.assertEqual(str(radiuspostauthentication), radiuspostauthentication.user_name)

class RadiusGroup(TestCase):

    def test_string_representation(self):
        radiusgroup = RadiusGroup(group_name='entry groupname')
        self.assertEqual(str(radiusgroup), radiusgroup.group_name)

class RadiusGroupUsers(TestCase):

    def test_string_representation(self):
        radiusgroupusers = RadiusGroupUsers(group_name='entry groupname')
        self.assertEqual(str(radiusgroupusers), radiusgroupusers.group_name)
