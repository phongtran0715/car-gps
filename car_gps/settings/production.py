from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['spidermen.xyz', 'dev.vina.spidermen.xyz', 'vina.spidermen.xyz', '167.179.80.179', 'vinatrackgps.vn', 'vinatrackgps.com']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
