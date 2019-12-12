from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from django_freeradius.migrations import (
    DEFAULT_SESSION_TIME_LIMIT, DEFAULT_SESSION_TRAFFIC_LIMIT, SESSION_TIME_ATTRIBUTE,
    SESSION_TRAFFIC_ATTRIBUTE,
)


class BaseTestNas(object):
    def test_string_representation(self):
        nas = self.nas_model(name='entry nasname')
        self.assertEqual(str(nas), nas.name)


class BaseTestRadiusAccounting(object):
    def test_string_representation(self):
        radiusaccounting = self.radius_accounting_model(unique_id='entry acctuniqueid')
        self.assertEqual(str(radiusaccounting), radiusaccounting.unique_id)

    def test_ipv6_validator(self):
        radiusaccounting = self.radius_accounting_model(unique_id='entry acctuniqueid',
                                                        session_id='entry acctuniqueid',
                                                        nas_ip_address='192.168.182.3',
                                                        framed_ipv6_prefix='::/64')
        radiusaccounting.full_clean()

        radiusaccounting.framed_ipv6_prefix = '192.168.0.0/28'
        self.assertRaises(ValidationError, radiusaccounting.full_clean)

        radiusaccounting.framed_ipv6_prefix = 'invalid ipv6_prefix'
        self.assertRaises(ValidationError, radiusaccounting.full_clean)


class BaseTestRadiusCheck(object):
    def test_string_representation(self):
        radiuscheck = self.radius_check_model(username='entry username')
        self.assertEqual(str(radiuscheck), radiuscheck.username)

    def test_auto_username(self):
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        c = self._create_radius_check(
            user=u,
            op=':=',
            attribute='Max-Daily-Session',
            value='3600'
        )
        self.assertEqual(c.username, u.username)

    def test_empty_username(self):
        opts = dict(op=':=',
                    attribute='Max-Daily-Session',
                    value='3600')
        try:
            self._create_radius_check(**opts)
        except ValidationError as e:
            self.assertIn('username', e.message_dict)
            self.assertIn('user', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_change_user_username(self):
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        c = self._create_radius_check(
            user=u,
            op=':=',
            attribute='Max-Daily-Session',
            value='3600'
        )
        u.username = 'changed'
        u.full_clean()
        u.save()
        c.refresh_from_db()
        # ensure related records have been updated
        self.assertEqual(c.username, u.username)

    def test_auto_value(self):
        obj = self._create_radius_check(username='Monica',
                                        value='Cam0_liX',
                                        attribute='NT-Password',
                                        op=':=')
        self.assertEqual(obj.value, '891fc570507eef023cbfec043dd5f2b1')

    def test_create_radius_check_model(self):
        obj = self.radius_check_model.objects.create(username='Monica',
                                                     new_value='Cam0_liX',
                                                     attribute='NT-Password',
                                                     op=':=')
        self.assertEqual(obj.value, '891fc570507eef023cbfec043dd5f2b1')


class BaseTestRadiusReply(object):
    def test_string_representation(self):
        radiusreply = self.radius_reply_model(username='entry username')
        self.assertEqual(str(radiusreply), radiusreply.username)

    def test_auto_username(self):
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        r = self._create_radius_reply(
            user=u,
            attribute='Reply-Message',
            op=':=',
            value='Login failed'
        )
        self.assertEqual(r.username, u.username)

    def test_empty_username(self):
        opts = dict(attribute='Reply-Message',
                    op=':=',
                    value='Login failed')
        try:
            self._create_radius_reply(**opts)
        except ValidationError as e:
            self.assertIn('username', e.message_dict)
            self.assertIn('user', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_change_user_username(self):
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        r = self._create_radius_reply(
            user=u,
            attribute='Reply-Message',
            op=':=',
            value='Login failed'
        )
        u.username = 'changed'
        u.full_clean()
        u.save()
        r.refresh_from_db()
        # ensure related records have been updated
        self.assertEqual(r.username, u.username)


class BaseTestRadiusPostAuth(object):
    def test_string_representation(self):
        radiuspostauthentication = self.radius_postauth_model(username='entry username')
        self.assertEqual(str(radiuspostauthentication), radiuspostauthentication.username)


class BaseTestRadiusGroup(object):
    def test_group_str(self):
        g = self.radius_group_model(name='entry groupname')
        self.assertEqual(str(g), g.name)

    def test_group_reply_str(self):
        r = self.radius_groupreply_model(groupname='entry groupname')
        self.assertEqual(str(r), r.groupname)

    def test_group_check_str(self):
        c = self.radius_groupcheck_model(groupname='entry groupname')
        self.assertEqual(str(c), c.groupname)

    def test_user_group_str(self):
        ug = self.radius_usergroup_model(username='entry username')
        self.assertEqual(str(ug), ug.username)

    def test_default_groups(self):
        queryset = self.radius_group_model.objects.all()
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(queryset.filter(name='users').count(), 1)
        self.assertEqual(queryset.filter(name='power-users').count(), 1)
        self.assertEqual(queryset.filter(default=True).count(), 1)
        users = queryset.get(name='users')
        self.assertTrue(users.default)
        self.assertEqual(users.radiusgroupcheck_set.count(), 2)
        check = users.radiusgroupcheck_set.get(attribute=SESSION_TIME_ATTRIBUTE)
        self.assertEqual(check.value, DEFAULT_SESSION_TIME_LIMIT)
        check = users.radiusgroupcheck_set.get(attribute=SESSION_TRAFFIC_ATTRIBUTE)
        self.assertEqual(check.value, DEFAULT_SESSION_TRAFFIC_LIMIT)
        power_users = queryset.get(name='power-users')
        self.assertEqual(power_users.radiusgroupcheck_set.count(), 0)

    def test_change_default_group(self):
        new_default = self.radius_group_model(name='new',
                                              description='test',
                                              default=True)
        new_default.full_clean()
        new_default.save()
        queryset = self.radius_group_model.objects.filter(default=True)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.filter(name='new').count(), 1)

    def test_delete_default_group(self):
        group = self.radius_group_model.objects.get(default=1)
        try:
            group.delete()
        except ProtectedError:
            pass
        else:
            self.fail('ProtectedError not raised')

    def test_undefault_group(self):
        group = self.radius_group_model.objects.get(default=True)
        group.default = False
        try:
            group.full_clean()
        except ValidationError as e:
            self.assertIn('default', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_no_default_failure_after_erasing(self):
        # this is a corner case but a very annoying one
        self.radius_group_model.objects.all().delete()  # won't trigger ValidationError
        self._create_radius_group(name='test')

    def test_new_user_default_group(self):
        u = get_user_model()(username='test',
                             email='test@test.org',
                             password='test')
        u.full_clean()
        u.save()
        usergroup_set = u.radiususergroup_set.all()
        self.assertEqual(usergroup_set.count(), 1)
        ug = usergroup_set.first()
        self.assertTrue(ug.group.default)

    def test_groupcheck_auto_name(self):
        g = self._create_radius_group(name='test',
                                      description='test')
        c = self._create_radius_groupcheck(
            group=g,
            attribute='Max-Daily-Session',
            op=':=',
            value='3600'
        )
        self.assertEqual(c.groupname, g.name)

    def test_groupcheck_empty_groupname(self):
        opts = dict(attribute='Max-Daily-Session',
                    op=':=',
                    value='3600')
        try:
            self._create_radius_groupcheck(**opts)
        except ValidationError as e:
            self.assertIn('groupname', e.message_dict)
            self.assertIn('group', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_groupreply_auto_name(self):
        g = self._create_radius_group(name='test',
                                      description='test')
        r = self._create_radius_groupreply(
            group=g,
            attribute='Reply-Message',
            op=':=',
            value='Login failed'
        )
        self.assertEqual(r.groupname, g.name)

    def test_groupreply_empty_groupname(self):
        opts = dict(attribute='Reply-Message',
                    op=':=',
                    value='Login failed')
        try:
            self._create_radius_groupreply(**opts)
        except ValidationError as e:
            self.assertIn('groupname', e.message_dict)
            self.assertIn('group', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_usergroups_auto_fields(self):
        g = self._create_radius_group(name='test',
                                      description='test')
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        ug = self._create_radius_usergroup(user=u,
                                           group=g,
                                           priority=1)
        self.assertEqual(ug.groupname, g.name)
        self.assertEqual(ug.username, u.username)

    def test_usergroups_empty_groupname(self):
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        try:
            self._create_radius_usergroup(user=u, priority=1)
        except ValidationError as e:
            self.assertIn('groupname', e.message_dict)
            self.assertIn('group', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_usergroups_empty_username(self):
        g = self._create_radius_group(name='test',
                                      description='test')
        try:
            self._create_radius_usergroup(group=g, priority=1)
        except ValidationError as e:
            self.assertIn('username', e.message_dict)
            self.assertIn('user', e.message_dict)
        else:
            self.fail('ValidationError not raised')

    def test_change_group_auto_name(self):
        g = self._create_radius_group(name='test',
                                      description='test')
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        c = self._create_radius_groupcheck(
            group=g,
            attribute='Max-Daily-Session',
            op=':=',
            value='3600'
        )
        r = self._create_radius_groupreply(
            group=g,
            attribute='Reply-Message',
            op=':=',
            value='Login failed'
        )
        ug = self._create_radius_usergroup(user=u,
                                           group=g,
                                           priority=1)
        g.name = 'changed'
        g.full_clean()
        g.save()
        c.refresh_from_db()
        r.refresh_from_db()
        ug.refresh_from_db()
        # ensure related records have been updated
        self.assertEqual(c.groupname, g.name)
        self.assertEqual(r.groupname, g.name)
        self.assertEqual(ug.groupname, g.name)

    def test_change_user_username(self):
        g = self._create_radius_group(name='test',
                                      description='test')
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        ug = self._create_radius_usergroup(user=u,
                                           group=g,
                                           priority=1)
        u.username = 'changed'
        u.full_clean()
        u.save()
        ug.refresh_from_db()
        # ensure related records have been updated
        self.assertEqual(ug.username, u.username)

    def test_delete(self):
        g = self._create_radius_group(name='test',
                                      description='test')
        g.delete()
        self.assertEqual(self.radius_group_model.objects.all().count(), 2)


class BaseTestRadiusBatch(object):
    def test_string_representation(self):
        radiusbatch = self.radius_batch_model(name='test')
        self.assertEqual(str(radiusbatch), 'test')

    def test_delete_method(self):
        radiusbatch = self._create_radius_batch(strategy='prefix',
                                                prefix='test',
                                                name='test')
        radiusbatch.prefix_add('test', 5)
        User = get_user_model()
        self.assertEqual(User.objects.all().count(), 5)
        radiusbatch.delete()
        self.assertEqual(self.radius_batch_model.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 0)

    def test_clean_method(self):
        with self.assertRaises(ValidationError):
            self._create_radius_batch()
        # missing csvfile
        try:
            self._create_radius_batch(strategy='csv',
                                      name='test')
        except ValidationError as e:
            self.assertIn('csvfile', e.message_dict)
        else:
            self.fail('ValidationError not raised')
        # missing prefix
        try:
            self._create_radius_batch(strategy='prefix',
                                      name='test')
        except ValidationError as e:
            self.assertIn('prefix', e.message_dict)
        else:
            self.fail('ValidationError not raised')
        # mixing strategies
        try:
            self._create_radius_batch(strategy='prefix',
                                      prefix='prefix',
                                      csvfile='test',
                                      name='test')
        except ValidationError as e:
            self.assertIn('Mixing', str(e))
        else:
            self.fail('ValidationError not raised')


class BaseTestRadiusToken(object):
    def test_string_representation(self):
        radiustoken = self.radius_token_model(key='test key')
        self.assertEqual(str(radiustoken), radiustoken.key)

    def test_create_radius_token_model(self):
        u = get_user_model().objects.create(username='test',
                                            email='test@test.org',
                                            password='test')
        obj = self.radius_token_model.objects.create(user=u)
        self.assertEqual(str(obj), obj.key)
        self.assertEqual(obj.user, u)
