from .base import *

DEBUG = False

ALLOWED_HOSTS = ALLOWED_HOSTS = ['spidermen.xyz', 'dev.vina.spidermen.xyz', 'vina.spidermen.xyz', '167.179.80.179']

INSTALLED_APPS += [
    'debug_toolbar',
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}