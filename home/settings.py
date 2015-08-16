import os
from configurations import Configuration, values


class Base(Configuration):
    SECRET_KEY = values.SecretValue()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

    ALLOWED_HOSTS = ['*']

    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'home',
        'transmission',
        'video_downloader',
        'games',
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


class Dev(Base):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    # Transmission
    TRANSMISSION_HOST = 'localhost'
    TRANSMISSION_PORT = 9091

    # Video Downloader
    DEFAULT_OUTPUT_DIR = os.path.join('~', 'Downloads')


class Prod(Base):
    DEBUG = False

    # Transmission
    TRANSMISSION_HOST = os.environ.get('TRANSMISSION_HOST', 'localhost')
    TRANSMISSION_PORT = os.environ.get('TRANSMISSION_PORT', 9091)

    # Video Downloader
    DEFAULT_OUTPUT_DIR = os.environ.get(
        'DEFAULT_OUTPUT_DIR', os.path.join('~', 'Downloads'))