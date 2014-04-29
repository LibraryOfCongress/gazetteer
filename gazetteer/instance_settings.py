 # -*- coding: utf-8 -*-

SHORT_NAME = 'loc'
SITE_TITLE = 'Digital Gazetteer'
API_BASE = '/1.0/'
APP_BASE = '/'
OSM_URL = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
OSM_ATTRIBUTION = u'Map data © openstreetmap contributors'
CENTER_LAT = 0
CENTER_LON = 0
SMOOTH_FACTOR = 1
DEFAULT_ZOOM = 1
MIN_YEAR = 1700
MAX_YEAR = 2013 #FIXME: get current year? should this be done in the JS and skip setting?
WARPER_URLS = ['http://maps.nypl.org']


try:
    from local_instance_settings import *
except:
    pass
