import json

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from freezegun import freeze_time
from rest_framework import status

from django_freeradius.settings import API_TOKEN

START_DATE = '2017-08-08 15:16:10+0200'

auth_header = "Bearer {}".format(API_TOKEN)
token_querystring = "?token={}".format(API_TOKEN)


class BaseTestApi(object):
    def test_disabled_user_login(self):
        User.objects.create_user(username='barbar', password='molly', is_active=False)
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'barbar', 'password': 'molly'},
                                    HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'control:Auth-Type': 'Reject'})

    def test_authorize_no_token_403(self):
        User.objects.create_user(username='molly', password='barbar')
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'molly', 'password': 'barbar'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'Token authentication failed'})

    def test_authorize_200(self):
        User.objects.create_user(username='molly', password='barbar')
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'molly', 'password': 'barbar'},
                                    HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'control:Auth-Type': 'Accept'})

    def test_authorize_200_querystring(self):
        User.objects.create_user(username='molly', password='barbar')
        post_url = "{}{}".format(reverse('freeradius:authorize'), token_querystring)
        response = self.client.post(post_url,
                                    {'username': 'molly', 'password': 'barbar'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'control:Auth-Type': 'Accept'})

    def test_authorize_401(self):
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'baldo', 'password': 'ugo'},
                                    HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'control:Auth-Type': 'Reject'})

    def test_postauth_accept_201(self):
        self.assertEqual(self.radius_postauth_model.objects.all().count(), 0)
        params = {'username': 'molly', 'password': 'barbar', 'reply': 'Access-Accept',
                  'called_station_id': '00-11-22-33-44-55:hostname',
                  'calling_station_id': '00:26:b9:20:5f:10'}
        response = self.client.post(reverse('freeradius:postauth'),
                                    params,
                                    HTTP_AUTHORIZATION=auth_header)
        params['password'] = ''
        self.assertEqual(self.radius_postauth_model.objects.filter(**params).count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_accept_201_querystring(self):
        self.assertEqual(self.radius_postauth_model.objects.all().count(), 0)
        params = {'username': 'molly', 'password': 'barbar', 'reply': 'Access-Accept',
                  'called_station_id': '00-11-22-33-44-55:hostname',
                  'calling_station_id': '00:26:b9:20:5f:10'}
        post_url = "{}{}".format(reverse('freeradius:postauth'), token_querystring)
        response = self.client.post(post_url, params)
        params['password'] = ''
        self.assertEqual(self.radius_postauth_model.objects.filter(**params).count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_reject_201(self):
        self.assertEqual(self.radius_postauth_model.objects.all().count(), 0)
        params = {'username': 'molly', 'password': 'barba', 'reply': 'Access-Reject'}
        response = self.client.post(reverse('freeradius:postauth'),
                                    params,
                                    HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(self.radius_postauth_model.objects.filter(username='molly',
                                                                   password='barba').count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_reject_201_empty_fields(self):
        params = {'username': 'molly', 'password': 'barba', 'reply': 'Access-Reject',
                  'called_station_id': '',
                  'calling_station_id': ''}
        response = self.client.post(reverse('freeradius:postauth'),
                                    params,
                                    HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(self.radius_postauth_model.objects.filter(**params).count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)

    def test_postauth_400(self):
        response = self.client.post(reverse('freeradius:postauth'), {},
                                    HTTP_AUTHORIZATION=auth_header)
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
        'framed_ip_address': '127.0.0.1'
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
                                HTTP_AUTHORIZATION=auth_header,
                                content_type='application/json')

    def assertAcctData(self, ra, data):
        """
        compares the values in data (dict)
        with the values of a RadiusAccounting instance
        to ensure they match
        """
        for key, value in data.items():
            if key == 'status_type':
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
        ra = self.radius_accounting_model.objects.create(**self._acct_initial_data)
        data = self.acct_post_data
        data['status_type'] = 'Start'
        response = self.post_json(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        ra.refresh_from_db()
        self.assertAcctData(ra, data)

    @freeze_time(START_DATE)
    def test_accounting_start_200_querystring(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        ra = self.radius_accounting_model.objects.create(**self._acct_initial_data)
        data = self.acct_post_data
        data['status_type'] = 'Start'
        post_url = "{}{}".format(self._acct_url, token_querystring)
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
            'framed_ip_address': '192.168.182.3'
        }
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
        response = self.post_json(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, None)
        self.assertEqual(self.radius_accounting_model.objects.count(), 1)
        self.assertAcctData(self.radius_accounting_model.objects.first(), data)

    @freeze_time(START_DATE)
    def test_accounting_update_200(self):
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)
        ra = self.radius_accounting_model.objects.create(**self._acct_initial_data)
        data = self.acct_post_data
        data['status_type'] = 'Interim-Update'
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
        ra = self.radius_accounting_model.objects.create(**self._acct_initial_data)
        # reload date object in order to store ra.start_time
        ra.refresh_from_db()
        start_time = ra.start_time
        data = self.acct_post_data
        data['status_type'] = 'Stop'
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
        response = self.post_json(self.acct_post_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('status_type', response.data)
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)

    @freeze_time(START_DATE)
    def test_accounting_400_invalid_status_type(self):
        data = self.acct_post_data
        data['status_type'] = 'INVALID'
        response = self.post_json(data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('status_type', response.data)
        self.assertEqual(self.radius_accounting_model.objects.count(), 0)

    @freeze_time(START_DATE)
    def test_accounting_400_validation_error(self):
        data = self.acct_post_data
        data['status_type'] = 'Start'
        del data['nas_ip_address']
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
        self.radius_accounting_model.objects.create(**data1)
        data2 = self.acct_post_data
        data2.update(dict(session_id='40111116',
                          unique_id='12234f69',
                          input_octets=3000909,
                          output_octets=1613176609))
        self.radius_accounting_model.objects.create(**data2)
        data3 = self.acct_post_data
        data3.update(dict(session_id='89897654',
                          unique_id='99144d60',
                          input_octets=4440909,
                          output_octets=1119074409))
        self.radius_accounting_model.objects.create(**data3)
        response = self.client.get('{0}?page_size=1&page=1'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['username'], 'admin')
        self.assertEqual(item['calling_station_id'], '5c:7d:c1:72:a7:3b')
        self.assertEqual(item['output_octets'], data1['output_octets'])
        self.assertEqual(item['input_octets'], data1['input_octets'])
        response = self.client.get('{0}?page_size=1&page=2'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['output_octets'], data2['output_octets'])
        self.assertEqual(item['nas_ip_address'], '172.16.64.91')
        self.assertEqual(item['input_octets'], data2['input_octets'])
        self.assertEqual(item['called_station_id'], '00-27-22-F3-FA-F1:hostname')
        response = self.client.get('{0}?page_size=1&page=3'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['output_octets'], data3['output_octets'])
        self.assertEqual(item['input_octets'], data3['input_octets'])
        self.assertEqual(item['nas_ip_address'], '172.16.64.91')
        self.assertEqual(item['calling_station_id'], '5c:7d:c1:72:a7:3b')

    def test_accounting_filter_username(self):
        data1 = self.acct_post_data
        data1.update(dict(username='test_user',
                          unique_id='75058e50'))
        self.radius_accounting_model.objects.create(**data1)
        data2 = self.acct_post_data
        data2.update(dict(username='admin',
                          unique_id='99144d60'))
        self.radius_accounting_model.objects.create(**data2)
        response = self.client.get('{0}?username=test_user'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['username'], 'test_user')

    def test_accounting_filter_called_station_id(self):
        data1 = self.acct_post_data
        data1.update(dict(called_station_id='E0-CA-40-EE-D1-0D',
                          unique_id='99144d60'))
        self.radius_accounting_model.objects.create(**data1)
        data2 = self.acct_post_data
        data2.update(dict(called_station_id='C0-CA-40-FE-E1-9D',
                          unique_id='85144d60'))
        self.radius_accounting_model.objects.create(**data2)
        response = self.client.get('{0}?called_station_id=E0-CA-40-EE-D1-0D'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['called_station_id'], 'E0-CA-40-EE-D1-0D')

    def test_accounting_filter_calling_station_id(self):
        data1 = self.acct_post_data
        data1.update(dict(calling_station_id='4c:8d:c2:80:a7:4c',
                          unique_id='99144d60'))
        self.radius_accounting_model.objects.create(**data1)
        data2 = self.acct_post_data
        data2.update(dict(calling_station_id='5c:6d:c2:80:a7:4c',
                          unique_id='85144d60'))
        self.radius_accounting_model.objects.create(**data2)
        response = self.client.get('{0}?calling_station_id=4c:8d:c2:80:a7:4c'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['calling_station_id'], '4c:8d:c2:80:a7:4c')

    @freeze_time(START_DATE)
    def test_accounting_filter_start_time(self):
        data1 = self.acct_post_data
        data1.update(dict(unique_id='99144d60'))
        self.radius_accounting_model.objects.create(**data1)
        data2 = self.acct_post_data
        data2.update(dict(start_time='2018-03-02T00:43:24.020460+01:00',
                          unique_id='85144d60'))
        self.radius_accounting_model.objects.create(**data2)
        response = self.client.get('{0}?start_time={1}'.format(self._acct_url, '2018-03-02'),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['start_time'], '2018-03-02T00:43:24.020460+01:00')

    @freeze_time(START_DATE)
    def test_accounting_filter_stop_time(self):
        data1 = self.acct_post_data
        data1.update(dict(stop_time=START_DATE,
                          unique_id='99144d60'))
        self.radius_accounting_model.objects.create(**data1)
        data2 = self.acct_post_data
        data2.update(dict(stop_time='2018-03-02T00:43:24.020460+01:00',
                          unique_id='85144d60'))
        self.radius_accounting_model.objects.create(**data2)
        response = self.client.get('{0}?stop_time={1}'.format(self._acct_url, '2018-03-02'),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['stop_time'], '2018-03-02T00:43:24.020460+01:00')

    def test_accounting_filter_is_open(self):
        data1 = self.acct_post_data
        data1.update(dict(stop_time=None,
                          unique_id='99144d60'))
        self.radius_accounting_model.objects.create(**data1)
        data2 = self.acct_post_data
        data2.update(dict(stop_time='2018-03-02T00:43:24.020460+01:00',
                          unique_id='85144d60'))
        self.radius_accounting_model.objects.create(**data2)
        response = self.client.get('{0}?is_open=true'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['stop_time'], None)
        response = self.client.get('{0}?is_open=false'.format(self._acct_url),
                                   HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item['stop_time'], '2018-03-02T00:43:24.020460+01:00')

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
            'framed_ip_address': ''
        }
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
            'framed_ip_address': ''
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
        response = self.client.post(reverse('freeradius:batch'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.radius_batch_model.objects.count(), 0)

    def test_batch_csv_201(self):
        self.assertEqual(self.radius_batch_model.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        text = 'user,cleartext$abcd,email@gmail.com,firstname,lastname'
        with open('test.csv', 'wb') as file:
            text2 = text.encode('utf-8')
            file.write(text2)
        with open('test.csv', 'rb') as file:
            data = {
                "name": "test",
                "strategy": "csv",
                "csvfile": file,
            }
            response = self.client.post(reverse('freeradius:batch'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.radius_batch_model.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)

    def test_batch_prefix_201(self):
        self.assertEqual(self.radius_batch_model.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        data = {
            "name": "test",
            "strategy": "prefix",
            "prefix": "prefix",
            "number_of_users": 1,
        }
        response = self.client.post(reverse('freeradius:batch'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.radius_batch_model.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
