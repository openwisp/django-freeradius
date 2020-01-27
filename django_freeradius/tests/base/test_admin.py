from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse

from django_freeradius import settings

User = get_user_model()


class BaseTestAdmin(object):
    _RADCHECK_ENTRY = {'username': 'Monica', 'value': 'Cam0_liX',
                       'attribute': 'NT-Password', 'op': ':='}
    _RADCHECK_ENTRY_PW_UPDATE = {'username': 'Monica', 'new_value': 'Cam0_liX',
                                 'attribute': 'NT-Password', 'op': ':='}

    def setUp(self):
        self._superuser_login()

    def _superuser_login(self):
        user = User.objects.create_superuser(username='admin',
                                             password='admin',
                                             email='test@test.org')
        self.client.force_login(user)

    def test_nas_change(self):
        options = dict(name='fiore', short_name='ff', type='cisco',
                       secret='d', ports='22', community='vmv',
                       description='ciao', server='jsjs')
        obj = self._create_nas(**options)
        response = self.client.get(reverse('admin:{0}_nas_change'.format(self.app_name), args=[obj.pk]))
        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiusreply_change(self):
        options = dict(username='bob', attribute='Cleartext-Password',
                       op=':=', value='passbob')
        obj = self._create_radius_reply(**options)
        response = self.client.get(reverse('admin:{0}_radiusreply_change'.format(self.app_name),
                                           args=[obj.pk]))

        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiusgroupreply_change(self):
        options = dict(groupname='students', attribute='Cleartext-Password',
                       op=':=', value='PPP')
        obj = self._create_radius_groupreply(**options)
        response = self.client.get(reverse('admin:{0}_radiusgroupreply_change'.format(self.app_name),
                                           args=[obj.pk]))

        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiusgroupcheck_change(self):
        options = dict(groupname='students', attribute='Cleartext-Password',
                       op=':=', value='PPP')
        obj = self._create_radius_groupcheck(**options)
        response = self.client.get(reverse(
                                   'admin:{0}_radiusgroupcheck_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiususergroup_change(self):
        options = dict(username='bob', groupname='students', priority='1')
        obj = self._create_radius_usergroup(**options)
        response = self.client.get(reverse(
                                   'admin:{0}_radiususergroup_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiusaccounting_change(self):
        options = dict(unique_id='2', username='bob', nas_ip_address='127.0.0.1',
                       start_time='2017-06-10 10:50:00', stop_time='2017-06-10 11:50:00',
                       session_time='5', authentication='RADIUS',
                       connection_info_start='f', connection_info_stop='hgh',
                       input_octets='1', output_octets='4', update_time='2017-03-10 11:50:00',
                       session_id='1')
        obj = self._create_radius_accounting(**options)
        response = self.client.get(reverse(
                                   'admin:{0}_radiusaccounting_change'.format(self.app_name),
                                   args=[obj.pk]))
        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiusaccounting_changelist(self):
        original_value = settings.EDITABLE_ACCOUNTING
        settings.EDITABLE_ACCOUNTING = False
        url = reverse('admin:{0}_radiusaccounting_changelist'.format(self.app_name))
        response = self.client.get(url)
        self.assertNotContains(response, 'Add accounting')
        settings.EDITABLE_ACCOUNTING = original_value

    def test_postauth_change(self):
        options = dict(username='gino', password='ciao', reply='ghdhd', date='2017-09-02')
        obj = self._create_radius_postauth(**options)
        url = reverse('admin:{0}_radiuspostauth_change'.format(self.app_name), args=[obj.pk])
        response = self.client.get(url)
        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiuscheck_change(self):
        obj = self._create_radius_check(**self._RADCHECK_ENTRY)
        _RADCHECK = self._RADCHECK_ENTRY.copy()
        _RADCHECK['attribute'] = 'Cleartext-Password'
        self._create_radius_check(**_RADCHECK)
        _RADCHECK['attribute'] = 'LM-Password'
        self._create_radius_check(**_RADCHECK)
        _RADCHECK['attribute'] = 'NT-Password'
        self._create_radius_check(**_RADCHECK)
        _RADCHECK['attribute'] = 'MD5-Password'
        self._create_radius_check(**_RADCHECK)
        _RADCHECK['attribute'] = 'SMD5-Password'
        self._create_radius_check(**_RADCHECK)
        _RADCHECK['attribute'] = 'SHA-Password'
        self._create_radius_check(**_RADCHECK)
        _RADCHECK['attribute'] = 'SSHA-Password'
        self._create_radius_check(**_RADCHECK)
        _RADCHECK['attribute'] = 'Crypt-Password'
        self._create_radius_check(**_RADCHECK)
        data = self._RADCHECK_ENTRY_PW_UPDATE.copy()
        data['mode'] = 'custom'
        url = reverse('admin:{0}_radiuscheck_change'.format(self.app_name), args=[obj.pk])
        response = self.client.post(url, data, follow=True)
        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiusbatch_change(self):
        obj = self._create_radius_batch(name='test',
                                        strategy='prefix',
                                        prefix='test',
                                        expiration_date='1998-01-28')
        url = reverse('admin:{0}_radiusbatch_change'.format(self.app_name), args=[obj.pk])
        response = self.client.get(url)
        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radiuscheck_create_weak_passwd(self):
        _RADCHECK = self._RADCHECK_ENTRY_PW_UPDATE.copy()
        _RADCHECK['new_value'] = ''
        resp = self.client.post(reverse('admin:{0}_radiuscheck_add'.format(self.app_name)),
                                _RADCHECK, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'errors')

    def test_radiuscheck_create_disabled_hash(self):
        data = self._RADCHECK_ENTRY_PW_UPDATE.copy()
        data['attribute'] = 'Cleartext-Password'
        data['mode'] = 'custom'
        url = reverse('admin:{0}_radiuscheck_add'.format(self.app_name))
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'errors')

    def test_radiuscheck_admin_save_model(self):
        obj = self._create_radius_check(**self._RADCHECK_ENTRY)
        change_url = reverse('admin:{0}_radiuscheck_change'.format(self.app_name), args=[obj.pk])
        # test admin save_model method
        data = self._RADCHECK_ENTRY_PW_UPDATE.copy()
        data['op'] = ':='
        data['mode'] = 'custom'
        response = self.client.post(change_url, data, follow=True)
        self.assertNotContains(response, 'errors')
        obj.refresh_from_db()
        self.assertNotEqual(obj.value, self._RADCHECK_ENTRY['value'])
        self.assertNotEqual(obj.value, data['new_value'])  # hashed
        # test also invalid password
        data['new_value'] = 'cionfrazZ'
        response = self.client.post(change_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errors')
        self.assertContains(response, 'The secret must contain')

    def test_radiuscheck_enable_disable_action(self):
        self._create_radius_check(**self._RADCHECK_ENTRY)
        checks = self.radius_check_model.objects.all().values_list('pk', flat=True)
        change_url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name))
        data = {'action': 'enable_action', '_selected_action': checks}
        self.client.post(change_url, data, follow=True)
        data = {'action': 'disable_action', '_selected_action': checks}
        self.client.post(change_url, data, follow=True)
        self.assertEqual(self.radius_check_model.objects.filter(is_active=True).count(), 0)

    def test_radiuscheck_filter_duplicates_username(self):
        self._create_radius_check(**self._RADCHECK_ENTRY)
        self._create_radius_check(**self._RADCHECK_ENTRY)
        url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name)) + '?duplicates=username'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_duplicates_value(self):
        self._create_radius_check(**self._RADCHECK_ENTRY)
        self._create_radius_check(**self._RADCHECK_ENTRY)
        url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name)) + '?duplicates=value'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_expired(self):
        url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name)) + '?expired=expired'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_radiuscheck_filter_not_expired(self):
        url = reverse('admin:{0}_radiuscheck_changelist'.format(self.app_name)) + '?expired=not_expired'
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_nas_admin_save_model(self):
        options = {
            'name': 'test-NAS', 'short_name': 'test', 'type': 'Virtual',
            'ports': '12', 'secret': 'testing123', 'server': '',
            'community': '', 'description': 'test'
        }
        nas = self._create_nas(**options)
        change_url = reverse('admin:{0}_nas_change'.format(self.app_name), args=[nas.pk])
        options['custom_type'] = ''
        options['type'] = 'Other'
        options = self._get_post_defaults(options)
        response = self.client.post(change_url, options, follow=True)
        self.assertNotContains(response, 'error')
        nas.refresh_from_db()
        self.assertEqual(nas.type, 'Other')

    def test_radius_batch_save_model(self):
        self.assertEqual(self.radius_batch_model.objects.count(), 0)
        add_url = reverse('admin:{0}_radiusbatch_add'.format(self.app_name))
        data = self._get_csv_post_data()
        response = self.client.post(add_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.radius_batch_model.objects.count(), 1)
        batch = self.radius_batch_model.objects.first()
        self.assertEqual(batch.users.count(), 3)
        change_url = reverse('admin:{0}_radiusbatch_change'.format(self.app_name), args=[batch.pk])
        response = self.client.post(change_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(batch.users.count(), 3)
        data = self._get_prefix_post_data()
        response = self.client.post(add_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.radius_batch_model.objects.count(), 2)
        data["number_of_users"] = -5
        response = self.client.post(add_url, data, follow=True)
        error_message = "Ensure this value is greater than or equal to 1"
        self.assertTrue(error_message in str(response.content))

    def test_radiusbatch_no_of_users(self):
        r = self._create_radius_batch(name='test',
                                      strategy='prefix',
                                      prefix='openwisp')
        path = reverse('admin:{0}_radiusbatch_change'.format(self.app_name), args=[r.pk])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'field-number_of_users')

    def test_radiusbatch_delete_methods(self):
        n = User.objects.count()
        options = dict(n=10, prefix='test', name='test')
        self._call_command('prefix_add_users', **options)
        self.assertEqual(User.objects.count() - n, 10)
        r = self.radius_batch_model.objects.first()
        delete_path = reverse('admin:{0}_radiusbatch_delete'.format(self.app_name), args=[r.pk])
        response = self.client.post(delete_path, {'post': 'yes'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count() - n, 0)
        options['name'] = 'test1'
        self._call_command('prefix_add_users', **options)
        options['name'] = 'test2'
        self._call_command('prefix_add_users', **options)
        self.assertEqual(User.objects.count() - n, 20)
        changelist_path = reverse('admin:{0}_radiusbatch_changelist'.format(self.app_name))
        p_keys = [x.pk for x in self.radius_batch_model.objects.all()]
        data = {
            'action': 'delete_selected_batches',
            '_selected_action': p_keys
        }
        response = self.client.post(changelist_path, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count() - n, 0)

    def test_radius_batch_csv_help_text(self):
        add_url = reverse('admin:{0}_radiusbatch_add'.format(self.app_name))
        response = self.client.get(add_url)
        docs_link = "https://django-freeradius.readthedocs.io/en/latest/general/importing_users.html"
        self.assertContains(response, docs_link)

    def test_radiususergroup_inline_user(self):
        app_label = User._meta.app_label
        add_url = reverse('admin:{}_user_add'.format(app_label))
        response = self.client.get(add_url)
        label_id = 'radiususergroup_set-group'
        self.assertNotContains(response, label_id)
        user = User.objects.first()
        change_url = reverse('admin:{}_user_change'.format(app_label), args=[user.pk])
        response = self.client.get(change_url)
        self.assertContains(response, label_id)

    def _get_csv_post_data(self):
        path = self._get_path('static/test_batch.csv')
        csvfile = open(path, 'rt')
        data = {'expiration_date': '2019-03-20', 'strategy': 'csv', 'csvfile': csvfile, 'name': 'test1'}
        return data

    def _get_prefix_post_data(self):
        data = {'expiration_date': '2019-03-20', 'strategy': 'prefix',
                'prefix': 'openwisp', 'number_of_users': 10, 'name': 'test2'}
        return data

    def test_radius_group_delete_default_by_superuser(self):
        rg = self.radius_group_model.objects
        default = rg.get(default=True)
        url_name = 'admin:{0}_radiusgroup_delete'.format(self.app_name)
        delete_url = reverse(url_name, args=[default.pk])
        response = self.client.get(delete_url)
        self.assertEqual(rg.filter(default=True).count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_radius_group_delete_default_by_non_superuser(self):
        user = User.objects.get(username='admin')
        user.is_superuser = False
        user.save()
        for permission in Permission.objects.all():
            user.user_permissions.add(permission)
        rg = self.radius_group_model.objects
        default = rg.get(default=True)
        url_name = 'admin:{0}_radiusgroup_delete'.format(self.app_name)
        delete_url = reverse(url_name, args=[default.pk])
        response = self.client.get(delete_url)
        self.assertEqual(rg.filter(default=True).count(), 1)
        self.assertEqual(response.status_code, 403)

    def test_radius_group_delete_selected_default(self):
        url = reverse('admin:{0}_radiusgroup_changelist'.format(self.app_name))
        rg = self.radius_group_model.objects
        default = rg.get(default=True)
        response = self.client.post(url, {
            'action': 'delete_selected_groups',
            '_selected_action': str(default.pk),
            'select_across': '0',
            'index': '0',
            'post': 'yes'
        }, follow=True)
        self.assertEqual(rg.filter(default=True).count(), 1)
        self.assertContains(response, 'error')
        self.assertContains(response, 'Cannot proceed with the delete')

    def test_radius_group_delete_selected_non_default(self):
        url = reverse('admin:{0}_radiusgroup_changelist'.format(self.app_name))
        rg = self.radius_group_model.objects
        non_default = rg.get(default=False)
        response = self.client.post(url, {
            'action': 'delete_selected_groups',
            '_selected_action': str(non_default.pk),
            'select_across': '0',
            'index': '0',
            'post': 'yes'
        }, follow=True)
        self.assertNotContains(response, 'error')
        self.assertEqual(rg.filter(default=False).count(), 0)

    def test_batch_user_creation_form(self):
        url = reverse('admin:{0}_radiusbatch_add'.format(self.app_name))
        response = self.client.post(url, {
            'strategy': 'prefix',
            'prefix': 'test',
            'name': 'test_name',
            'csvfile': '',
            'number_of_users': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errors field-number_of_users')

    def test_radius_token_creation_form(self):
        n = self.radius_token_model.objects.count()
        url = reverse('admin:{0}_radiustoken_add'.format(self.app_name))
        user = User.objects.create_user(username='test_user', password='test_password')
        self.client.post(url, {'user': user.id})
        self.assertEqual(self.radius_token_model.objects.count() - n, 1)

    def test_radius_token_change(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        token = self.radius_token_model.objects.create(user=user)
        response = self.client.get(reverse(
            'admin:{0}_radiustoken_change'.format(self.app_name),
            args=[token.key]))
        self.assertContains(response, 'ok')
        self.assertNotContains(response, 'errors')

    def test_radius_token_delete_selected(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        token = self.radius_token_model.objects.create(user=user)
        n = self.radius_token_model.objects.count()
        url = reverse('admin:{0}_radiustoken_changelist'.format(self.app_name))
        self.client.post(url, {
            'action': 'delete_selected',
            '_selected_action': str(token.key),
            'select_across': '0',
            'index': '0',
            'post': 'yes'
        }, follow=True)
        self.assertEqual(n - self.radius_token_model.objects.count(), 1)
