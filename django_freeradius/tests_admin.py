from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
import unittest
from .models import (Nas, RadiusAccounting, RadiusCheck, RadiusGroup,
                     RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
                     RadiusPostAuthentication, RadiusReply, RadiusUserGroup)


class UserTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_users_not_login(self):
        resp = self.client.get('/admin/auth/')
        self.assertEqual(resp.status_code, 302)

    def test_users(self):
        self.client.login(username='fiorella', password='milafiore91')
        resp = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(resp.status_code, 200)

    def setUp(self):
        self.client = Client()

    def test_users_nas(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it')
        Nas.objects.create(nas_name='fiore', short_name='ff', type='cisco', secret='d', ports='22', community='vmv', description='ciao', server='jsjs')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/django_freeradius/nas/1/change/')
        self.assertContains(resp,'ok')#(reverse('admin:django_freeradius_nas_change', args=[nas.id])

    def test_users_check(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it')
        RadiusCheck.objects.create(user_name='bob', attribute='Cleartext-Password', op=':=', value='passbob')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.post('/admin/django_freeradius/radiuscheck/1/change/')
        self.assertContains(resp,'ok')

    def test_users_reply(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it' )
        RadiusReply.objects.create(user_name='bob', attribute='Cleartext-Password', op=':=', value='passbob')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/django_freeradius/radiusreply/1/change/')
        self.assertContains(resp,'ok')

    def test_users_group_reply(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it' )
        RadiusGroupReply.objects.create(group_name='students', attribute='Cleartext-Password', op=':=', value='PPP')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/django_freeradius/radiusgroupreply/1/change/')
        self.assertContains(resp,'ok')

    def test_users_group_check(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it' )
        RadiusGroupCheck.objects.create(group_name='students', attribute='Cleartext-Password', op=':=', value='PPP')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/django_freeradius/radiusgroupcheck/1/change/')
        self.assertContains(resp,'ok')

    def test_users_group(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it')
        RadiusGroup.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf', group_name='students', priority='1', creation_date='2017-09-02', modification_date='2017-08-03', notes='hh')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/django_freeradius/radiusgroup/1/change/')
        self.assertContains(resp,'ok')

    def test_users_usersgroup(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it' )
        RadiusUserGroup.objects.create(user_name='bob', group_name='students', priority='1')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/django_freeradius/radiususergroup/1/change/')
        self.assertContains(resp,'ok')

    def test_users_groupusers(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it' )
        RadiusGroupUsers.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',user_name='bob', group_name='students', radius_reply='bob', radius_check='bob')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/django_freeradius/radiusgroupusers/1/change/')
        self.assertContains(resp,'ok')

    def test_users_accounting(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it' )
        RadiusAccounting.objects.create(
        acct_unique_id='-2', user_name='bob', nas_ip_address='ff', acct_start_time='2017-03-05 08:50', acct_stop_time='2017-09-04 09:10', acct_session_time='5', acct_authentic='kj', connection_info_start='f', connection_info_stop='hgh', acct_input_octets='1' ,acct_output_octets='4', rad_acct_id='870df8e8-3107-4487-8316-81e089b8c2cf')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/django_freeradius/radiusaccounting/1/change/')
        self.assertContains(resp,'ok')
