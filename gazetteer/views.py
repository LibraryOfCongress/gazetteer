from django.template import RequestContext, Context, loader
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate
from ox.django.shortcuts import render_to_json_response
import json
import re
from os.path import join
from place import *
import api_views
import datetime
import isodate
import settings
import instance_settings
from gazetteer.shortcuts import get_place_or_404
from django.views.decorators.csrf import csrf_exempt
from helpers import get_settings

def index(request):
    places_count = Place.objects.count("*")
    context = RequestContext(request, {
        'total_count': places_count
    })
    return render_to_response("index.html", context)

def backbone(request):
    instance_name = instance_settings.SHORT_NAME
    instance_templates_base = join('instance_templates', instance_name)
    footer_template = join(instance_templates_base, 'footer.html')
    try:
        footer_content = render_to_string(footer_template)
    except:
        footer_content = ''
    context = {
        'site_title': instance_settings.SITE_TITLE,
        'app_base': instance_settings.APP_BASE,
        'footer': footer_content,
        'debug': settings.DEBUG
    }
    return render(request, "backbone.html", context)

#FIXME: move to models
GRANULARITY_CHOICES = (
    ("0", 'None'),
    ("1", 'One Day'),
    ("7", 'One Week'),
    ("30", 'One Month'),
    ("365", 'One Year'),
    ("3650", 'One Decade'),
)


def detail(request, place_id):
    place = get_place_or_404(place_id)
    if place.updated:
        updated = isodate.isodates.parse_date(place.updated)
    else:
        updated = None
    geojson = json.dumps(place.to_geojson())

    similar_geojson = api_views.similar(request, place_id).content 

    similar_places = json.loads(similar_geojson)
    if place.feature_code:
        try:
            feature_code = FeatureCode.objects.get(typ=place.feature_code)
        except:
            feature_code = "Invalid"
    else:
        feature_code = "None"

    revisions_json = api_views.history(request, place_id).content
    revisions = json.loads(revisions_json)

    #FIXME: move get_wms_layers to a model method or so
    WARPER_URLS = ['http://maps.nypl.org']
    wms_layers = []
    for uri in place.uris:
        for warper_url in WARPER_URLS:
            if uri.startswith(warper_url):
                regex = re.compile(r'' + warper_url + '/warper/layers/([0-9]*)\..*$')
                if regex.match(uri):
                    warper_id = regex.findall(uri)[0]
                    wms_layer = warper_url + "/warper/layers/wms/" + warper_id
                    wms_layers.append(wms_layer)
            

    if place.relationships is not None:
        place.relationships = [{'type': obj['type'], 'place': Place.objects.get(obj['id'])} for obj in place.relationships]

    context = RequestContext(request, {
        'place': place,
        'updated': updated,
        'place_geojson': geojson,
        'feature_code': feature_code,
        'similar_places': similar_places,
        'similar_geojson': similar_geojson,
        'revisions': revisions,
        'revisions_json': revisions_json,
        'wms_layers': json.dumps(wms_layers),
        'GRANULARITY_CHOICES': GRANULARITY_CHOICES,
        'RELATION_CHOICES': Place.RELATION_CHOICES       
    })
    return render_to_response("detail.html", context)

@csrf_exempt
def login_json(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        user_json = {
            'id': user.id,
            'username': user.username
        }
        return render_to_json_response({'success': 'User logged in', 'user': user_json})
    return render_to_json_response({'error': 'Username / password do not match'})
    
@csrf_exempt
def logout_json(request):
    logout(request)
    return render_to_json_response({'success': 'User logged out'})    


def user_json(request):
    if request.user.is_authenticated():
        user_json = {
            'id': request.user.id,
            'username': request.user.username
        }
    else:
        user_json = {}   
    return render_to_json_response({'user': user_json, 'settings': get_settings()}) 

def edit_place(request, place_id):
    place = get_place_or_404(place_id)
    geojson = json.dumps(place.to_geojson())
    context = RequestContext(request, {
        'place': place,
        'place_geojson': geojson
    })
    return render_to_response("edit_place.html", context)  


def new(request):
    place_obj  =  {
                "relationships": [],"admin": [], "name": "", 
                "geometry": {}, "is_primary": True,
                "uris": [], "feature_code": "ADM1",
                "centroid": [], "timeframe": {}, "is_composite": False
                }
    place = Place(place_obj)
    geojson = json.dumps(place.to_geojson())
    context = RequestContext(request, {
        'place': place,
        'place_geojson': geojson
    })
    return render_to_response("new.html", context)  
    



