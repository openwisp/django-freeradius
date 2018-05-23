from django.contrib.auth import get_user_model

from django_freeradius.utils import find_available_username


class BaseTestUtils(object):
    def test_find_available_username(self):
        User = get_user_model()
        User.objects.create(username='rohith', password='password')
        self.assertEqual(find_available_username('rohith', []), 'rohith1')
        User.objects.create(username='rohith1', password='password')
        self.assertEqual(find_available_username('rohith', []), 'rohith2')
