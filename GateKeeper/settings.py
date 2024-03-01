import os
from pathlib import Path
from dotenv import load_dotenv
import binascii

print("Loading settings.py...")

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print("\nSettings | BASE_DIR:", BASE_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', f'random-securet-key-{int(binascii.hexlify(os.urandom(64)), 16)}#'
)

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
print("Settings | DEBUG:", DEBUG)

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', ''
).strip().replace(" ", "").split(',')

print("Settings | ALLOWED_HOSTS:", ALLOWED_HOSTS)

SERVER_PORT = os.environ.get('PORT', '2087')
print("Settings | SERVER_PORT:", SERVER_PORT)

AUTH_USER_MODEL = 'core.UserAccount'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core.apps.CoreConfig"
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GateKeeper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'GateKeeper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}

print("Settings | DATABASES_ENGINE:", DATABASES.get('default').get('ENGINE'))
print("Settings | DATABASES_NAME:", DATABASES.get('default').get('NAME'))


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


print("Settings | STATIC_URL:", STATIC_URL)
print("Settings | STATICFILES_DIRS:", STATICFILES_DIRS)
print("Settings | STATIC_ROOT:", STATIC_ROOT)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
