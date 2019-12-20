import json

from dateutil import parser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now
from freezegun import freeze_time
from rest_framework import status

from django_freeradius import settings as app_settings

START_DATE = '2019-04-20T22:14:09+01:00'

User = get_user_model()


class BaseTestApi(object):
    def test_invalid_token(self):
        options = dict(username='molly', password='barbar')
        self._create_user(**options)
        auth_header = self.auth_header.replace(' ', '')  # removes spaces in token
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'molly', 'password': 'barbar'},
                                    HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, 400)

    def test_disabled_user_login(self):
        options = dict(username='barbar', password='molly', is_active=False)
        self._create_user(**options)
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'barbar', 'password': 'molly'},
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)

    def test_authorize_no_token_403(self):
        options = dict(username='molly', password='barbar')
        self._create_user(**options)
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'molly', 'password': 'barbar'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Token authentication failed'})

    def test_authorize_200(self):
        options = dict(username='molly', password='barbar')
        self._create_user(**options)
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'molly', 'password': 'barbar'},
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'control:Auth-Type': 'Accept'})

    def test_authorize_200_querystring(self):
        options = dict(username='molly', password='barbar')
        self._create_user(**options)
        post_url = "{}{}".format(reverse('freeradius:authorize'), self.token_querystring)
        response = self.client.post(post_url,
                                    {'username': 'molly', 'password': 'barbar'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'control:Auth-Type': 'Accept'})

    def test_authorize_failed(self):
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'baldo', 'password': 'ugo'},
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)

    def test_authorize_wrong_password(self):
        self._create_user(username='tester', password='tester123')
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'tester', 'password': 'wrong'},
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)

    def test_postauth_accept_201(self):
        self.assertEqual(self.radius_postauth_model.objects.all().count(), 0)
        params = self._get_postauth_params()
        response = self.client.post(reverse('freeradius:postauth'),
                                    params,
                                    HTTP_AUTHORIZATION=self.auth_header)
        params['password'] = ''
        self.assertEqual(self.radius_postauth_model.objects.filter(**params).count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_accept_201_querystring(self):
        self.assertEqual(self.radius_postauth_model.objects.all().count(), 0)
        params = self._get_postauth_params()
        post_url = "{}{}".format(reverse('freeradius:postauth'), self.token_querystring)
        response = self.client.post(post_url, params)
        params['password'] = ''
        self.assertEqual(self.radius_postauth_model.objects.filter(**params).count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_reject_201(self):
        self.assertEqual(self.radius_postauth_model.objects.all().count(), 0)
        params = {'username': 'molly', 'password': 'barba', 'reply': 'Access-Reject'}
        params = self._get_postauth_params(**params)
        response = self.client.post(reverse('freeradius:postauth'),
                                    params,
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_postauth_model.objects.filter(username='molly',
                                                                   password='barba').count(), 1)

    def test_postauth_reject_201_empty_fields(self):
        params = {'reply': 'Access-Reject',
                  'called_station_id': '',
                  'calling_station_id': ''}
        params = self._get_postauth_params(**params)
        response = self.client.post(reverse('freeradius:postauth'),
                                    params,
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(self.radius_postauth_model.objects.filter(**params).count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_400(self):
        response = self.client.post(reverse('freeradius:postauth'), {},
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(self.radius_postauth_model.objects.all().count(), 0)
        self.assertEqual(response.status_code, 400)

    def test_postauth_no_token_403(self):
        response = self.client.post(reverse('freeradius:postauth'), {})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Token authentication failed'})

    _acct_url = reverse('freeradius:accounting')
    _acct_initial_data = {
        'unique_id': '75058e50',
        'session_id': '35000006',
        'nas_ip_address': '172.16.64.91',
        'session_time': 0,
        'input_octets': 0,
        'output_octets': 0,
    }
    _acct_post_data = {
        'username': 'admin',
        'realm': '',
        'nas_port_id': '1',
        'nas_port_type': 'Async',
        'session_time': '261',
        'authentication': 'RADIUS',
        'input_octets': '1111909',
        'output_octets': '1511074444',
        'called_station_id': '00-27-22-F3-FA-F1:hostname',
        'calling_station_id': '5c:7d:c1:72:a7:3b',
        'terminate_cause': 'User_Request',
        'service_type': 'Login-User',
        'framed_protocol': 'test',
        'framed_ip_address': '127.0.0.1',
        'framed_ipv6_address': '::1',
        'framed_ipv6_prefix': '0::/64',
        'framed_interface_id': '0000:0000:0000:0001',
        'delegated_ipv6_prefix': '0::/64'
    }

    @property
    def acct_post_data(self):
        """ returns a copy of self._acct_data """
        data = self._acct_initial_data.copy()
        data.update(self._acct_post_data.copy())
        return data

    def post_json(self, data):
        """
        performs a post using application/json as content type
        emulating the exact behaviour of freeradius 3
        """
        return self.client.post(self._acct_url,
                                data=json.dumps(data),
                                HTTP_AUTHORIZATION=self.auth_header,
                                content_type='application/json')

    def assertAcctData(self, ra, data):
        """
        compares the values in data (dict)
        with the values of a RadiusAccounting instance
        to ensure they match
        """
        for key, value in data.items():
            if key in ('status_type', 'framed_ipv6_address'):
                continue
            ra_value = getattr(ra, key)
            data_value = data[key]
            _type = type(ra_value)
            if _type != type(data_value):
                data_value = _type(data_value)
            self.assertEqual(ra_value, data_value, msg=key)

    def test_accounting_no_token_403(self):
        response = self.client.post(self._acct_url, {})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Token authentication failed'})

    @freeze_time(START_DATE)
    def test_accounting_start_200(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        ra = self._create_radius_accounting(**self._acct_initial_data)
        data = self.acct_post_data
        data['status_type'] = 'Start'
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        ra.refresh_from_db()
        self.assertAcctData(ra, data)

    @freeze_time(START_DATE)
    def test_accounting_start_200_querystring(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        ra = self._create_radius_accounting(**self._acct_initial_data)
        data = self.acct_post_data
        data['status_type'] = 'Start'
        data = self._get_accounting_params(**data)
        post_url = "{}{}".format(self._acct_url, self.token_querystring)
        response = self.client.post(post_url, json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        ra.refresh_from_db()
        self.assertAcctData(ra, data)

    @freeze_time(START_DATE)
    def test_accounting_start_coova_chilli(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        data = {
            'status_type': 'Start',
            'session_id': '5a4f59aa00000001',
            'unique_id': 'd11a8069e261040d8b01b9135bdb8dc9',
            'username': 'username',
            'realm': '',
            'nas_ip_address': '192.168.182.1',
            'nas_port_id': '1',
            'nas_port_type': 'Wireless-802.11',
            'session_time': '',
            'authentication': '',
            'input_octets': '',
            'output_octets': '',
            'called_station_id': 'C0-4A-00-EE-D1-0D',
            'calling_station_id': 'A4-02-B9-D3-FD-29',
            'terminate_cause': '',
            'service_type': '',
            'framed_protocol': '',
            'framed_ip_address': '192.168.182.3',
            'framed_ipv6_address': '::ffff:c0a8:b603',
            'framed_ipv6_prefix': '0::/64',
            'framed_interface_id': '0000:ffff:c0a8:b603',
            'delegated_ipv6_prefix': '0::/64'
        }
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        ra = self.radius_accounting_model.objects.last()
        ra.refresh_from_db()
        data['session_time'] = 0
        data['input_octets'] = 0
        data['output_octets'] = 0
        self.assertEqual(ra.session_time, 0)
        self.assertEqual(ra.input_octets, 0)
        self.assertEqual(ra.output_octets, 0)
        self.assertAcctData(ra, data)

    @freeze_time(START_DATE)
    def test_accounting_start_201(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        data = self.acct_post_data
        data['status_type'] = 'Start'
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        self.assertAcctData(self.radius_accounting_model.objects.first(), data)

    @freeze_time(START_DATE)
    def test_accounting_update_200(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        ra = self._create_radius_accounting(**self._acct_initial_data)
        data = self.acct_post_data
        data['status_type'] = 'Interim-Update'
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        ra.refresh_from_db()
        self.assertEqual(ra.update_time.timetuple(), now().timetuple())
        self.assertAcctData(ra, data)

    @freeze_time(START_DATE)
    def test_accounting_update_201(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        data = self.acct_post_data
        data['status_type'] = 'Interim-Update'
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        ra = self.radius_accounting_model.objects.first()
        self.assertEqual(ra.update_time.timetuple(), now().timetuple())
        self.assertAcctData(ra, data)

    @freeze_time(START_DATE)
    def test_accounting_stop_200(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        ra = self._create_radius_accounting(**self._acct_initial_data)
        # reload date object in order to store ra.start_time
        ra.refresh_from_db()
        start_time = ra.start_time
        data = self.acct_post_data
        data['status_type'] = 'Stop'
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        ra.refresh_from_db()
        self.assertEqual(ra.update_time.timetuple(), now().timetuple())
        self.assertEqual(ra.stop_time.timetuple(), now().timetuple())
        self.assertEqual(ra.start_time, start_time)
        self.assertAcctData(ra, data)

    @freeze_time(START_DATE)
    def test_accounting_stop_201(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        data = self.acct_post_data
        data['status_type'] = 'Stop'
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        ra = self.radius_accounting_model.objects.first()
        self.assertEqual(ra.update_time.timetuple(), now().timetuple())
        self.assertEqual(ra.stop_time.timetuple(), now().timetuple())
        self.assertEqual(ra.start_time.timetuple(), now().timetuple())
        self.assertAcctData(ra, data)

    @freeze_time(START_DATE)
    def test_accounting_400_missing_status_type(self):
        data = self._get_accounting_params(**self.acct_post_data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('status_type', response.data)
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)

    @freeze_time(START_DATE)
    def test_accounting_400_invalid_status_type(self):
        data = self.acct_post_data
        data['status_type'] = 'INVALID'
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('status_type', response.data)
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)

    @freeze_time(START_DATE)
    def test_accounting_400_validation_error(self):
        data = self.acct_post_data
        data['status_type'] = 'Start'
        del data['nas_ip_address']
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('nas_ip_address', response.data)
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)

    def test_accounting_list_200(self):
        data1 = self.acct_post_data
        data1.update(dict(session_id='35000006',
                          unique_id='75058e50',
                          input_octets=9900909,
                          output_octets=1513075509))
        self._create_radius_accounting(**data1)
        data2 = self.acct_post_data
        data2.update(dict(session_id='40111116',
                          unique_id='12234f69',
                          input_octets=3000909,
                          output_octets=1613176609))
        self._create_radius_accounting(**data2)
        data3 = self.acct_post_data
        data3.update(dict(session_id='89897654',
                          unique_id='99144d60',
                          input_octets=4440909,
                          output_octets=1119074409))
        self._create_radius_accounting(**data3)
        response = self.client.get('{0}?page_size=1&page=1'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['output_octets'], data3['output_octets'])
        self.assertEqual(item['input_octets'], data3['input_octets'])
        self.assertEqual(item['nas_ip_address'], '172.16.64.91')
        self.assertEqual(item['calling_station_id'], '5c:7d:c1:72:a7:3b')
        response = self.client.get('{0}?page_size=1&page=2'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['output_octets'], data2['output_octets'])
        self.assertEqual(item['nas_ip_address'], '172.16.64.91')
        self.assertEqual(item['input_octets'], data2['input_octets'])
        self.assertEqual(item['called_station_id'], '00-27-22-F3-FA-F1:hostname')
        response = self.client.get('{0}?page_size=1&page=3'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['username'], 'admin')
        self.assertEqual(item['calling_station_id'], '5c:7d:c1:72:a7:3b')
        self.assertEqual(item['output_octets'], data1['output_octets'])
        self.assertEqual(item['input_octets'], data1['input_octets'])

    def test_accounting_filter_username(self):
        data1 = self.acct_post_data
        data1.update(dict(username='test_user',
                          unique_id='75058e50'))
        self._create_radius_accounting(**data1)
        data2 = self.acct_post_data
        data2.update(dict(username='admin',
                          unique_id='99144d60'))
        self._create_radius_accounting(**data2)
        response = self.client.get('{0}?username=test_user'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['username'], 'test_user')

    def test_accounting_filter_called_station_id(self):
        data1 = self.acct_post_data
        data1.update(dict(called_station_id='E0-CA-40-EE-D1-0D',
                          unique_id='99144d60'))
        self._create_radius_accounting(**data1)
        data2 = self.acct_post_data
        data2.update(dict(called_station_id='C0-CA-40-FE-E1-9D',
                          unique_id='85144d60'))
        self._create_radius_accounting(**data2)
        response = self.client.get('{0}?called_station_id=E0-CA-40-EE-D1-0D'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['called_station_id'], 'E0-CA-40-EE-D1-0D')

    def test_accounting_filter_calling_station_id(self):
        data1 = self.acct_post_data
        data1.update(dict(calling_station_id='4c:8d:c2:80:a7:4c',
                          unique_id='99144d60'))
        self._create_radius_accounting(**data1)
        data2 = self.acct_post_data
        data2.update(dict(calling_station_id='5c:6d:c2:80:a7:4c',
                          unique_id='85144d60'))
        self._create_radius_accounting(**data2)
        response = self.client.get('{0}?calling_station_id=4c:8d:c2:80:a7:4c'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['calling_station_id'], '4c:8d:c2:80:a7:4c')

    @freeze_time(START_DATE)
    def test_accounting_filter_start_time(self):
        data1 = self.acct_post_data
        data1.update(dict(unique_id='99144d60'))
        self._create_radius_accounting(**data1)
        data2 = self.acct_post_data
        data2.update(dict(start_time='2018-03-02T00:43:24.020460+01:00',
                          unique_id='85144d60'))
        ra = self._create_radius_accounting(**data2)
        response = self.client.get('{0}?start_time={1}'.format(self._acct_url, '2018-03-01'),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, 200)
        item = response.data[-1]
        self.assertEqual(parser.parse(item['start_time']), ra.start_time)

    @freeze_time(START_DATE)
    def test_accounting_filter_stop_time(self):
        data1 = self.acct_post_data
        data1.update(dict(start_time=START_DATE,
                          stop_time=START_DATE.replace('04-20', '04-21'),
                          unique_id='99144d60'))
        self._create_radius_accounting(**data1)
        data2 = self.acct_post_data
        stop_time = '2018-03-02T11:43:24.020460+01:00'
        data2.update(dict(start_time='2018-03-02T10:43:24.020460+01:00',
                          stop_time=stop_time,
                          unique_id='85144d60'))
        ra = self._create_radius_accounting(**data2)
        response = self.client.get('{0}?stop_time={1}'.format(self._acct_url, '2018-03-02 21:43:25'),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(parser.parse(item['stop_time']), ra.stop_time)

    def test_accounting_filter_is_open(self):
        data1 = self.acct_post_data
        data1.update(dict(stop_time=None,
                          unique_id='99144d60'))
        self._create_radius_accounting(**data1)
        data2 = self.acct_post_data
        data2.update(dict(stop_time='2018-03-02T00:43:24.020460+01:00',
                          unique_id='85144d60'))
        ra = self._create_radius_accounting(**data2)
        response = self.client.get('{0}?is_open=true'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['stop_time'], None)
        response = self.client.get('{0}?is_open=false'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(parser.parse(item['stop_time']), ra.stop_time)

    @freeze_time(START_DATE)
    def test_coova_accounting_on_200(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        data = {
            'status_type': 'Accounting-On',
            'session_id': '',
            'unique_id': '569533dad629d47d8b122826d3ed7f3d',
            'username': '',
            'realm': '',
            'nas_ip_address': '192.168.182.1',
            'nas_port_id': '',
            'nas_port_type': 'Wireless-802.11',
            'session_time': '',
            'authentication': '',
            'input_octets': '',
            'output_octets': '',
            'called_station_id': 'C0-4A-00-EE-D1-0D',
            'calling_station_id': '00-00-00-00-00-00',
            'terminate_cause': '',
            'service_type': '',
            'framed_protocol': '',
            'framed_ip_address': '',
            'framed_ipv6_address': '',
            'framed_ipv6_prefix': '',
            'framed_interface_id': '',
            'delegated_ipv6_prefix': ''
        }
        data = self._get_accounting_params(**data)
        response = self.post_json(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)

    @freeze_time(START_DATE)
    def test_coova_accounting_off_200(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        data = {
            'status_type': 'Accounting-Off',
            'session_id': '',
            'unique_id': '569533dad629d47d8b122826d3ed7f3d',
            'username': '',
            'realm': '',
            'nas_ip_address': '192.168.182.1',
            'nas_port_id': '',
            'nas_port_type': 'Wireless-802.11',
            'session_time': '',
            'authentication': '',
            'input_octets': '',
            'output_octets': '',
            'called_station_id': 'C0-4A-00-EE-D1-0D',
            'calling_station_id': '00-00-00-00-00-00',
            'terminate_cause': '0',
            'service_type': '',
            'framed_protocol': '',
            'framed_ip_address': '',
            'framed_ipv6_address': '',
            'framed_ipv6_prefix': '',
            'framed_interface_id': '',
            'delegated_ipv6_prefix': ''
        }
        response = self.post_json(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)

    def test_batch_bad_request_400(self):
        self.assertEqual(self.radius_batch_model.objects.count(), 0)
        data = {
            "name": "",
            "strategy": "prefix",
            "number_of_users": -1,
            "prefix": "",
        }
        response = self.client.post(reverse('freeradius:batch'), data,
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.radius_batch_model.objects.count(), 0)

    def test_batch_csv_201(self):
        self.assertEqual(self.radius_batch_model.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        text = 'user,cleartext$abcd,email@gmail.com,firstname,lastname'
        with open('{}/test.csv'.format(settings.MEDIA_ROOT), 'wb') as file:
            text2 = text.encode('utf-8')
            file.write(text2)
        with open('{}/test.csv'.format(settings.MEDIA_ROOT), 'rb') as file:
            data = self._get_post_defaults({
                "name": "test",
                "strategy": "csv",
                "csvfile": file,
            })
            response = self.client.post(reverse('freeradius:batch'), data,
                                        HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.radius_batch_model.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)

    def test_batch_prefix_201(self):
        self.assertEqual(self.radius_batch_model.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        data = self._get_post_defaults({
            "name": "test",
            "strategy": "prefix",
            "prefix": "prefix",
            "number_of_users": 1,
        })
        response = self.client.post(reverse('freeradius:batch'), data,
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.radius_batch_model.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)

    def test_api_batch_user_creation_no_users(self):
        data = {
            'strategy': 'prefix',
            'prefix': 'test',
            'name': 'test_name',
            'csvfile': '',
            'number_of_users': '',
            'modified': '',
        }
        response = self.client.post(
            reverse('freeradius:batch'),
            data,
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, 400)

    def test_get_authorize_view(self):
        url = '{}{}'.format(reverse('freeradius:authorize'), self.token_querystring)
        r = self.client.get(url, HTTP_ACCEPT='text/html')
        self.assertEqual(r.status_code, 405)
        expected = '<form action="{}'.format(reverse('freeradius:authorize'))
        self.assertIn(expected, r.content.decode())


class BaseTestApiReject(object):
    @classmethod
    def setUpClass(cls):
        app_settings.API_AUTHORIZE_REJECT = True

    @classmethod
    def tearDownClass(cls):
        app_settings.API_AUTHORIZE_REJECT = False

    def test_disabled_user_login(self):
        User.objects.create_user(username='barbar',
                                 password='molly',
                                 is_active=False)
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'barbar', 'password': 'molly'},
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'control:Auth-Type': 'Reject'})

    def test_authorize_401(self):
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'baldo', 'password': 'ugo'},
                                    HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'control:Auth-Type': 'Reject'})


class BaseTestAutoGroupname(object):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_settings.API_ACCOUNTING_AUTO_GROUP = True

    def test_automatic_groupname_account_enabled(self):
        user = self.user_model.objects.create_superuser(
            username='username1', email='admin@admin.com', password='qwertyuiop'
        )
        usergroup1 = self._create_radius_usergroup(groupname='group1', priority=2, username='testgroup1')
        usergroup2 = self._create_radius_usergroup(groupname='group2', priority=1, username='testgroup2')
        user.radiususergroup_set.set([usergroup1, usergroup2])
        self.client.post('/api/v1/accounting/{}'.format(self.token_querystring), {
            'status_type': 'Start',
            'session_time': '',
            'input_octets': '',
            'output_octets': '',
            'nas_ip_address': '127.0.0.1',
            'session_id': '48484',
            'unique_id': '1515151',
            'username': 'username1',
        })
        accounting_created = self.radius_accounting_model.objects.get(username='username1')
        self.assertEqual(accounting_created.groupname, 'group2')
        user.delete()


class BaseTestAutoGroupnameDisabled(object):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_settings.API_ACCOUNTING_AUTO_GROUP = False

    def test_account_creation_api_automatic_groupname_disabled(self):
        user = self.user_model.objects.create_superuser(
            username='username1',
            email='admin@admin.com',
            password='qwertyuiop'
        )
        usergroup1 = self._create_radius_usergroup(groupname='group1',
                                                   priority=2,
                                                   username='testgroup1')
        usergroup2 = self._create_radius_usergroup(groupname='group2',
                                                   priority=1,
                                                   username='testgroup2')
        user.radiususergroup_set.set([usergroup1, usergroup2])
        url = '{}{}'.format(reverse('freeradius:accounting'),
                            self.token_querystring)
        self.client.post(url, {
            'status_type': 'Start',
            'session_time': '',
            'input_octets': '',
            'output_octets': '',
            'nas_ip_address': '127.0.0.1',
            'session_id': '48484',
            'unique_id': '1515151',
            'username': 'username1',
        })
        accounting_created = self.radius_accounting_model \
                                 .objects.get(username='username1')
        self.assertIsNone(accounting_created.groupname)
        user.delete()


if app_settings.REST_USER_TOKEN_ENABLED:
    from rest_framework.authtoken.models import Token

    class BaseTestApiUserToken(object):
        def _get_url(self):
            return reverse('freeradius:user_auth_token')

        def test_user_auth_token_200(self):
            url = self._get_url()
            opts = dict(username='tester',
                        password='tester')
            self._create_user(**opts)
            response = self.client.post(url, opts)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['key'],
                             Token.objects.first().key)
            self.assertEqual(response.data['radius_user_token'],
                             self.radius_token_model.objects.first().key)

        def test_user_auth_token_400_credentials(self):
            url = self._get_url()
            opts = dict(username='tester',
                        password='tester')
            r = self.client.post(url, opts)
            self.assertEqual(r.status_code, 400)
            self.assertIn('Unable to log in',
                          r.json()['non_field_errors'][0])

    class BaseTestApiValidateToken:

        def _get_url(self):
            return reverse('freeradius:validate_auth_token')

        def get_user(self):
            opts = dict(username='tester',
                        password='tester')
            user = self._create_user(**opts)
            return user

        def test_validate_auth_token(self):
            url = self._get_url()
            user = self.get_user()
            token = Token.objects.create(user=user)
            # empty payload
            response = self.client.post(url)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.data['response_code'],
                             'BLANK_OR_INVALID_TOKEN')
            # invalid token
            payload = dict(token="some-random-string")
            response = self.client.post(url, payload)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.data['response_code'],
                             'BLANK_OR_INVALID_TOKEN')
            # valid token
            payload = dict(token=token.key)
            response = self.client.post(url, payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['response_code'],
                             'AUTH_TOKEN_VALIDATION_SUCCESSFUL')
            self.assertEqual(response.data['auth_token'],
                             token.key)
            self.assertEqual(response.data['radius_user_token'],
                             self.radius_token_model.objects.first().key)
