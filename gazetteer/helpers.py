from instance_settings import *
import settings
from models import Origin, FeatureCode
from place import Place

def get_settings():
    return {
        'debug': settings.DEBUG,
        'api_base': API_BASE,
        'app_base': APP_BASE,
        'osmUrl': OSM_URL,
        'osmAttrib': OSM_ATTRIBUTION,
        'centerLat': CENTER_LAT,
        'centerLon': CENTER_LON,
        'defaultZoom': DEFAULT_ZOOM,
        'smoothFactor': SMOOTH_FACTOR,
        'warperURLs': WARPER_URLS,
        'minYear': MIN_YEAR,
        'maxYear': MAX_YEAR,
        'origins': [origin.to_json() for origin in Origin.objects.all()],
        'featureCodes': get_feature_codes()
    }


def get_feature_codes():
    top_feature_codes = Place.objects.feature_code_counts(10)
    codes = [code['term'] for code in top_feature_codes]
    return [fcode.to_json() for fcode in FeatureCode.objects.filter(typ__in=codes)]    
