import os
from unittest import skipIf

from django.core.management import call_command
from django.test import TestCase

from ..models import RadiusAccounting, RadiusPostAuth

_RADACCT = {'username': 'bob', 'nas_ip_address': '127.0.0.1',
            'start_time': '2017-06-10 10:50:00', 'authentication': 'RADIUS',
            'connection_info_start': 'f', 'connection_info_stop': 'hgh',
            'input_octets': '1', 'output_octets': '4'}


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestCommands(TestCase):
    def test_cleanup_stale_radacct_command(self):
        options = _RADACCT.copy()
        options['unique_id'] = '117'
        RadiusAccounting.objects.create(**options)
        call_command('cleanup_stale_radacct', 30)
        session = RadiusAccounting.objects.get(unique_id='117')
        self.assertNotEqual(session.stop_time, None)
        self.assertNotEqual(session.session_time, None)
        self.assertEqual(session.update_time, session.stop_time)

    def test_delete_old_postauth_command(self):
        RadiusPostAuth.objects.create(username='steve', password='jones', reply='ghdhd')
        RadiusPostAuth.objects.filter(username='steve').update(date='2017-06-10 10:50:00')
        call_command('delete_old_postauth', 3)
        self.assertEqual(RadiusPostAuth.objects.filter(username='steve').count(), 0)

    def test_delete_old_radacct_command(self):
        options = _RADACCT.copy()
        options['stop_time'] = '2017-06-10 11:50:00'
        options['update_time'] = '2017-03-10 11:50:00'
        options['unique_id'] = '666'
        RadiusAccounting.objects.create(**options)
        call_command('delete_old_radacct', 3)
        self.assertEqual(RadiusAccounting.objects.filter(unique_id='666').count(), 0)
