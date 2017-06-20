from django.test import TestCase
import swapper

RadiusGroupReply = swapper.load_model("django_freeradius", "RadiusGroupReply")
RadiusGroupCheck = swapper.load_model("django_freeradius", "RadiusGroupCheck")
RadiusGroupUsers = swapper.load_model("django_freeradius", "RadiusGroupUsers")
RadiusUserGroup = swapper.load_model("django_freeradius", "RadiusUserGroup")
RadiusReply = swapper.load_model("django_freeradius", "RadiusReply")
RadiusCheck = swapper.load_model("django_freeradius", "RadiusCheck")
RadiusPostAuthentication = swapper.load_model("django_freeradius", "RadiusPostAuthentication")
Nas = swapper.load_model("django_freeradius", "Nas")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
RadiusGroup = swapper.load_model("django_freeradius", "RadiusGroup")


class NasModelTest(TestCase):

    def test_string_representation(self):
        nas = Nas(nas_name='entry nasname')
        self.assertEqual(str(nas), nas.nas_name)


class RadiusAccountingModelTest(TestCase):

    def test_string_representation(self):
        radiusaccounting = RadiusAccounting(acct_unique_id='entry acctuniqueid')
        self.assertEqual(str(radiusaccounting), radiusaccounting.acct_unique_id)


class RadiusCheckModelTest(TestCase):

    def test_string_representation(self):
        radiuscheck = RadiusCheck(user_name='entry username')
        self.assertEqual(str(radiuscheck), radiuscheck.user_name)


class RadiusReplyModelTest(TestCase):

    def test_string_representation(self):
        radiusreply = RadiusReply(user_name='entry username')
        self.assertEqual(str(radiusreply), radiusreply.user_name)


class RadiusGroupReplyModelTest(TestCase):

    def test_string_representation(self):
        radiusgroupreply = RadiusGroupReply(group_name='entry groupname')
        self.assertEqual(str(radiusgroupreply), radiusgroupreply.group_name)


class RadiusGroupCheckModelTest(TestCase):

    def test_string_representation(self):
        radiusgroupcheck = RadiusGroupCheck(group_name='entry groupname')
        self.assertEqual(str(radiusgroupcheck), radiusgroupcheck.group_name)


class RadiusUserGroupModelTest(TestCase):

    def test_string_representation(self):
        radiususergroup = RadiusUserGroup(user_name='entry username')
        self.assertEqual(str(radiususergroup), radiususergroup.user_name)


class RadiusPostAuthenticationModelTest(TestCase):

    def test_string_representation(self):
        radiuspostauthentication = RadiusPostAuthentication(user_name='entry username')
        self.assertEqual(str(radiuspostauthentication), radiuspostauthentication.user_name)


class RadiusGroupModelTest(TestCase):

    def test_string_representation(self):
        radiusgroup = RadiusGroup(group_name='entry groupname')
        self.assertEqual(str(radiusgroup), radiusgroup.group_name)


class RadiusGroupUsersModelTest(TestCase):

    def test_string_representation(self):
        radiusgroupusers = RadiusGroupUsers(user_name='entry groupname')
        self.assertEqual(str(radiusgroupusers), radiusgroupusers.user_name)
