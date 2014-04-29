# Django settings for gazetteer project.
import os
from os.path import join

DEBUG = True
TEMPLATE_DEBUG = DEBUG

JSON_DEBUG = DEBUG
# DATA_DIR = '/home/sanj/c/gazetteer/data'
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
INTERNAL_IPS = ('127.0.0.1',)
MANAGERS = ADMINS

LOCAL_DEVELOPMENT = True

PROJECT_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gazetteer',                      # Or path to database file if using sqlite3.
        'USER': 'gazetteer',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(PROJECT_ROOT, 'media')

STATIC_ROOT = join(PROJECT_ROOT, 'static')

STATIC_URL = '/static/'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/static/'

# Make this unique, and don't share it with anybody.
#SECRET_KEY = '4a$-vh!9+^)rzhvq%uq)!qq)!4th=315o-q@-$2g81n0%(&c@a'

# Make this unique, creates random key first at first time.
try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            SECRET_KEY = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "places.context_processors.gazetteer_params",
)

AJAX_LOOKUP_CHANNELS = {
    # the simplest case, pass a DICT with the model and field to search against :
    'authority_record' : dict(model='places.authorityrecord', search_field='preferred_name'),
    'time_frame': dict(model='places.timeframe', search_field='description'),
    'feature_type': ('places.lookups', 'FeatureTypeLookup'),
    'feature': dict(model='places.feature', search_field='preferred_name'),
    # this generates a simple channel
    # specifying the model Track in the music app, and searching against the 'title' field

    # or write a custom search channel and specify that using a TUPLE
#    'contact' : ('peoplez.lookups', 'ContactLookup'),
    # this specifies to look for the class `ContactLookup` in the `peoplez.lookups` module
}

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'places',
    'django_extensions',
    'debug_toolbar',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
#    'django.contrib.admindocs',
    'ajax_select',
)

#Over-ride these in local_settings.py
GAZETTEER_PARAMS = {
    'supported_by_website_url': 'http://www.loc.gov/index.html',
    'supported_by_image_url': '/static/images/logo-loc.png',
#    'supported_by_name': 'Library of Congress'        
}

try:
  from local_settings import *
except:
  pass
