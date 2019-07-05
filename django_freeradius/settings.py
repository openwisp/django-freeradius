import os

from django.conf import settings

EDITABLE_ACCOUNTING = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_ACCOUNTING', False)
EDITABLE_POSTAUTH = getattr(settings, 'DJANGO_FREERADIUS_EDITABLE_POSTAUTH', False)
GROUPCHECK_ADMIN = getattr(settings, 'DJANGO_FREERADIUS_GROUPCHECK_ADMIN', False)
GROUPREPLY_ADMIN = getattr(settings, 'DJANGO_FREERADIUS_GROUPREPLY_ADMIN', False)
USERGROUP_ADMIN = getattr(settings, 'DJANGO_FREERADIUS_USERGROUP_ADMIN', False)
DEFAULT_SECRET_FORMAT = getattr(settings,
                                'DJANGO_FREERADIUS_DEFAULT_SECRET_FORMAT',
                                'NT-Password')
DISABLED_SECRET_FORMATS = getattr(settings, 'DJANGO_FREERADIUS_DISABLED_SECRET_FORMATS', [])
RADCHECK_SECRET_VALIDATORS = getattr(settings,
                                     'DJANGO_FREERADIUS_RADCHECK_SECRET_VALIDATORS',
                                     {'regexp_lowercase': '[a-z]+',
                                      'regexp_uppercase': '[A-Z]+',
                                      'regexp_number': '[0-9]+',
                                      'regexp_special': '[\!\%\-_+=\[\]\
                                                        {\}\:\,\.\?\<\>\(\)\;]+'})
BATCH_DEFAULT_PASSWORD_LENGTH = getattr(settings, 'DJANGO_FREERADIUS_BATCH_DEFAULT_PASSWORD_LENGTH', 8)
BATCH_DELETE_EXPIRED = getattr(settings, 'DJANGO_FREERADIUS_BATCH_DELETE_EXPIRED', 18)
BATCH_MAIL_SUBJECT = getattr(settings, 'DJANGO_FREERADIUS_BATCH_MAIL_SUBJECT', 'Credentials')
BATCH_MAIL_MESSAGE = getattr(settings, 'DJANGO_FREERADIUS_BATCH_MAIL_MESSAGE', 'username: {}, password: {}')
BATCH_MAIL_SENDER = getattr(settings, 'DJANGO_FREERADIUS_BATCH_MAIL_SENDER', settings.DEFAULT_FROM_EMAIL)
BATCH_PDF_TEMPLATE = getattr(settings,
                             'DJANGO_FREERADIUS_BATCH_PDF_TEMPLATE',
                             os.path.join(os.path.dirname(__file__),
                                          'templates/django_freeradius/prefix_pdf.html'))
API_TOKEN = getattr(settings, 'DJANGO_FREERADIUS_API_TOKEN', None)
API_AUTHORIZE_REJECT = getattr(settings, 'DJANGO_FREERADIUS_API_AUTHORIZE_REJECT', False)
REST_USER_TOKEN_ENABLED = 'rest_framework.authtoken' in settings.INSTALLED_APPS
SOCIAL_LOGIN_ENABLED = 'allauth.socialaccount' in settings.INSTALLED_APPS
DISPOSABLE_RADIUS_USER_TOKEN = getattr(settings, 'DJANGO_FREERADIUS_DISPOSABLE_RADIUS_USER_TOKEN', True)
API_ACCOUNTING_AUTO_GROUP = getattr(settings, 'DJANGO_FREERADIUS_API_ACCOUNTING_AUTO_GROUP', True)
EXTRA_NAS_TYPES = getattr(settings, 'DJANGO_FREERADIUS_EXTRA_NAS_TYPES', tuple())
