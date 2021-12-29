from garpixcms.settings import *
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


INSTALLED_APPS += [
    'allauth',
    'allauth.account',
    'django_filters',
    'api',
    'djoser',

]

AUTH_USER_MODEL = 'user.User'


REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'user.serializers.UserSerializer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
        ('rest_framework.authentication.TokenAuthentication',
         'rest_framework.authentication.SessionAuthentication'),
    'DEFAULT_SCHEMA_CLASS':
        'rest_framework.schemas.coreapi.AutoSchema',
}

DJOSER = {
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
}
