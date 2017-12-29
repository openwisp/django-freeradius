import os
from copy import copy
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

_SUPERUSER = {'username': 'gino', 'password': 'cic', 'email': 'giggi_vv@gmail.it'}
_RADCHECK_ENTRY = {'username': 'Monica', 'value': 'Cam0_liX',
                   'attribute': 'NT-Password'}
_RADCHECK_ENTRY_PW_UPDATE = {'username': 'Monica', 'new_value': 'Cam0_liX',
                             'attribute': 'NT-Password'}


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
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(resp.status_code, 200)

    def test_radius_nas_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        obj = Nas.objects.create(name='fiore', short_name='ff', type='cisco',
                                 secret='d', ports='22', community='vmv',
                                 description='ciao', server='jsjs', details='nb')
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get(reverse('admin:sample_radius_nas_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusreply_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        obj = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                         op=':=', value='passbob', details='nb')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:sample_radius_radiusreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupreply_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        obj = RadiusGroupReply.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP', details='nb')
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupcheck_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        obj = RadiusGroupCheck.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP', details='nb')
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupcheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroup_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        obj = RadiusGroup.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                         groupname='students', priority='1',
                                         notes='hh', details='nb')
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get(reverse('admin:sample_radius_radiusgroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiususergroup_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        obj = RadiusUserGroup.objects.create(username='bob', groupname='students',
                                             priority='1', details='nb')
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get(reverse('admin:sample_radius_radiususergroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupusers_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        reply = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                           op=':=', value='passbob')
        check = RadiusCheck.objects.create(username='bob', attribute='Cleartext-Password',
                                           op=':=', value='passbob')
        obj = RadiusGroupUsers.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                              username='bob', groupname='students')
        obj.radius_reply.add(reply)
        obj.radius_check.add(check)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get(reverse('admin:sample_radius_radiusgroupusers_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusaccounting_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        ola = RadiusAccounting.objects.create(
            unique_id='-2', username='bob', nas_ip_address='127.0.0.1',
            start_time='2012-09-04 06:00:00.000000-01:00',
            stop_time='2012-09-04 06:00:00.000000-08:00', session_time='5', authentication='FreeRADIUS',
            connection_info_start='f', connection_info_stop='hgh',
            input_octets='1', output_octets='4', details='nb',
            update_time='2012-09-06 11:50'
        )
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get(reverse('admin:sample_radius_radiusaccounting_change', args=[ola.pk]))
        self.assertContains(resp, 'ok')

    def test_radiuspostauth_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        olu = RadiusPostAuth.objects.create(username='gino', password='ciao', reply='ghdhd',
                                            date='2017-09-02', details='nb')
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        resp = self.client.get(reverse('admin:sample_radius_radiuspostauth_change', args=[olu.pk]))
        self.assertContains(resp, 'ok')

    def test_radiuscheck_change(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        obj = RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        _RADCHECK = copy(_RADCHECK_ENTRY_PW_UPDATE)
        _RADCHECK['attribute'] = 'Cleartext-Password'
        RadiusCheck.objects.create(**_RADCHECK)
        _RADCHECK['attribute'] = 'LM-Password'
        RadiusCheck.objects.create(**_RADCHECK)
        _RADCHECK['attribute'] = 'NT-Password'
        RadiusCheck.objects.create(**_RADCHECK)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        response = self.client.post(reverse('admin:sample_radius_radiuscheck_change', args=[obj.pk]),
                                    _RADCHECK_ENTRY_PW_UPDATE, follow=True)
        self.assertContains(response, 'ok')

    def test_radiuscheck_create_weak_passwd(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        _RADCHECK = copy(_RADCHECK_ENTRY_PW_UPDATE)
        _RADCHECK['new_value'] = ''
        resp = self.client.post(reverse('admin:sample_radius_radiuscheck_add'),
                                _RADCHECK, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_create_disabled_hash(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        _RADCHECK = copy(_RADCHECK_ENTRY_PW_UPDATE)
        _RADCHECK['attribute'] = 'Cleartext-Password'
        response = self.client.post(reverse('admin:sample_radius_radiuscheck_add'),
                                    _RADCHECK, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_radiuscheck_admin_save_model(self):
        obj = RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        change_url = reverse('admin:sample_radius_radiuscheck_change', args=[obj.pk])
        # test admin save_model method
        data = _RADCHECK_ENTRY_PW_UPDATE
        data['op'] = ':='
        response = self.client.post(change_url, data, follow=True)
        # test also invalid password
        data = _RADCHECK_ENTRY_PW_UPDATE
        data['new_value'] = 'cionfrazZ'
        response = self.client.post(change_url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_radiuscheck_enable_disable_action(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        checks = RadiusCheck.objects.all().values_list('pk', flat=True)
        change_url = reverse('admin:sample_radius_radiuscheck_changelist')
        data = {'action': 'enable_action',
                '_selected_action': checks}
        self.client.post(change_url, data, follow=True)
        data = {'action': 'disable_action',
                '_selected_action': checks}
        self.client.post(change_url, data, follow=True)
        self.assertEqual(RadiusCheck.objects.filter(is_active=True).count(), 0)

    def test_radiuscheck_filter_duplicates_username(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        url = reverse('admin:sample_radius_radiuscheck_changelist')+'?duplicates=username'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_duplicates_value(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        url = reverse('admin:sample_radius_radiuscheck_changelist')+'?duplicates=value'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_expired(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        url = reverse('admin:sample_radius_radiuscheck_changelist')+'?expired=expired'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_not_expired(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        url = reverse('admin:sample_radius_radiuscheck_changelist')+'?expired=not_expired'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_nas_admin_save_model(self):
        User.objects.create_superuser(**_SUPERUSER)
        self.client.login(username=_SUPERUSER['username'], password=_SUPERUSER['password'])
        options = {
            'name': 'test-NAS', 'short_name': 'test', 'type': 'Virtual',
            'ports': '12', 'secret': 'testing123', 'server': '',
            'community': '', 'description': 'test'
        }
        nas = Nas.objects.create(**options)
        change_url = reverse('admin:sample_radius_nas_change', args=[nas.pk])
        data = options.copy()
        data['custom_type'] = ''
        data['type'] = 'Other'
        response = self.client.post(change_url, data, follow=True)
        self.assertNotContains(response, 'error')
        nas.refresh_from_db()
        self.assertEqual(nas.type, 'Other')
        data['custom_type'] = 'my-custom-type'
        response = self.client.post(change_url, data, follow=True)
        self.assertNotContains(response, 'error')
        nas.refresh_from_db()
        self.assertEqual(nas.type, 'my-custom-type')
