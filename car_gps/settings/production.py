from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['clover.gotechjsc.com']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
