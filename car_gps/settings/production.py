from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['clover.gotechjsc.com', '172.31.40.49']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
