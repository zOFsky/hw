import os
import cloudinary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!s%$qa&cn7e$n$3$7lb_e#3o8@5fls+2q5y$q&06$7+h3slu8o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'home',
    'users',
    'fit',
    'cloudinary',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'happy_walker.urls'

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

WSGI_APPLICATION = 'happy_walker.wsgi.application'

DATABASES = {
       'default': {
           'ENGINE': 'djongo',
           'NAME': 'mongodb',
           'HOST': '',
           'PORT': 27017,
       }
   }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DOMEN = 'localhost'

CLIENT_SECRETS_FILE = 'users/client_secret.json'
API_SERVICE_NAME = 'fitness'
API_VERSION = 'v1'
REDIRECT_URI = 'http://localhost:3000/oauth2callback'
REDIRECT_URI_CRED = 'http://localhost:3000/oauthWalker'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
# CLIENT_ID = os.environ['CLIENT_ID']
# CLIENT_SECRET = os.environ['CLIENT_SECRET']
CLIENT_ID = '273646785748-1iii0vgckdfr7cer7gu2had4dln55qvm.apps.googleusercontent.com'
CLIENT_SECRET = 'k40UuBJGSq2dnqkh_l3SyS2P'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

if "ENV" in os.environ:
    ENV = os.environ['ENV']
    if ENV == 'PROD':
        from happy_walker.dep_settings.prod_settings import *
    elif ENV == 'QA':
        from happy_walker.dep_settings.qa_settings import *
else:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    cloudinary.config(
        cloud_name="happywalker",
        api_key="167896788241779",
        api_secret="rOItkY1sukqTpA43jwcShJDGPsY"
    )

