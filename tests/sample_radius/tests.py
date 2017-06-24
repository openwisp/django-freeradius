import swapper
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from unittest import skipUnless
import os

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


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
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


class UserTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_users_not_login(self):
        resp = self.client.get('/admin/auth/')
        self.assertEqual(resp.status_code, 302)

    def test_users(self):
        self.client.login(username='gino', password='ciao')
        resp = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(resp.status_code, 200)

    def test_users_nas(self):
        User.objects.create_superuser(username='gino', password='cc', email='giggi_vv@gmail.it')
        obj = Nas.objects.create(
            nas_name='fiore', short_name='ff', type='cisco', secret='d', ports='22', community='vmv',
            description='ciao', server='jsjs', details='nb')
        self.client.login(username='gino', password='cc')
        resp = self.client.get(reverse('admin:sample_radius_nas_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_check(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusCheck.objects.create(
            user_name='bob', attribute='Cleartext-Password', op=':=', value='passbob', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiuscheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_reply(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusReply.objects.create(
            user_name='bob', attribute='Cleartext-Password', op=':=', value='passbob', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_group_reply(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusGroupReply.objects.create(
            group_name='students', attribute='Cleartext-Password', op=':=', value='PPP', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_group_check(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it')
        obj = RadiusGroupCheck.objects.create(
            group_name='students', attribute='Cleartext-Password', op=':=', value='PPP', details='nb')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupcheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_group(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusGroup.objects.create(
            id='870df8e8-3107-4487-8316-81e089b8c2cf', group_name='students', priority='1',
            creation_date='2017-09-02', modification_date='2017-08-03', notes='hh', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusgroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_usersgroup(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusUserGroup.objects.create(
            user_name='bob', group_name='students', priority='1', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiususergroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_groupusers(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        reply = RadiusReply.objects.create(
            user_name='bob', attribute='Cleartext-Password', op=':=', value='passbob')
        check = RadiusCheck.objects.create(
            user_name='bob', attribute='Cleartext-Password', op=':=', value='passbob')
        obj = RadiusGroupUsers.objects.create(
            id='870df8e8-3107-4487-8316-81e089b8c2cf', user_name='bob', group_name='students')
        obj.radius_reply.add(reply)
        obj.radius_check.add(check)
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupusers_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_accounting(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        ola = RadiusAccounting.objects.create(
            acct_unique_id='-2', user_name='bob', nas_ip_address='ff',
            acct_start_time='2012-09-04 06:00:00.000000-01:00',
            acct_stop_time='2012-09-04 06:00:00.000000-08:00', acct_session_time='5', acct_authentic='kj',
            connection_info_start='f', connection_info_stop='hgh',
            acct_input_octets='1', acct_output_octets='4', rad_acct_id='123', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusaccounting_change', args=[ola.pk]))
        self.assertContains(resp, 'ok')

    def test_users_postauthentication(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        olu = RadiusPostAuthentication.objects.create(
            user_name='gino', password='ciao', reply='ghdhd', auth_date='2017-09-02', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse(
            'admin:sample_radius_radiuspostauthentication_change', args=[olu.pk]))
        self.assertContains(resp, 'ok')
