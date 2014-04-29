from ox.django.shortcuts import render_to_json_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.conf import settings
#from django.http import HttpResponse
from place import Place
from pyelasticsearch.exceptions import ElasticHttpNotFoundError
try:
    import json
except:
    import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
import datetime
import math
from models import FeatureCode
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import OGRException
from shortcuts import get_place_or_404
import re


@csrf_exempt 
def new_place_json(request):
    ''' Takes a GeoJSON string as POST data and saves it as a new place
         saves and returns back geojson for the place
    '''
        
    if not request.method == 'POST':
        return render_to_json_response({'error': 'Method Not Allowed'}, status=405)
        
    geojson = json.loads(request.body)
    if geojson.has_key("comment"):
        comment = geojson.pop("comment")
    else:
        comment = ''
    json_obj = geojson.pop("properties")
    json_obj['geometry'] = geojson['geometry']
    json_obj['centroid'] = []
    if geojson["geometry"]:
        centroid = GEOSGeometry(json.dumps(json_obj['geometry'])).centroid
        json_obj['centroid'] = list(centroid.coords)      
        
    p = Place(json_obj)
    
    import random, hashlib
    p.id = hashlib.md5(p.name + str(random.random())).hexdigest()[:16]        
    p.relationships = []

    if settings.GAZETTEER["url"]:
        uri = settings.GAZETTEER["url"] + "/gazetteer/feature/"+ p.id
    else:
        uri = "http://gazetteer.in/feature/"+p.id
    p.uris.append(uri)
    
    user_id = request.user.id
    username = request.user.username
    
    metadata = {
        'user': username,
        'user_id': user_id,
        'comment': comment
    }
    
    p.save(metadata=metadata)
    new_place = p.copy() #returns a copy of the newly saved place
    return render_to_json_response(new_place.to_geojson())
        
        
     
@csrf_exempt
def place_json(request, id):

    place = get_place_or_404(id)
              
    if request.method == 'GET':
        '''
            Return GeoJSON for Place
        '''
        geo_json = place.to_geojson()
        return render_to_json_response(geo_json)
    
    elif request.method == 'PUT':
        '''
            Takes a GeoJSON string as PUT data and saves Place
            Saves and returns  back GeoJSON for place.
        '''
        #FIXME: check permissions
#        if not request.user.is_staff():
#            return render_to_json_response({'error': 'You do not have permissions to edit this place.'}, status=403) 
        geojson = json.loads(request.body)
        if geojson.has_key("comment"):
            comment = geojson.pop("comment")
        else:
            comment = ''
        json_obj = geojson.pop("properties")
        json_obj['geometry'] = geojson['geometry']

        #handle getting centroid:
        if json_obj['geometry']:
            centroid = GEOSGeometry(json.dumps(json_obj['geometry'])).centroid
            json_obj['centroid'] = list(centroid.coords)
        else:
            json_obj['centroid'] = []
            json_obj['geometry'] = {}
       
        #updates place but doesn't save it
        place.update(json_obj)
        
        user_id = request.user.id
        username = request.user.username
        metadata = { 
            'user': username,
            'user_id': user_id,
            'comment': comment
        }

        place.save(metadata=metadata)
        new_place = place.copy()#returns a copy of the newly saved place
        
        return render_to_json_response(new_place.to_geojson())
        

    elif request.method == 'DELETE':
        return render_to_json_response({'error': 'Not implemented'}, status=501)

    else:
        return render_to_json_response({'error': 'Method Not Allowed'}, status=405)


def search(request):
    '''
        Takes GET params:
            q: search string
            bbox: bounding box string
                - if "false", will search for places without geos
                - if empty string / not specified, will search for places with and without geos, not constrained by bbox
            per_page: results per page int, default=100
            page: page no (starting with 1) int, default=1

        Returns:
            GeoJSON feed of search results
            Extra properties of feed:
                total: total number of results
                max_score: max score in results (?)
                page: page number
    '''
    query = request.GET.get("q", "")
    if query == "":
        query = '*'
    #FIXME: remove feature_type from API as feature type queries are handled by query-string
    feature_type = request.GET.get("feature_type", None)
    if feature_type:
        if FeatureCode.objects.filter(typ=feature_type).count() > 0:
            query += ' feature_code:%s' % feature_type.upper()
    per_page = int(request.GET.get("per_page", 100)) #FIXME: add error handling if int conversion fails
    page = int(request.GET.get("page", 1))
    page_0 = page - 1 #model method requires page number to be zero-based whereas API accepts 1-based.
    bbox_string = request.GET.get("bbox", "")
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)
    
    year_regex = re.compile(r'^[0-9]{4}')
    if start_date and year_regex.match(start_date):
        start_date += "-01-01"
    if end_date and year_regex.match(end_date):
        end_date += "-12-31"

    sort = request.GET.get("sort", None)
    VALID_SORTS = ['relevance', 'feature_code', 'start', 'end', 'name', 'uris', 'distance']
    if sort and sort not in VALID_SORTS:
        sort = None #Should we throw an error here?
    order = request.GET.get("order", None)
    if order and order not in ['asc', 'desc']:
        order = None    
            
    if bbox_string and bbox_string != "false":
        bbox = [float(b) for b in bbox_string.split(",")]
    elif bbox_string == 'false':
        bbox = False
    else:
        bbox = None
    result = Place.objects.search(query, bbox=bbox, start_date=start_date, end_date=end_date, per_page=per_page, page=page_0, sort=sort, order=order)
    total = result['total']
    pages = int(math.ceil(total / (per_page + .0))) #get total number of pages

    simplify = request.GET.get("simplify", False)
    if simplify and total >= 1:
        if bbox:
            degrees = bbox[2] - bbox[0]
            map_width = 700 #(roughly)
            tolerance = (degrees / map_width) / 2
        else:
            tolerance = 0.01
        
        for place in result["places"]:
            if place.geometry and (place.geometry["type"] == "Polygon" or place.geometry["type"] == "MultiPolygon"):
                coords = [item for sublist in place.geometry["coordinates"] for item in sublist]
                if len(coords) > 200:  #only simplify the larger polygons. TODO - determine best number for this
                    try:
                        geos_geom = GEOSGeometry(json.dumps(place.geometry))
                        if geos_geom.valid:
                            simplified_geom = geos_geom.simplify(tolerance, preserve_topology=True)
                            place.geometry = json.loads(simplified_geom.json)
                        else:
                            #invalid geometry so we will nullify it - we could try to fix this though
                            place.geometry = {}
                    except OGRException:
                        place.geometry = {}

    format = request.GET.get("format", "geojson")
    if format == "csv":
        from django.http import HttpResponse
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="gazetteer_results.csv"'
        dictwriter = csv.DictWriter(response, delimiter='\t', fieldnames=Place.CSV_FIELDNAMES)
        dictwriter.writer.writerow(dictwriter.fieldnames)
        for p in result['places']:
            dictwriter.writerow(p.to_csv_dict())
        return response


    ret = {
        'type': 'FeatureCollection',
        'features': [p.to_geojson() for p in result['places']],
        'total': total,
        'page': result['page'],
        'pages': pages,
        'per_page': result['per_page'],
        'max_score': result['max_score']
    }
    return render_to_json_response(ret)


def similar(request, id):
    '''
        Takes place ID
        Returns GeoJSON feed of similar places.
            Extra properties of feed:
                total: total number of similar places
                max_score: max score of similarity (?)
    '''
    try:
        place = Place.objects.get(id)
    except ElasticHttpNotFoundError:
        return render_to_json_response({'error': 'Place not found'}, status=404)          

    if request.method == 'GET':
        similar_places = place.find_similar()
        geojson = {
            'type': 'FeatureCollection',
            'total': similar_places['total'],
            'max_score': similar_places['max_score'],
            'features': [p.to_geojson() for p in similar_places['places']]
        }
        return render_to_json_response(geojson)
        #return render_to_json_response({'error': 'Not implemented'}, status=501)

    else:
        return render_to_json_response({'error': 'Method Not Allowed'}, status=405)


def hierarchy(request, id):
    try:
        place = Place.objects.get(id)
    except ElasticHttpNotFoundError:
        return render_to_json_response({'error': 'Place not found'}, status=404)

    if request.method == 'GET':
        #hierarchy_json = place.get_hierarchy()        
        #return render_to_json_response(hierarchy_json)
        return render_to_json_response({'error': 'Not implemented'}, status=501)

    else:
        return render_to_json_response({'error': 'Method Not Allowed'}, status=405)


def history(request, id):
    '''
        Returns array of revision objects for Place
    '''
    try:
        place = Place.objects.get(id)
    except ElasticHttpNotFoundError:
        return render_to_json_response({'error': 'Place not found'}, status=404)

    if request.method == 'GET':
        history_json = Place.objects.history(place)
        #history_json = place.get_history()        
        return render_to_json_response(history_json)
        #return render_to_json_response({'error': 'Not implemented'}, status=501)

    else:
        return render_to_json_response({'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def revision(request, id, revision):
    '''
        Get GeoJSON of a place at given revision
    '''
    place = get_place_or_404(id)

    if request.method == 'GET':
        revision = Place.objects.revision(place,revision)
        geojson = revision['place'].to_geojson()
        geojson['version'] = revision['version']
        geojson['digest'] = revision['digest']
        return render_to_json_response(geojson)


    elif request.method == 'PUT':
        user_id = request.user.id
        username = request.user.username
        data = json.loads(request.body)
        comment = data.get('comment', '')
        metadata = {
            'user': username,
            'user_id': user_id,
            'comment': comment
        }       
        place = place.rollback(revision, metadata=metadata) #FIXME: handle invalid revision ids
        return render_to_json_response(place.to_geojson())

    else:
        return render_to_json_response({'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def relations(request, id):
    '''
        Returns GeoJSON feed for related places. Adds a property 'relation_type' to geojson properties to indicate type of relations
    '''

    place = get_place_or_404(id)

    features = []
    if place.relationships:
        for obj in place.relationships:
            geojson = Place.objects.get(obj['id']).to_geojson()
            geojson['properties']['relation_type'] = obj['type']
            features.append(geojson)

    relations_geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
   
    return render_to_json_response(relations_geojson)

@csrf_exempt
def add_delete_relation(request, id1, relation_type, id2):
    place1 = get_place_or_404(id1)
    place2 = get_place_or_404(id2)
    if relation_type not in Place.RELATION_CHOICES.keys():
        return render_to_json_response({'error': 'Invalid relation type'}, status=404)

  
    user_id = request.user.id
    username = request.user.username
    comment = json.loads(request.body).get("comment", "")

    metadata = {
        'user': username,
        'user_id': user_id,
        'comment': comment
    }

    if request.method == 'PUT':
        place1.add_relation(place2, relation_type, metadata)
    if request.method == 'DELETE':
        place1.delete_relation(place2, metadata)

    return relations(request, place1.id)


#@csrf_exempt
#def add_relation(request, id):
#    '''
#    Add relation for a place with id, takes JSON in a PUT request
#        target_id: <string> id of place being related to
#        relation_type: <string> type of relation
#        metadata:
#            user: <string> username
#            comment: <string> comment about change
#    '''

#    place = get_place_or_404(id)
#    if request.method == 'PUT':
#        #FIXME: check permissions
#        data = json.loads(request.body)
#        #FIXME: handle validation / sending back errors
#        place.add_relation(data['target_id'], data['relation_type'], data['metadata'])
#        return render_to_json_response(place.to_geojson())
#    else:
#        return render_to_json_response({'error': 'Method Not Allowed'}, status=405)



def feature_codes_autocomplete(request):
    '''
        Used for autocomplete: return Feature Codes matching GET param 'q'
    '''
    query = request.GET.get("q", "a")
    page_limit = int(request.GET.get("page_limit", 10))
    page = int(request.GET.get("page", 1))
    matched_codes = FeatureCode.objects.filter(Q(cls__icontains=query) | Q(typ__icontains=query) | Q(name__icontains=query) | Q(description__icontains=query))       
    paginator = Paginator(matched_codes, page_limit)
    results = paginator.page(page)
    items = [obj.to_json() for obj in results.object_list]  
    return render_to_json_response({
        'items': items,
        'has_next': results.has_next()
    })    


