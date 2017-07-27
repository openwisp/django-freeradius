import os
from unittest import skipUnless

import swapper
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

RadiusGroupReply = swapper.load_model("django_freeradius", "RadiusGroupReply")
RadiusGroupCheck = swapper.load_model("django_freeradius", "RadiusGroupCheck")
RadiusGroupUsers = swapper.load_model("django_freeradius", "RadiusGroupUsers")
RadiusUserGroup = swapper.load_model("django_freeradius", "RadiusUserGroup")
RadiusReply = swapper.load_model("django_freeradius", "RadiusReply")
RadiusCheck = swapper.load_model("django_freeradius", "RadiusCheck")
RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
Nas = swapper.load_model("django_freeradius", "Nas")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
RadiusGroup = swapper.load_model("django_freeradius", "RadiusGroup")


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestNas(TestCase):
    def test_string_representation(self):
        nas = Nas(name='entry nasname')
        self.assertEqual(str(nas), nas.name)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusAccounting(TestCase):
    def test_string_representation(self):
        radiusaccounting = RadiusAccounting(unique_id='entry acctuniqueid')
        self.assertEqual(str(radiusaccounting), radiusaccounting.unique_id)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusCheckModelTest(TestCase):
    def test_string_representation(self):
        radiuscheck = RadiusCheck(username='entry username')
        self.assertEqual(str(radiuscheck), radiuscheck.username)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusReplyModelTest(TestCase):
    def test_string_representation(self):
        radiusreply = RadiusReply(username='entry username')
        self.assertEqual(str(radiusreply), radiusreply.username)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroupReplyModelTest(TestCase):
    def test_string_representation(self):
        radiusgroupreply = RadiusGroupReply(groupname='entry groupname')
        self.assertEqual(str(radiusgroupreply), radiusgroupreply.groupname)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroupCheckModelTest(TestCase):
    def test_string_representation(self):
        radiusgroupcheck = RadiusGroupCheck(groupname='entry groupname')
        self.assertEqual(str(radiusgroupcheck), radiusgroupcheck.groupname)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusUserGroupModelTest(TestCase):
    def test_string_representation(self):
        radiususergroup = RadiusUserGroup(username='entry username')
        self.assertEqual(str(radiususergroup), radiususergroup.username)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusPostAuthModelTest(TestCase):
    def test_string_representation(self):
        radiuspostauthentication = RadiusPostAuth(username='entry username')
        self.assertEqual(str(radiuspostauthentication), radiuspostauthentication.username)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroupModelTest(TestCase):
    def test_string_representation(self):
        radiusgroup = RadiusGroup(groupname='entry groupname')
        self.assertEqual(str(radiusgroup), radiusgroup.groupname)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestRadiusGroupUsersModelTest(TestCase):
    def test_string_representation(self):
        radiusgroupusers = RadiusGroupUsers(username='entry groupname')
        self.assertEqual(str(radiusgroupusers), radiusgroupusers.username)


@skipUnless(os.environ.get('SAMPLE_APP', False), 'Running tests on standard django_freeradius models')
class TestAdmin(TestCase):
    def test_users_not_login(self):
        resp = self.client.get('/admin/auth/')
        self.assertEqual(resp.status_code, 302)

    def test_users(self):
        self.client.login(username='gino', password='ciao')
        resp = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(resp.status_code, 200)

    def test_radius_nas_change(self):
        User.objects.create_superuser(username='gino', password='cc', email='giggi_vv@gmail.it')
        obj = Nas.objects.create(name='fiore', short_name='ff', type='cisco',
                                 secret='d', ports='22', community='vmv',
                                 description='ciao', server='jsjs', details='nb')
        self.client.login(username='gino', password='cc')
        resp = self.client.get(reverse('admin:sample_radius_nas_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiuscheck_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusCheck.objects.create(username='bob', attribute='Cleartext-Password',
                                         op=':=', value='passbob', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiuscheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusreply_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                         op=':=', value='passbob', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupreply_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusGroupReply.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupcheck_change(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it')
        obj = RadiusGroupCheck.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP', details='nb')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupcheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroup_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusGroup.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                         groupname='students', priority='1',
                                         notes='hh', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusgroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiususergroup_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusUserGroup.objects.create(username='bob', groupname='students',
                                             priority='1', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiususergroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupusers_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        reply = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                           op=':=', value='passbob')
        check = RadiusCheck.objects.create(username='bob', attribute='Cleartext-Password',
                                           op=':=', value='passbob')
        obj = RadiusGroupUsers.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                              username='bob', groupname='students')
        obj.radius_reply.add(reply)
        obj.radius_check.add(check)
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupusers_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusaccounting_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        ola = RadiusAccounting.objects.create(
            unique_id='-2', username='bob', nas_ip_address='127.0.0.1',
            start_time='2012-09-04 06:00:00.000000-01:00',
            stop_time='2012-09-04 06:00:00.000000-08:00', session_time='5', authentication='FreeRADIUS',
            connection_info_start='f', connection_info_stop='hgh',
            input_octets='1', output_octets='4', details='nb',
            update_time='2012-09-06 11:50'
        )
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusaccounting_change', args=[ola.pk]))
        self.assertContains(resp, 'ok')

    def test_radiuspostauth_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        olu = RadiusPostAuth.objects.create(username='gino', password='ciao', reply='ghdhd',
                                            date='2017-09-02', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiuspostauth_change', args=[olu.pk]))
        self.assertContains(resp, 'ok')
