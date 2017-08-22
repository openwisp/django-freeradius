import swapper
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now
from freezegun import freeze_time

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")


class TestApi(TestCase):
    def test_authorize_200(self):
        User.objects.create_user(username='molly', password='barbar')
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'molly', 'password': 'barbar'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'control:Auth-Type': 'Accept'})

    def test_authorize_401(self):
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'baldo', 'password': 'ugo'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'control:Auth-Type': 'Reject'})

    def test_postauth_accept_201(self):
        self.assertEqual(RadiusPostAuth.objects.all().count(), 0)
        params = {'username': 'molly', 'password': 'barbar', 'reply': 'Access-Accept',
                  'called_station_id': '00-11-22-33-44-55:hostname',
                  'calling_station_id': '00:26:b9:20:5f:10'}
        response = self.client.post(reverse('freeradius:postauth'), params)
        params['password'] = ''
        self.assertEqual(RadiusPostAuth.objects.filter(**params).count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_reject_201(self):
        self.assertEqual(RadiusPostAuth.objects.all().count(), 0)
        params = {'username': 'molly', 'password': 'barba', 'reply': 'Access-Reject'}
        response = self.client.post(reverse('freeradius:postauth'), params)
        self.assertEqual(RadiusPostAuth.objects.filter(username='molly', password='barba').count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_reject_201_empty_fields(self):
        params = {'username': 'molly', 'password': 'barba', 'reply': 'Access-Reject',
                  'called_station_id': '',
                  'calling_station_id': ''}
        response = self.client.post(reverse('freeradius:postauth'), params)
        self.assertEqual(RadiusPostAuth.objects.filter(**params).count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_400(self):
        response = self.client.post(reverse('freeradius:postauth'), {})
        self.assertEqual(RadiusPostAuth.objects.all().count(), 0)
        self.assertEqual(response.status_code, 400)

    def test_accounting_start_200(self):
        self.assertEqual(RadiusAccounting.objects.count(), 0)
        ra = RadiusAccounting.objects.create(
            session_id='35000006', unique_id='75058e50',
            username='admin', start_time='2017-08-08 15:16:10+0200',
            nas_ip_address='172.16.64.91', nas_port_id='1',
            nas_port_type='Async',
            session_time='262',
            authentication='authentication', realm='',
            input_octets='9900909',
            output_octets='1513075509', calling_station_id='5c:7d:c1:72:a7:3b',
            called_station_id='00-27-22-F3-FA-F1:hostname',
            terminate_cause='terminate_cause',
            service_type='service_type', framed_protocol='',
            framed_ip_address='', groupname=''
        )
        data = {'username': 'admin', 'nas_ip_address': '172.16.64.91',
                'nas_port': '1', 'called_station_id': '00_27_22_F3_Fa_F1',
                'calling_station_id': '5c:7d:c1:72:a7:3b', 'nas_identifier': '',
                'status_type': 'Start', 'authentication': 'RADIUS',
                'acct_delay_time': '0',
                'unique_id': '75058e50',
                'terminate_cause': 'User_Request', 'input_octets': '1111909',
                'output_octets': '1511074444', 'nas_port_type': 'async',
                'session_time': '261', 'login_service': 'Telnet',
                'login_ip_host': '172.16.64.25', 'session_id': '35000006',
                'framed_protocol': '', 'framed_ip_address': '',
                'service_type': 'Login-User', 'Realm': ''}
        response = self.client.post(reverse('freeradius:accounting'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RadiusAccounting.objects.count(), 1)

    def test_accounting_start_201(self):
        self.assertEqual(RadiusAccounting.objects.count(), 0)
        data = {'username': 'admin', 'nas_ip_address': '172.16.64.91',
                'nas_port': '1', 'called_station_id': '00_27_22_F3_Fa_F1',
                'calling_station_id': '5c:7d:c1:72:a7:3b', 'nas_identifier': '',
                'status_type': 'Start', 'authentication': 'RADIUS',
                'acct_delay_time': '0',
                'unique_id': '75058e50',
                'terminate_cause': 'User_Request', 'input_octets': '1111909',
                'output_octets': '1511074444', 'nas_port_type': 'async',
                'session_time': '261', 'login_service': 'Telnet',
                'login_ip_host': '172.16.64.25', 'session_id': '35000006',
                'framed_protocol': '', 'framed_ip_address': '',
                'service_type': 'Login-User', 'Realm': ''}
        response = self.client.post(reverse('freeradius:accounting'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RadiusAccounting.objects.count(), 1)

    @freeze_time("2017-08-08 15:16:10+0200")
    def test_accounting_update_200(self):
        self.assertEqual(RadiusAccounting.objects.count(), 0)
        ra = RadiusAccounting.objects.create(
            session_id='35000006', unique_id='75058e50',
            username='admin', start_time='2017-08-08 15:16:10+0200',
            nas_ip_address='172.16.64.91', nas_port_id='1',
            nas_port_type='Async',
            session_time='262',
            authentication='authentication', realm='',
            input_octets='9900909',
            output_octets='1513075509', calling_station_id='5c:7d:c1:72:a7:3b',
            called_station_id='00-27-22-F3-FA-F1:hostname',
            terminate_cause='terminate_cause',
            service_type='service_type', framed_protocol='',
            framed_ip_address='', groupname=''
        )
        data = {'username': 'admin', 'nas_ip_address': '172.16.64.91',
                'nas_port': '1', 'called_station_id': '00_27_22_F3_Fa_F1',
                'calling_station_id': '5c:7d:c1:72:a7:3b', 'nas_identifier': '',
                'status_type': 'Interim-Update', 'authentication': 'RADIUS',
                'acct_delay_time': '0',
                'unique_id': '75058e50',
                'terminate_cause': 'User_Request', 'input_octets': '1111909',
                'output_octets': '1511074444', 'nas_port_type': 'async',
                'acct_session_time': '261', 'login_service': 'Telnet',
                'login_ip_host': '172.16.64.25', 'session_id': '35000006',
                'framed_protocol': '', 'framed_ip_address': '',
                'service_type': 'Login-User', 'Realm': ''}

        # sending an accounting packet
        response = self.client.post(reverse('freeradius:accounting'), data=data)
        self.assertEqual(response.status_code, 200)
        ra.refresh_from_db()
        self.assertEqual(RadiusAccounting.objects.count(), 1)
        self.assertEqual(ra.output_octets, 1511074444)
        self.assertEqual(ra.input_octets, 1111909)
        self.assertEqual(ra.update_time.timetuple(), now().timetuple())

    @freeze_time("2017-08-08 15:16:10+0200")
    def test_accounting_stop_200(self):
        self.assertEqual(RadiusAccounting.objects.count(), 0)
        ra = RadiusAccounting.objects.create(
            session_id='35000006', unique_id='75058e50',
            username='admin', start_time='2017-08-08 15:16:10+0200',
            nas_ip_address='172.16.64.91', nas_port_id='1',
            nas_port_type='Async',
            session_time='261',
            authentication='authentication', realm='',
            input_octets='9900909',
            output_octets='1511075509', calling_station_id='5c:7d:c1:72:a7:3b',
            called_station_id='00-27-22-F3-FA-F1:hostname',
            terminate_cause='terminate_cause',
            service_type='service_type', framed_protocol='',
            framed_ip_address='', groupname=''
        )
        # reload date object in order to store ra.start_time
        ra.refresh_from_db()
        start_time = ra.start_time
        data = {'username': 'admin', 'nas_ip_address': '172.16.64.91',
                'nas_port': '1', 'called_station_id': '00_27_22_F3_Fa_F1',
                'calling_station_id': '5c:7d:c1:72:a7:3b', 'nas_identifier': '',
                'status_type': 'Stop', 'authentication': 'RADIUS',
                'acct_delay_time': '0',
                'unique_id': '75058e50',
                'terminate_cause': 'User_Request', 'input_octets': '9900909',
                'output_octets': '1511075509', 'nas_port_type': 'async',
                'session_time': '261', 'login_service': 'Telnet',
                'login_ip_host': '172.16.64.25', 'session_id': '35000006',
                'framed_protocol': '', 'framed_ip_address': '',
                'service_type': 'Login-User', 'Realm': ''}
        response = self.client.post(reverse('freeradius:accounting'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RadiusAccounting.objects.count(), 1)
        ra.refresh_from_db()
        self.assertEqual(ra.update_time.timetuple(), now().timetuple())
        self.assertEqual(ra.stop_time.timetuple(), now().timetuple())
        self.assertEqual(ra.start_time, start_time)

    def test_accounting_list_200(self):
        RadiusAccounting.objects.create(
            session_id='35000006', unique_id='75058e50',
            username='admin', start_time='2017-08-08 15:16:10+0200',
            nas_ip_address='172.16.64.91', nas_port_id='1',
            nas_port_type='Async',
            session_time='262',
            authentication='authentication', realm='',
            input_octets='9900909',
            output_octets='1513075509', calling_station_id='5c:7d:c1:72:a7:3b',
            called_station_id='00-27-22-F3-FA-F1:hostname',
            terminate_cause='terminate_cause',
            service_type='service_type', framed_protocol='',
            framed_ip_address='', groupname=''
        )
        RadiusAccounting.objects.create(
            session_id='40111116', unique_id='12234f69',
            username='molly', start_time='2017-08-08 15:16:10+0200',
            nas_ip_address='172.16.64.91', nas_port_id='1',
            nas_port_type='Async',
            session_time='262',
            authentication='authentication', realm='',
            input_octets='3000909',
            output_octets='1613176609', calling_station_id='5c:7d:c1:72:a7:3b',
            called_station_id='00-27-22-F3-FA-F1:hostname',
            terminate_cause='terminate_cause',
            service_type='service_type', framed_protocol='',
            framed_ip_address='', groupname=''
        )
        RadiusAccounting.objects.create(
            session_id='89897654', unique_id='99144d60',
            username='lillo', start_time='2017-08-17 18:16:10+0200',
            nas_ip_address='172.16.64.91', nas_port_id='1',
            nas_port_type='Async',
            session_time='262',
            authentication='authentication', realm='',
            input_octets='4440909',
            output_octets='1119074409', calling_station_id='5c:7d:c1:72:a7:3b',
            called_station_id='00-27-22-F3-FA-F1:hostname',
            terminate_cause='User_Request',
            service_type='Login-User', framed_protocol='',
            framed_ip_address='', groupname=''
        )
        response = self.client.get(reverse('freeradius:accounting'))
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['username'], 'admin')
        self.assertEqual(item['calling_station_id'], '5c:7d:c1:72:a7:3b')
        self.assertEqual(item['output_octets'], 1513075509)
        self.assertEqual(item['input_octets'], 9900909)
        item = response.data[1]
        self.assertEqual(item['output_octets'], 1613176609)
        self.assertEqual(item['nas_ip_address'], '172.16.64.91')
        self.assertEqual(item['input_octets'], 3000909)
        self.assertEqual(item['called_station_id'], '00-27-22-F3-FA-F1:hostname')
        item = response.data[2]
        self.assertEqual(item['output_octets'], 1119074409)
        self.assertEqual(item['input_octets'], 4440909)
        self.assertEqual(item['nas_ip_address'], '172.16.64.91')
        self.assertEqual(item['calling_station_id'], '5c:7d:c1:72:a7:3b')
