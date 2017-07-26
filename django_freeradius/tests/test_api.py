import swapper
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")


class TestApi(TestCase):
    def test_authorize(self):
        User.objects.create_user(username='molly', password='barbar')
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'molly', 'password': 'barbar'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'control:Auth-Type': 'Accept'})

    def test_unauthorize(self):
        response = self.client.post(reverse('freeradius:authorize'),
                                    {'username': 'baldo', 'password': 'ugo'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'control:Auth-Type': 'Reject'})

    def test_postauth_accept(self):
        RadiusPostAuth.objects.all().count()
        self.assertEqual(RadiusPostAuth.objects.all().count(), 0)
        response = self.client.post(reverse('freeradius:postauth'),
                                    {'username': 'molly', 'password': 'barbar', 'reply': 'Access-Accept'})
        self.assertEqual(RadiusPostAuth.objects.filter(username='molly', password='').count(), 1)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {''})

    def test_postauth_reject(self):
        RadiusPostAuth.objects.all().count()
        self.assertEqual(RadiusPostAuth.objects.all().count(), 0)
        response = self.client.post(reverse('freeradius:postauth'),
                                    {'username': 'molly', 'password': 'barba', 'reply': 'Access-Reject'})
        self.assertEqual(RadiusPostAuth.objects.filter(username='molly', password='barba').count(), 1)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {''})
