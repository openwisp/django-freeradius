import os
import sys

import environ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTING = sys.argv[1] == 'test'

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': env.db(default='sqlite:///django-freeradius.db'),
}

SECRET_KEY = 'fn)t*+$)ugeyip6-#txyy$5wf2ervc0d2n#h)qb)y5@ly$t*@w'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'openwisp_utils.admin_theme',
    'django.contrib.admin',
    'django_freeradius',
    'rest_framework',
    'django_filters',
    'django_extensions',
    # registration
    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'allauth.socialaccount.providers.facebook',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TIME_ZONE = 'Europe/Rome'
LANGUAGE_CODE = 'en-gb'
USE_TZ = True
USE_I18N = False
USE_L10N = False
STATIC_URL = '/static/'
CORS_ORIGIN_ALLOW_ALL = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
EMAIL_PORT = '1025'
MEDIA_URL = '/media/'

# during development only
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# change this to something secret in production
DJANGO_FREERADIUS_API_TOKEN = 'djangofreeradiusapitoken'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'openwisp_utils.loaders.DependencyLoader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'openwisp_utils.staticfiles.DependencyFinder',
]

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
        ],
        'VERIFIED_EMAIL': True,
    }
}
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False

if os.environ.get('SAMPLE_APP', False):
    INSTALLED_APPS.remove('django_freeradius')
    INSTALLED_APPS.append('sample_radius')
    EXTENDED_APPS = ['django_freeradius']
    DJANGO_FREERADIUS_RADIUSCHECK_MODEL = 'sample_radius.RadiusCheck'
    DJANGO_FREERADIUS_RADIUSREPLY_MODEL = 'sample_radius.RadiusReply'
    DJANGO_FREERADIUS_RADIUSGROUP_MODEL = 'sample_radius.RadiusGroup'
    DJANGO_FREERADIUS_RADIUSGROUPREPLY_MODEL = 'sample_radius.RadiusGroupReply'
    DJANGO_FREERADIUS_RADIUSGROUPCHECK_MODEL = 'sample_radius.RadiusGroupCheck'
    DJANGO_FREERADIUS_RADIUSUSERGROUP_MODEL = 'sample_radius.RadiusUserGroup'
    DJANGO_FREERADIUS_RADIUSACCOUNTING_MODEL = 'sample_radius.RadiusAccounting'
    DJANGO_FREERADIUS_NAS_MODEL = 'sample_radius.Nas'
    DJANGO_FREERADIUS_RADIUSPOSTAUTH_MODEL = 'sample_radius.RadiusPostAuth'
    DJANGO_FREERADIUS_RADIUSBATCH_MODEL = 'sample_radius.RadiusBatch'
    DJANGO_FREERADIUS_RADIUSTOKEN_MODEL = 'sample_radius.RadiusToken'

if TESTING:
    DJANGO_FREERADIUS_GROUPCHECK_ADMIN = True
    DJANGO_FREERADIUS_GROUPREPLY_ADMIN = True
    DJANGO_FREERADIUS_USERGROUP_ADMIN = True

DJANGO_FREERADIUS_EXTRA_NAS_TYPES = (
    ('cisco', 'Cisco Router'),
)

# local settings must be imported before test runner otherwise they'll be ignored
try:
    from local_settings import *
except ImportError:
    pass
