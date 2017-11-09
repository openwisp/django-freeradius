from django.conf import settings

EDITABLE_ACCOUNTING = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_ACCOUNTING', False)
EDITABLE_POSTAUTH = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_POSTAUTH', False)

DISABLED_SECRET_FORMAT = ['Cleartext-Password',
                          'LM-Password', 
                          'MD5-Password',
                          'SMD5-Password',
                          'SSHA-Password',
                          'Crypt-Password']
