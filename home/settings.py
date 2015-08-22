import os

from configurations import Configuration, values
from kombu import Queue, Exchange


class Base(Configuration):
    SECRET_KEY = values.SecretValue()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'home',
        'games',
        'djcelery',
        'smart_downloader',
        'say',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'home.urls'

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

    WSGI_APPLICATION = 'home.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'database.sqlite3'),
        }
    }


    # Internationalization
    # https://docs.djangoproject.com/en/1.8/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.8/howto/static-files/

    STATIC_URL = '/static/'
    MEDIA_URL = 'http://franhp.no-ip.org/media/'


    # Celery
    BROKER_URL = 'amqp://guest:guest@localhost//'

    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
    CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('downloads', Exchange('downloads'), routing_key='downloads'),
    )
    CELERY_DEFAULT_QUEUE = 'default'
    CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
    CELERY_DEFAULT_ROUTING_KEY = 'default'


class Dev(Base):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    ALLOWED_HOSTS = ['127.0.0.1']

    # Transmission
    TRANSMISSION_HOST = 'localhost'
    TRANSMISSION_PORT = 9091

    # Video Downloader
    DEFAULT_OUTPUT_DIR = os.path.join('~', 'Downloads')


class Prod(Base):
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    ALLOWED_HOSTS = ['*']

    # Transmission
    TRANSMISSION_HOST = os.environ.get('TRANSMISSION_HOST', 'localhost')
    TRANSMISSION_PORT = os.environ.get('TRANSMISSION_PORT', 9091)

    # Video Downloader
    DEFAULT_OUTPUT_DIR = os.environ.get(
        'DEFAULT_OUTPUT_DIR', os.path.join('~', 'Downloads'))
