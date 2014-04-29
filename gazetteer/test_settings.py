from settings import *

#
# Settings file for use with the tests, so that they use sqlite and a custom ES index
#
#TODO - look into using spatialite if that speeds things up?
#DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
DEBUG = False #set DEBUG to 'production' mode
DATABASES['default'] = {'ENGINE': 'django.contrib.gis.db.backends.postgis', 'NAME':'gazdevtest'}
ELASTICSEARCH["default"]["INDEX"] = "gaz-test-index"

#createdb gazdevtest
#psql -d gazdevtest
#psql> create extension postgis;
