from django.contrib.auth.models import User
from django.urls import reverse

from django_freeradius import settings

_RADCHECK_ENTRY = {'username': 'Monica', 'value': 'Cam0_liX',
                   'attribute': 'NT-Password'}
_RADCHECK_ENTRY_PW_UPDATE = {'username': 'Monica', 'new_value': 'Cam0_liX',
                             'attribute': 'NT-Password'}


class BaseTestAdmin(object):
    def setUp(self):
        self._superuser_login()

    def _superuser_login(self):
        user = User.objects.create_superuser(username='admin',
                                             password='admin',
                                             email='test@test.org')
        self.client.force_login(user)

    def test_nas_change(self):
        obj = self.nas_model.objects.create(name='fiore', short_name='ff', type='cisco',
                                            secret='d', ports='22', community='vmv',
                                            description='ciao', server='jsjs')
        response = self.client.get(reverse('admin:{0}_nas_change'.format(self.app_name), args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusreply_change(self):
        obj = self.radius_reply_model.objects.create(username='bob', attribute='Cleartext-Password',
                                                     op=':=', value='passbob')
        response = self.client.get(reverse(
                                   'admin:{0}_radiusreply_change'.format(self.app_name),
                                   args=[obj.pk]))

        self.assertContains(response, 'ok')

    def test_radiusgroupreply_change(self):
        obj = self.radius_groupreply_model.objects.create(groupname='students',
                                                          attribute='Cleartext-Password',
                                                          op=':=', value='PPP')
        response = self.client.get(reverse(
                                   'admin:{0}_radiusgroupreply_change'.format(self.app_name),
                                   args=[obj.pk]))

        self.assertContains(response, 'ok')

    def test_radiusgroupcheck_change(self):
        obj = self.radius_groupcheck_model.objects.create(groupname='students',
                                                          attribute='Cleartext-Password',
                                                          op=':=', value='PPP')
        response = self.client.get(reverse(
                                   'admin:{0}_radiusgroupcheck_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusgroup_change(self):
        obj = self.radius_group_model.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                                     groupname='students', priority='1', notes='hh')
        response = self.client.get(reverse(
                                   'admin:{0}_radiusgroup_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiususergroup_change(self):
        obj = self.radius_usergroup_model.objects.create(username='bob', groupname='students', priority='1')
        response = self.client.get(reverse(
                                   'admin:{0}_radiususergroup_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusgroupusers_change(self):
        reply = self.radius_reply_model.objects.create(username='bob', attribute='Cleartext-Password',
                                                       op=':=', value='passbob')
        check = self.radius_check_model.objects.create(username='bob', attribute='Cleartext-Password',
                                                       op=':=', value='passbob')
        obj = self.radius_groupusers_model.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                                          username='bob', groupname='students')
        obj.radius_reply.add(reply)
        obj.radius_check.add(check)
        response = self.client.get(reverse(
                                   'admin:{0}_radiusgroupusers_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusaccounting_change(self):
        obj = self.radius_accounting_model.objects.create(
            unique_id='2', username='bob', nas_ip_address='127.0.0.1', start_time='2017-06-10 10:50:00',
            stop_time='2017-06-10 11:50:00', session_time='5', authentication='RADIUS',
            connection_info_start='f', connection_info_stop='hgh',
            input_octets='1', output_octets='4', update_time='2017-03-10 11:50:00'
        )
        response = self.client.get(reverse(
                                   'admin:{0}_radiusaccounting_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiusaccounting_changelist(self):
        original_value = settings.EDITABLE_ACCOUNTING
        settings.EDITABLE_ACCOUNTING = False
        response = self.client.get(reverse(
                                   'admin:{0}_radiusaccounting_changelist'.format(self.app_name)))
        self.assertNotContains(response, 'Add accounting')
        settings.EDITABLE_ACCOUNTING = original_value

    def test_postauth_change(self):
        obj = self.radius_postauth_model.objects.create(username='gino', password='ciao',
                                                        reply='ghdhd', date='2017-09-02')
        response = self.client.get(reverse(
                                   'admin:{0}_radiuspostauth_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')

    def test_radiuscheck_change(self):
        obj = self.radius_check_model.objects.create(**_RADCHECK_ENTRY)
        _RADCHECK = _RADCHECK_ENTRY_PW_UPDATE.copy()
        _RADCHECK['attribute'] = 'Cleartext-Password'
        self.radius_check_model.objects.create(**_RADCHECK)
        _RADCHECK['attribute'] = 'LM-Password'
        self.radius_check_model.objects.create(**_RADCHECK)
        _RADCHECK['attribute'] = 'NT-Password'
        self.radius_check_model.objects.create(**_RADCHECK)
        response = self.client.post(reverse(
                                    'admin:{0}_radiuscheck_change'.format(self.app_name),
                                    args=[obj.pk]),
                                    _RADCHECK_ENTRY_PW_UPDATE, follow=True)
        self.assertContains(response, 'ok')

    def test_radiuscheck_create_weak_passwd(self):
        _RADCHECK = _RADCHECK_ENTRY_PW_UPDATE.copy()
        _RADCHECK['new_value'] = ''
        resp = self.client.post(reverse('admin:{0}_radiuscheck_add'.format(self.app_name)),
                                _RADCHECK, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_create_disabled_hash(self):
        _RADCHECK = _RADCHECK_ENTRY_PW_UPDATE.copy()
        _RADCHECK['attribute'] = 'Cleartext-Password'
        response = self.client.post(reverse('admin:{0}_radiuscheck_add'.format(self.app_name)),
                                    _RADCHECK, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_radiuscheck_admin_save_model(self):
        obj = self.radius_check_model.objects.create(**_RADCHECK_ENTRY)
        change_url = reverse('admin:{0}_radiuscheck_change'.format(self.app_name), args=[obj.pk])
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
        self.radius_check_model.objects.create(**_RADCHECK_ENTRY)
        checks = self.radius_check_model.objects.all().values_list('pk', flat=True)
        change_url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name))
        data = {'action': 'enable_action',
                '_selected_action': checks}
        self.client.post(change_url, data, follow=True)
        data = {'action': 'disable_action',
                '_selected_action': checks}
        self.client.post(change_url, data, follow=True)
        self.assertEqual(self.radius_check_model.objects.filter(is_active=True).count(), 0)

    def test_radiuscheck_filter_duplicates_username(self):
        self.radius_check_model.objects.create(**_RADCHECK_ENTRY)
        self.radius_check_model.objects.create(**_RADCHECK_ENTRY)
        url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name))+'?duplicates=username'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_duplicates_value(self):
        self.radius_check_model.objects.create(**_RADCHECK_ENTRY)
        self.radius_check_model.objects.create(**_RADCHECK_ENTRY)
        url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name))+'?duplicates=value'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_expired(self):
        url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name))+'?expired=expired'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_not_expired(self):
        url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name))+'?expired=not_expired'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_nas_admin_save_model(self):
        options = {
            'name': 'test-NAS', 'short_name': 'test', 'type': 'Virtual',
            'ports': '12', 'secret': 'testing123', 'server': '',
            'community': '', 'description': 'test'
        }
        nas = self.nas_model.objects.create(**options)
        change_url = reverse('admin:{0}_nas_change'.format(self.app_name), args=[nas.pk])
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
