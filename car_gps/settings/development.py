from .base import *

DEBUG = False

ALLOWED_HOSTS = ['clover.gotechjsc.com', '172.31.40.49']

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