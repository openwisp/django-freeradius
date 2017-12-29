import os
from copy import copy
from unittest import skipIf

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .. import settings
from ..models import (
    Nas, RadiusAccounting, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
    RadiusPostAuth, RadiusReply, RadiusUserGroup,
)

_RADCHECK_ENTRY = {'username': 'Monica', 'value': 'Cam0_liX',
                   'attribute': 'NT-Password'}
_RADCHECK_ENTRY_PW_UPDATE = {'username': 'Monica', 'new_value': 'Cam0_liX',
                             'attribute': 'NT-Password'}
_RADACCT = {'username': 'bob', 'nas_ip_address': '127.0.0.1',
            'start_time': '2017-06-10 10:50:00', 'authentication': 'RADIUS',
            'connection_info_start': 'f', 'connection_info_stop': 'hgh',
            'input_octets': '1', 'output_octets': '4'}


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestAdmin(TestCase):
    def setUp(self):
        self._superuser_login()

    def _superuser_login(self):
        user = User.objects.create_superuser(username='admin',
                                             password='admin',
                                             email='test@test.org')
        self.client.force_login(user)

    def test_nas_change(self):
        obj = Nas.objects.create(name='fiore', short_name='ff', type='cisco',
                                 secret='d', ports='22', community='vmv',
                                 description='ciao', server='jsjs')
        response = self.client.get(reverse('admin:django_freeradius_nas_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusreply_change(self):
        obj = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                         op=':=', value='passbob')
        response = self.client.get(reverse('admin:django_freeradius_radiusreply_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusgroupreply_change(self):
        obj = RadiusGroupReply.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP')
        response = self.client.get(reverse('admin:django_freeradius_radiusgroupreply_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusgroupcheck_change(self):
        obj = RadiusGroupCheck.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP')
        response = self.client.get(reverse('admin:django_freeradius_radiusgroupcheck_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusgroup_change(self):
        obj = RadiusGroup.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                         groupname='students', priority='1', notes='hh')
        response = self.client.get(reverse('admin:django_freeradius_radiusgroup_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiususergroup_change(self):
        obj = RadiusUserGroup.objects.create(username='bob', groupname='students', priority='1')
        response = self.client.get(reverse('admin:django_freeradius_radiususergroup_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusgroupusers_change(self):
        reply = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                           op=':=', value='passbob')
        check = RadiusCheck.objects.create(username='bob', attribute='Cleartext-Password',
                                           op=':=', value='passbob')
        obj = RadiusGroupUsers.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                              username='bob', groupname='students')
        obj.radius_reply.add(reply)
        obj.radius_check.add(check)
        response = self.client.get(reverse('admin:django_freeradius_radiusgroupusers_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusaccounting_change(self):
        obj = RadiusAccounting.objects.create(
            unique_id='2', username='bob', nas_ip_address='127.0.0.1', start_time='2017-06-10 10:50:00',
            stop_time='2017-06-10 11:50:00', session_time='5', authentication='RADIUS',
            connection_info_start='f', connection_info_stop='hgh',
            input_octets='1', output_octets='4', update_time='2017-03-10 11:50:00'
        )
        response = self.client.get(reverse('admin:django_freeradius_radiusaccounting_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusaccounting_changelist(self):
        original_value = settings.EDITABLE_ACCOUNTING
        settings.EDITABLE_ACCOUNTING = False
        response = self.client.get(reverse('admin:django_freeradius_radiusaccounting_changelist'))
        self.assertNotContains(response, 'Add accounting')
        settings.EDITABLE_ACCOUNTING = original_value

    def test_postauth_change(self):
        obj = RadiusPostAuth.objects.create(username='gino', password='ciao',
                                            reply='ghdhd', date='2017-09-02')
        response = self.client.get(reverse('admin:django_freeradius_radiuspostauth_change', args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiuscheck_change(self):
        obj = RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        _RADCHECK = copy(_RADCHECK_ENTRY_PW_UPDATE)
        _RADCHECK['attribute'] = 'Cleartext-Password'
        RadiusCheck.objects.create(**_RADCHECK)
        _RADCHECK['attribute'] = 'LM-Password'
        RadiusCheck.objects.create(**_RADCHECK)
        _RADCHECK['attribute'] = 'NT-Password'
        RadiusCheck.objects.create(**_RADCHECK)
        response = self.client.post(reverse('admin:django_freeradius_radiuscheck_change', args=[obj.pk]),
                                    _RADCHECK_ENTRY_PW_UPDATE, follow=True)
        self.assertContains(response, 'ok')

    def test_radiuscheck_create_weak_passwd(self):
        _RADCHECK = copy(_RADCHECK_ENTRY_PW_UPDATE)
        _RADCHECK['new_value'] = ''
        resp = self.client.post(reverse('admin:django_freeradius_radiuscheck_add'),
                                _RADCHECK, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_create_disabled_hash(self):
        _RADCHECK = copy(_RADCHECK_ENTRY_PW_UPDATE)
        _RADCHECK['attribute'] = 'Cleartext-Password'
        response = self.client.post(reverse('admin:django_freeradius_radiuscheck_add'),
                                    _RADCHECK, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_radiuscheck_admin_save_model(self):
        obj = RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        change_url = reverse('admin:django_freeradius_radiuscheck_change', args=[obj.pk])
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
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        checks = RadiusCheck.objects.all().values_list('pk', flat=True)
        change_url = reverse('admin:django_freeradius_radiuscheck_changelist')
        data = {'action': 'enable_action',
                '_selected_action': checks}
        self.client.post(change_url, data, follow=True)
        data = {'action': 'disable_action',
                '_selected_action': checks}
        self.client.post(change_url, data, follow=True)
        self.assertEqual(RadiusCheck.objects.filter(is_active=True).count(), 0)

    def test_radiuscheck_filter_duplicates_username(self):
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        url = reverse('admin:django_freeradius_radiuscheck_changelist')+'?duplicates=username'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_duplicates_value(self):
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        RadiusCheck.objects.create(**_RADCHECK_ENTRY)
        url = reverse('admin:django_freeradius_radiuscheck_changelist')+'?duplicates=value'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_expired(self):
        url = reverse('admin:django_freeradius_radiuscheck_changelist')+'?expired=expired'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_not_expired(self):
        url = reverse('admin:django_freeradius_radiuscheck_changelist')+'?expired=not_expired'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_delete_old_radacct_command(self):
        options = _RADACCT.copy()
        options['stop_time'] = '2017-06-10 11:50:00'
        options['update_time'] = '2017-03-10 11:50:00'
        options['unique_id'] = '666'
        RadiusAccounting.objects.create(**options)
        call_command('delete_old_radacct', 3)
        self.assertEqual(RadiusAccounting.objects.filter(unique_id='666').count(), 0)

    def test_delete_old_postauth_command(self):
        RadiusPostAuth.objects.create(username='steve', password='jones', reply='ghdhd')
        RadiusPostAuth.objects.filter(username='steve').update(date='2017-06-10 10:50:00')
        call_command('delete_old_postauth', 3)
        self.assertEqual(RadiusPostAuth.objects.filter(username='steve').count(), 0)

    def test_nas_admin_save_model(self):
        options = {
            'name': 'test-NAS', 'short_name': 'test', 'type': 'Virtual',
            'ports': '12', 'secret': 'testing123', 'server': '',
            'community': '', 'description': 'test'
        }
        nas = Nas.objects.create(**options)
        change_url = reverse('admin:django_freeradius_nas_change', args=[nas.pk])
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

    def test_cleanup_stale_radacct_command(self):
        options = _RADACCT.copy()
        options['unique_id'] = '117'
        RadiusAccounting.objects.create(**options)
        call_command('cleanup_stale_radacct', 30)
        session = RadiusAccounting.objects.get(unique_id='117')
        self.assertNotEqual(session.stop_time, None)
        self.assertNotEqual(session.session_time, None)
        self.assertEqual(session.update_time, session.stop_time)
