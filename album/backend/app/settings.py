import rest_framework.authentication
from garpixcms.settings import *  # noqa
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'



INSTALLED_APPS += [
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'django_filters',
    'api',


]

AUTH_USER_MODEL = 'user.User'

ACCOUNT_USERNAME_REQUIRED = True

SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'user.serializers.UserSerializer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
        ('rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'),
}

