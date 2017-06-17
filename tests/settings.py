import os

import environ

import swapper

DJANGO_FREERADIUS_RADIUSREPLY_MODEL = "django_freeradius.RadiusReply"
DJANGO_FREERADIUS_RADIUSCHECK_MODEL = "django_freeradius.RadiusCheck"
DJANGO_FREERADIUS_RADIUSUSERGROUP_MODEL = "django_freeradius.RadiusUserGroup"
DJANGO_FREERADIUS_RADIUSGROUP_MODEL = "django_freeradius.RadiusGroup"
DJANGO_FREERADIUS_RADIUSACCOUNTING_MODEL = "django_freeradius.RadiusAccounting"
DJANGO_FREERADIUS_RADIUSPOSTAUTHENTICATION_MODEL = "django_freeradius.RadiusPostAuthentication"
DJANGO_FREERADIUS_RADIUSGROUPREPLY_MODEL = "django_freeradius.RadiusGroupReply"
DJANGO_FREERADIUS_RADIUSGROUPCHECK_MODEL = "django_freeradius.RadiusGroupCheck"
DJANGO_FREERADIUS_RADIUSGROUPUSER_MODEL = "django_freeradius.RadiusGroupUser"
DJANGO_FREERADIUS_NAS_MODEL = "django_freeradius.RadiusReply"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False), )
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
    'django.contrib.admin',
    'django_freeradius'
]

MIDDLEWARE_CLASSES = [
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# local settings must be imported before test runner otherwise they'll be ignored
try:
    from local_settings import *
except ImportError:
    pass
