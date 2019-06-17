"""Django settings when running project in any environment."""
import os
import configparser

DEBUG = False
TESTING = False

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

django_env = os.getenv('DJANGO_ENV', 'local')

secrets = configparser.RawConfigParser()
secrets.read(os.path.join(ROOT_DIR, 'secrets.cfg'))
secrets = secrets[django_env]

SECRET_KEY = secrets.get('django_secret_key')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'tweets2text',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': secrets.get('db_name'),
        'USER': secrets.get('db_user'),
        'PASSWORD': secrets.get('db_password', ''),
        'HOST': secrets.get('db_host'),
        'PORT': secrets.getint('db_port'),
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # noqa
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/admin/login/'

TWITTER_CONSUMER_KEY = secrets.get('twitter_consumer_key')
TWITTER_CONSUMER_SECRET = secrets.get('twitter_consumer_secret')
TWITTER_ACCESS_TOKEN = secrets.get('twitter_access_token')
TWITTER_ACCESS_TOKEN_SECRET = secrets.get('twitter_access_token_secret')
TWITTER_API_ENV = secrets.get('twitter_api_env')
BOT_ACCOUNT_ID_STR = secrets.get('bot_account_id_str')
