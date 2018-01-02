from django.core.management import call_command

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
