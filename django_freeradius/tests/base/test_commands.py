from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command
from django.utils.timezone import now

_RADACCT = {'username': 'bob', 'nas_ip_address': '127.0.0.1',
            'start_time': '2017-06-10 10:50:00', 'authentication': 'RADIUS',
            'connection_info_start': 'f', 'connection_info_stop': 'hgh',
            'input_octets': '1', 'output_octets': '4'}


class BaseTestCommands(object):
    def test_cleanup_stale_radacct_command(self):
        options = _RADACCT.copy()
        options['unique_id'] = '117'
        self.radius_accounting_model.objects.create(**options)
        call_command('cleanup_stale_radacct', 30)
        session = self.radius_accounting_model.objects.get(unique_id='117')
        self.assertNotEqual(session.stop_time, None)
        self.assertNotEqual(session.session_time, None)
        self.assertEqual(session.update_time, session.stop_time)

    def test_delete_old_postauth_command(self):
        self.radius_postauth_model.objects.create(username='steve', password='jones', reply='ghdhd')
        self.radius_postauth_model.objects.filter(username='steve').update(date='2017-06-10 10:50:00')
        call_command('delete_old_postauth', 3)
        self.assertEqual(self.radius_postauth_model.objects.filter(username='steve').count(), 0)

    def test_delete_old_radacct_command(self):
        options = _RADACCT.copy()
        options['stop_time'] = '2017-06-10 11:50:00'
        options['update_time'] = '2017-03-10 11:50:00'
        options['unique_id'] = '666'
        self.radius_accounting_model.objects.create(**options)
        call_command('delete_old_radacct', 3)
        self.assertEqual(self.radius_accounting_model.objects.filter(unique_id='666').count(), 0)

    def test_batch_add_users_command(self):
        self.assertEqual(self.radius_batch_model.objects.all().count(), 0)
        call_command('batch_add_users', file='django_freeradius/tests/static/test_batch.csv',
                     expiration='28-01-2018', name='test')
        self.assertEqual(self.radius_batch_model.objects.all().count(), 1)
        radiusbatch = self.radius_batch_model.objects.first()
        self.assertEqual(get_user_model().objects.all().count(), 3)
        self.assertEqual(radiusbatch.expiration_date.strftime('%d-%m-%y'), '28-01-18')
        call_command('batch_add_users', file='django_freeradius/tests/static/test_batch.csv', name='test1')
        self.assertEqual(self.radius_batch_model.objects.all().count(), 2)
        self.assertEqual(get_user_model().objects.all().count(), 6)
        with self.assertRaises(CommandError):
            call_command('batch_add_users', file='doesnotexist.csv', name='test2')
        with self.assertRaises(SystemExit):
            call_command('batch_add_users',
                         file='django_freeradius/tests/static/test_batch_invalid.csv',
                         name='test3')

    def test_deactivate_expired_users_command(self):
        call_command('batch_add_users', file='django_freeradius/tests/static/test_batch.csv',
                     expiration='28-01-1970', name='test')
        self.assertEqual(get_user_model().objects.filter(is_active=True).count(), 3)
        call_command('deactivate_expired_users')
        self.assertEqual(get_user_model().objects.filter(is_active=True).count(), 0)

    def test_delete_old_users_command(self):
        call_command('batch_add_users', file='django_freeradius/tests/static/test_batch.csv',
                     expiration='28-01-1970', name='test')
        expiration_date = now() - timedelta(days=30*15)
        call_command('batch_add_users', file='django_freeradius/tests/static/test_batch.csv',
                     expiration=expiration_date.strftime('%d-%m-%Y'), name='test1')
        self.assertEqual(get_user_model().objects.all().count(), 6)
        call_command('delete_old_users')
        self.assertEqual(get_user_model().objects.all().count(), 3)
        call_command('delete_old_users', older_than_months=12)
        self.assertEqual(get_user_model().objects.all().count(), 0)

    def test_prefix_add_users_commnad(self):
        self.assertEqual(self.radius_batch_model.objects.all().count(), 0)
        call_command('prefix_add_users', prefix='openwisp', n=10,
                     name='test', expiration='28-01-2018')
        self.assertEqual(self.radius_batch_model.objects.all().count(), 1)
        radiusbatch = self.radius_batch_model.objects.first()
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 10)
        for u in users:
            self.assertTrue('openwisp' in u.username)
        self.assertEqual(radiusbatch.expiration_date.strftime('%d-%m-%y'), '28-01-18')
        call_command('prefix_add_users', prefix='gsoc', n=5, name='test1')
        self.assertEqual(self.radius_batch_model.objects.all().count(), 2)
        self.assertEqual(get_user_model().objects.all().count(), 15)
        with self.assertRaises(SystemExit):
            call_command('prefix_add_users', prefix='openwisp', n=-5,
                         name='test2', expiration='28-01-2018')
