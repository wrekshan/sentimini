"""
Django settings for sentimini project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url
import socket

#Grab this for later with the local vs web shit

if socket.gethostname().startswith('myhost.local'):
    LIVEHOST = False
else: 
    LIVEHOST = True
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%l(q-u@mf%m43cw(3jw0*u1ajed27atox$#e^64(u4bil#du3r'

# SECURITY WARNING: don't run with debug turned on in production!

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
     #ALL AUTH STUFF
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', #i think you need this for all auth
    'crispy_forms', #for forms
    'datetimewidget',
    'import_export',

    #my apps
    'ent',
    'vis',
    'power',
    'professional',
    
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sentimini.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        # 'DIRS': [], #This is the empty one
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

WSGI_APPLICATION = 'sentimini.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

#This was default.  THis is assuming that the static files are wihtin the app directory
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


######## THIS IS FROM THE HEROKU DOCS
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# # Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


######## THIS IS FROM THE HEROKU DOCS


######## MAYBE DELETE


# ACTIVATION STUFF
# auth and allauth settings
LOGIN_REDIRECT_URL = '/consumer/home/'
SITE_ID = 1

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}

# ACCOUNT_EMAIL_REQUIRED=True

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)
# ACTIVATION STUFF END


# ACCOUNT_EMAIL_VERIFICATION = True # Set this to wait for the email to register account



#Email Stuff
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend' # this is to print to console
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.sep.join([os.path.dirname(os.path.dirname(__file__)), 'tmp_email'])



DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

if LIVEHOST:
    # EMAIL_USE_TLS = True
    # EMAIL_HOST = 'smtp.gmail.com'
    # EMAIL_HOST_USER = 'sentimini@gmail.com'
    # EMAIL_HOST_PASSWORD = os.environ['GMAIL_KEY']
    # EMAIL_PORT = 587
    SECURE_SSL_REDIRECT = True
    DEFAULT_FROM_EMAIL = 'system@sentimini.com'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.zoho.com'
    EMAIL_HOST_USER = 'system@sentimini.com'
    EMAIL_HOST_PASSWORD = os.environ['GMAIL_KEY']
    EMAIL_PORT = 587

    use_gmail = 0

    ### THESE ARE THE NON-LOCAL STUFF
    DATABASES['default'] = dj_database_url.config()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') #don't know what this line is doing
    ### COMMET AND UNCOMMENT THESE

    #These were different than static
    ALLOWED_HOSTS = ['sentimini.com','www.sentimini.com'] 
    DEBUG = False
else:
    DEFAULT_FROM_EMAIL = 'system_dev@sentimini.com'
    ### LOCAL
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.zoho.com'
    EMAIL_HOST_USER = 'system_dev@sentimini.com'
    EMAIL_HOST_PASSWORD = 'wr579351'
    EMAIL_PORT = 587

    use_gmail = 0

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'emojinsei_db',
            'USER': 'williamrekshan',
            'PASSWORD': 'wr579351',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    ALLOWED_HOSTS = ['*'] 
    DEBUG = True


