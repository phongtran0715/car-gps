from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ALLOWED_HOSTS = ['spidermen.xyz', 'dev.vina.spidermen.xyz', 'vina.spidermen.xyz', '167.179.80.179']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
