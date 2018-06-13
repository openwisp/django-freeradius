from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class BaseTestNas(object):
    def test_string_representation(self):
        nas = self.nas_model(name='entry nasname')
        self.assertEqual(str(nas), nas.name)


class BaseTestRadiusAccounting(object):
    def test_string_representation(self):
        radiusaccounting = self.radius_accounting_model(unique_id='entry acctuniqueid')
        self.assertEqual(str(radiusaccounting), radiusaccounting.unique_id)


class BaseTestRadiusCheck(object):
    def test_string_representation(self):
        radiuscheck = self.radius_check_model(username='entry username')
        self.assertEqual(str(radiuscheck), radiuscheck.username)


class BaseTestRadiusReply(object):
    def test_string_representation(self):
        radiusreply = self.radius_reply_model(username='entry username')
        self.assertEqual(str(radiusreply), radiusreply.username)


class BaseTestRadiusGroupReply(object):
    def test_string_representation(self):
        radiusgroupreply = self.radius_groupreply_model(groupname='entry groupname')
        self.assertEqual(str(radiusgroupreply), radiusgroupreply.groupname)


class BaseTestRadiusGroupCheck(object):
    def test_string_representation(self):
        radiusgroupcheck = self.radius_groupcheck_model(groupname='entry groupname')
        self.assertEqual(str(radiusgroupcheck), radiusgroupcheck.groupname)


class BaseTestRadiusUserGroup(object):
    def test_string_representation(self):
        radiususergroup = self.radius_usergroup_model(username='entry username')
        self.assertEqual(str(radiususergroup), radiususergroup.username)


class BaseTestRadiusPostAuth(object):
    def test_string_representation(self):
        radiuspostauthentication = self.radius_postauth_model(username='entry username')
        self.assertEqual(str(radiuspostauthentication), radiuspostauthentication.username)


class BaseTestRadiusGroup(object):
    def test_string_representation(self):
        radiusgroup = self.radius_group_model(groupname='entry groupname')
        self.assertEqual(str(radiusgroup), radiusgroup.groupname)


class BaseTestRadiusGroupUsersModel(object):
    def test_string_representation(self):
        radiusgroupusers = self.radius_groupusers_model(username='entry groupname')
        self.assertEqual(str(radiusgroupusers), radiusgroupusers.username)


class BaseTestRadiusBatchModel(object):
    def test_string_representation(self):
        radiusbatch = self.radius_batch_model(name='test')
        self.assertEqual(str(radiusbatch), 'test')

    def test_custom_queryset(self):
        radiusbatch = self.radius_batch_model.objects.create()
        User = get_user_model()
        for i in range(5):
            user = User.objects.create(username='rohith{}'.format(str(i)))
            user.set_password('password')
            user.save()
            radiusbatch.users.add(user)
        self.assertEqual(User.objects.all().count(), 5)
        radiusbatch.delete()
        self.assertEqual(self.radius_batch_model.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 0)

    def test_clean_method(self):
        radiusbatch = self.radius_batch_model.objects.create()
        with self.assertRaises(ValidationError):
            radiusbatch.full_clean()
        radiusbatch = self.radius_batch_model(strategy='csv', prefix='test',
                                              name='testing')
        with self.assertRaises(ValidationError):
            radiusbatch.full_clean()
