import os
from unittest import skipIf

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ..models import (
    Nas, RadiusAccounting, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
    RadiusPostAuthentication, RadiusReply, RadiusUserGroup,
)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestAdmin(TestCase):
    def test_users_not_login(self):
        resp = self.client.get('/admin/auth/')
        self.assertEqual(resp.status_code, 302)

    def test_users(self):
        self.client.login(username='gino', password='ciao')
        resp = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(resp.status_code, 200)

    def test_users_nas(self):
        User.objects.create_superuser(username='gino', password='cc', email='giggi_vv@gmail.it')
        obj = Nas.objects.create(name='fiore', short_name='ff', type='cisco',
                                 secret='d', ports='22', community='vmv',
                                 description='ciao', server='jsjs')
        self.client.login(username='gino', password='cc')
        resp = self.client.get(reverse('admin:django_freeradius_nas_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_check(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusCheck.objects.create(username='bob', attribute='Cleartext-Password',
                                         op=':=', value='passbob')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiuscheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_reply(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                         op=':=', value='passbob')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_group_reply(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusGroupReply.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusgroupreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_group_check(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it')
        obj = RadiusGroupCheck.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get(reverse('admin:django_freeradius_radiusgroupcheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_group(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusGroup.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                         groupname='students', priority='1', notes='hh')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusgroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_usersgroup(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusUserGroup.objects.create(username='bob', groupname='students', priority='1')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiususergroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_groupusers(self):
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
        resp = self.client.get(reverse('admin:django_freeradius_radiusgroupusers_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_users_accounting(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        ola = RadiusAccounting.objects.create(
            acct_unique_id='-2', username='bob', nas_ip_address='ff', acct_start_time='2017-06-10 10:50:00',
            acct_stop_time='2017-06-10 11:50:00', acct_session_time='5', acct_authentic='kj',
            connection_info_start='f', connection_info_stop='hgh',
            acct_input_octets='1', acct_output_octets='4', rad_acct_id='123'
        )
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusaccounting_change', args=[ola.pk]))
        self.assertContains(resp, 'ok')

    def test_users_postauthentication(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        olu = RadiusPostAuthentication.objects.create(username='gino', password='ciao',
                                                      reply='ghdhd', auth_date='2017-09-02')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiuspostauthentication_change', args=[olu.pk]))
        self.assertContains(resp, 'ok')
