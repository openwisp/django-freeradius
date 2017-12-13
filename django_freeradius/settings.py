from django.conf import settings

EDITABLE_ACCOUNTING = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_ACCOUNTING', False)
EDITABLE_POSTAUTH = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_POSTAUTH', False)

DEFAULT_SECRET_FORMAT = getattr(settings,
                                'DJANGO_FREERADIUS_DEFAULT_SECRET_FORMAT',
                                'NT-Password')

DISABLED_SECRET_FORMATS = getattr(settings,
                                  'DISABLED_SECRET_FORMATS',
                                  ['Cleartext-Password',
                                   'LM-Password',
                                   'MD5-Password',
                                   'SMD5-Password',
                                   'SSHA-Password',
                                   'Crypt-Password'])

RADCHECK_SECRET_VALIDATORS = getattr(settings,
                                     'DJANGO_FREERADIUS_RADCHECK_SECRET_VALIDATORS',
                                     {'regexp_lowercase': '[a-z]+',
                                      'regexp_uppercase': '[A-Z]+',
                                      'regexp_number': '[0-9]+',
                                      'regexp_special': '[\!\%\-_+=\[\]\
                                                        {\}\:\,\.\?\<\>\(\)\;]+'})
