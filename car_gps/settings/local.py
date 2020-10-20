from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cjs!qp6i4cw7mj&*+bfel4wfi@u^&$uqk!)gk4_fx$lvy$u^u&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'car_gps_db',
        'USER': 'root',
        'PASSWORD': '123456aA@',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # During development only
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
