from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django_freeradius.utils import find_available_username, validate_csvfile


class BaseTestUtils(object):
    def test_find_available_username(self):
        User = get_user_model()
        User.objects.create(username='rohith', password='password')
        self.assertEqual(find_available_username('rohith', []), 'rohith1')
        User.objects.create(username='rohith1', password='password')
        self.assertEqual(find_available_username('rohith', []), 'rohith2')

    def test_validate_csvfile(self):
        with self.assertRaises(ValidationError) as error:
            validate_csvfile(open('django_freeradius/tests/static/test_batch_invalid.csv', 'rt'))
        self.assertTrue('Enter a valid email address' in error.exception.message)
        with self.assertRaises(ValidationError) as error:
            validate_csvfile(open('django_freeradius/tests/static/test_batch_improper.csv', 'rt'))
        self.assertTrue('Improper CSV format' in error.exception.message)
