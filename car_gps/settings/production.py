from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cjs!qp6i4cw7mj&*+bfel4wfi@u^&$uqk!)gk4_fx$lvy$u^u&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['clover.gotechjsc.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'car_gps',
        'USER': 'spiderboot',
        'PASSWORD': 'CloverDating@2019',
        'HOST': 'clover.gotechjsc.com',
        'PORT': '6688'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
