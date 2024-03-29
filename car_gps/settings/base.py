"""
Django settings for car_gps project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import datetime
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from rest_framework import settings
import environ

env = environ.Env(
	# set casting, default value
	DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Application definition

INSTALLED_APPS = [
	'simpleui',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'django_rest_passwordreset',
	'rest_framework_simplejwt',
	'rest_framework_simplejwt.token_blacklist',
	'django_seed',
	'crispy_forms',
	'authentication',
	'tracking_info',
	'user_profile',
	'promotions',
	'django_crontab',
	'fcm_django',
	'channels',
	'notifications',
	'import_export',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'car_gps.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'car_gps.wsgi.application'
ASGI_APPLICATION = "car_gps.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
	'default': env.db(),
}

# Password validation
PASSWORD_HASHERS = [
	'django.contrib.auth.hashers.PBKDF2PasswordHasher',
	'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
	'django.contrib.auth.hashers.Argon2PasswordHasher',
	'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
		'OPTIONS': {
			'min_length': 8,
		}
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

REST_FRAMEWORK = {
	# When you enable API versioning, the request.version attribute will contain a string
	# that corresponds to the version requested in the incoming client request.
	'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
	# Permission settings
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.IsAuthenticated'
	],
	# Authentication settings
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'rest_framework.authentication.TokenAuthentication',
		'rest_framework_simplejwt.authentication.JWTAuthentication',
		'rest_framework.authentication.BasicAuthentication',
	],
	# Pagination style
	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
	'PAGE_SIZE': 30,
}

SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=90),
	'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=90),
	'ROTATE_REFRESH_TOKENS': False,
	'BLACKLIST_AFTER_ROTATION': True,

	'ALGORITHM': 'HS256',
	'SIGNING_KEY': SECRET_KEY,
	'VERIFYING_KEY': None,
	'AUDIENCE': None,
	'ISSUER': None,

	'AUTH_HEADER_TYPES': ('Bearer',),
	'USER_ID_FIELD': 'id',
	'USER_ID_CLAIM': 'user_id',

	'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
	'TOKEN_TYPE_CLAIM': 'token_type',

	'JTI_CLAIM': 'jti',

	'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
	'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=1),
	'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'root': {
		'level': 'INFO',
		'handlers': ['file'],
	},
	'formatters': {
		'default': {
			'format': '%(levelname)s %(asctime)s %(message)s'
		}
	},
	'handlers': {
		'file': {
			'level': 'INFO',
			'class': 'logging.FileHandler',
			'formatter': 'default',
			'filename': os.path.join(BASE_DIR, 'log/general.log')
		}
	},
	'loggers': {
		'django': {
			'level': 'INFO',
			'handlers': ['file'],
			'propagate': True,
		}
	}
}

CRONJOBS = [
	('0 0 * * *', 'tracking_info.cron.db_rotation_job', '>> {}'.format(os.path.join(BASE_DIR, 'log/scheduled_job.log'))),
]

FCM_DJANGO_SETTINGS = {
	# default: _('FCM Django')
	"APP_VERBOSE_NAME": "[Vinatrack GPS]",
	# Your firebase API KEY
	"FCM_SERVER_KEY": env('FCM_SERVER_KEY'),
	# true if you want to have only one active device per registered user at a time
	# default: False
	"ONE_DEVICE_PER_USER": False,
	# devices to which notifications cannot be sent,
	# are deleted upon receiving error response from FCM
	# default: False
	"DELETE_INACTIVE_DEVICES": False,
}

EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
	# Extra lookup directories for collectstatic to find static files
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOCALE_PATHS = ( os.path.join(BASE_DIR, 'locale'), )
CRISPY_TEMPLATE_PACK = 'bootstrap4'

CHANNEL_LAYERS = {
	'default': {
		'BACKEND': 'channels_redis.core.RedisChannelLayer',
		'CONFIG': {
			"hosts": [('127.0.0.1', 6379)],
		},
	},
}

# Setting for admin template UI
SIMPLEUI_HOME_ICON = 'fas fa-user-shield'
SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_HOME_ACTION = True
SIMPLEUI_ANALYSIS = True

