from django.test import TestCase
from django.test import Client
from django.urls import reverse
import unittest
from .models import (Nas, RadiusAccounting, RadiusCheck, RadiusGroup,
                     RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
                     RadiusPostAuthentication, RadiusReply, RadiusUserGroup)


class UserTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_users_not_login(self):
        resp = self.client.get('/admin/auth/')
        self.assertEqual(resp.status_code, 302)

    def test_users(self):
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(resp.status_code, 200)



    def test_usersnas(self):
         nas = Nas.objects.create(nas_name='fiore', short_name='ff', type='cisco', secret='d', ports='22', community='vmv', description='ciao', server='jsjs')
         resp = self.client.get('/admin/django_freeradius/nas/1/change/')
         print (resp['Location']) #(reverse('admin:django_freeradius_nas_change', args=[nas.id]))
         self.assertContains(resp, 'ok', status_code=200)


     #def test_check(self):
        #RadiusCheck.objects.create(user_name='bob', attribute='Cleartext-Password', op=':=', value='passbob')
        #resp = self.client.post('/admin/django_freeradius/radiuscheck/1/change/')
        #self.assertContains(resp,'r')
