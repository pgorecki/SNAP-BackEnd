"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from configurations import Configuration, values
from django.utils.log import DEFAULT_LOGGING
import logging.config


class BaseConfiguration(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = 'secret'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = values.ListValue([])

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'rest_framework',
        'rest_framework.authtoken',
        'corsheaders',
        'drf_yasg',
        'core',
        'agency',
        'client',
        'survey',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        # 'core.middleware.UserProfileMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'backend.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

    WSGI_APPLICATION = 'backend.wsgi.application'

    DATABASES = values.DatabaseURLValue()

    # Password validation
    # https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 6,
            }
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/

    STATIC_URL = '/static/'

    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],
    }

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:3030',
    ]
    CORS_ORIGIN_REGEX_WHITELIST = [
        'http://localhost:3030',
    ]

    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'DRF Token': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        }
    }

    # Logging

    LOGGING_CONFIG = None
    LOGLEVEL = values.Value('DEBUG')

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                # exact format is not important, this is the minimum information
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            },
            'django.server': DEFAULT_LOGGING['formatters']['django.server'],
        },
        'handlers': {
            # console logs to stderr
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            # Add Handler for Sentry for `warning` and above
            # 'sentry': {
            #     'level': 'WARNING',
            #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            # },
            'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        },
        'loggers': {
            # default for all undefined Python modules
            '': {
                'level': 'WARNING',
                'handlers': ['console'],  # 'sentry'],
            },
            # Our application code
            'app': {
                'level': str(LOGLEVEL).upper(),
                'handlers': ['console'],  # , 'sentry'],
                # Avoid double logging because of root logger
                'propagate': False,
            },
            # Prevent noisy modules from logging to Sentry
            'noisy_module': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            # Default runserver request logging
            'django.server': DEFAULT_LOGGING['loggers']['django.server'],
        },
    })

    def __init__(self):
        print(f'Using {self.__class__.__name__} config')


class Dev(BaseConfiguration):
    DEBUG = True
    AUTH_PASSWORD_VALIDATORS = []
    STATIC_ROOT = f"{BaseConfiguration.BASE_DIR}/static/"


class Test(BaseConfiguration):
    DEBUG = True


class Staging(BaseConfiguration):
    DEBUG = False
    # SENTRY_DSN = values.URLValue(environ_required=True)
    STATIC_ROOT = "/host/static/"
    MEDIA_ROOT = "/host/uploads/"
    ALLOWED_HOSTS = ['*']

    SECRET_KEY = values.SecretValue()

    # EMAIL = values.EmailURLValue()

    @classmethod
    def post_setup(cls):
        print('Using Staging config')
        # super().post_setup()
        # import sentry_sdk
        # from sentry_sdk.integrations.django import DjangoIntegration

        # sentry_sdk.init(
        #     dsn=str(cls.SENTRY_DSN), integrations=[DjangoIntegration()], environment="Staging"
        # )
