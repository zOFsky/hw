import os

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']
# REDIRECT_URI = os.environ['REDIRECT_URI']
REDIRECT_URI = 'a-qa-frontend-happy-walker.herokuapp.com/oauth2callback'

ALLOWED_HOSTS = ['a-qa-backend-happy-walker.herokuapp.com', 'a-prod-backend-happy-walker.herokuapp.com']

DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'HOST': os.environ['DB_HOST'],
            'PORT': int(os.environ['DB_PORT']),
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'AUTH_SOURCE': os.environ['AUTH_SOURCE'],
        }
    }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# CORS_ORIGIN_WHITELIST = (
#     'https://heppy-walkernew.herokuapp.com',
#     'https://a-prod-frontend-happy-walker.herokuapp.com',
#     'https://a-qa-frontend-happy-walker.herokuapp.com'
# )