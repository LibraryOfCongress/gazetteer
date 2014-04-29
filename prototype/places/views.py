# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from ox.django.shortcuts import render_to_json_response, get_object_or_404_json
from django.template import RequestContext
from models import Feature, FeatureType, AuthorityRecord, Relationship
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
try:
    import json
except:
    import simplejson as json

def search(request):
    d = RequestContext(request, {})
    return render_to_response("search.html", d)

def feature_detail(request, id):
    feature = get_object_or_404(Feature, pk=id)
    geojson = json.dumps(feature.get_geojson())
    d = RequestContext(request, {
        'feature': feature,
        'geojson': geojson
    })
    return render_to_response("feature.html", d)      

def search_json(request):
    search_term = request.GET.get("q", "")
    threshold = request.GET.get("threshold", '0.5')
    bbox = request.GET.get("bbox", False)
    page = int(request.GET.get("page", '1'))
    count = int(request.GET.get("count", '100'))
    country = request.GET.get("cc", "US") # right now, unused
    adm1 = request.GET.get("adm1", "")
    adm2 = request.GET.get("adm2", "")
    srid = int(request.GET.get("srid", 4326))

    if threshold:
        try:
            threshold = max(float(threshold), 0.1)
        except ValueError:
            return render_to_json_response({'error': 'threshold must be a float'})

    if bbox:
        try:
            bbox = map(float, bbox.split(","))
        except ValueError:
            bbox = None
            return render_to_json_response({'error': 'bbox must be in the form: minx,miny,maxx,maxy'})

    if not bbox and not search_term:
        return render_to_json_response({'error': 'must supply either a valid `bbox` or a `search` parameter'})

    features_qset = Feature.search.find(bbox=bbox, text=search_term, threshold=threshold, adm1=adm1, adm2=adm2, srid=srid)
    total_results = features_qset.count()
    paginator = Paginator(features_qset, count)
    num_pages = paginator.num_pages

    try:
        results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        results = paginator.page(paginator.num_pages)
    features = [f.get_geojson(srid) for f in results.object_list]

    d = {
        'type': 'FeatureCollection',
        'results': total_results,
        'current_page': page,
        'pages': num_pages,
        'features': features
    }
    return render_to_json_response(d)

def feature_json(request, id):
    id = str(id)
    srid = int(request.GET.get("srid",4326))
    feature = get_object_or_404_json(Feature, pk=id)
    return render_to_json_response(feature.get_geojson(srid))

def search_related_json(request, id):
#    id = request.GET.get("id", "0")
    id = str(id)
    feature = get_object_or_404_json(Feature, pk=id)
    similar_features = feature.similar_features()
    d = []

    for s in similar_features:
        time_frame = relates_to = related_by = ""
        if s.time_frame is not None:
            time_frame = s.time_frame.description
        if s.relationship_type is not None:
            if s.feature2_id == s.id:
               relates_to = s.relationship_type
            elif s.feature1_id == s.id:
               related_by = s.relationship_type
        d.append({
            'id': s.id,
            'feature_type': s.feature_type.name, #FeatureType.objects.get(pk=s.feature_type_id).name,
            'preferred_name': s.preferred_name,
            'similarity': s.similarity,
            'distance': s.distance,
            'time_frame': time_frame,
            'is_primary': s.is_primary,
            'relates_to': relates_to,
            'related_by': related_by
        })    
    return render_to_json_response(d)

def auth_record_json(request):
    id = request.GET.get("id", "0")
    auth_record = get_object_or_404_json(AuthorityRecord, pk=id)
    features = [f.get_geojson() for f in auth_record.feature_set.all()]
    d = {
        'type': 'FeatureCollection',
        'features': features
    }
    return render_to_json_response(d)
    
def time_frame_json(request):
    id = request.GET.get("id", "0")
    time_frame = get_object_or_404_json(AuthorityRecord, pk=id)
    features = [f.get_geojson() for f in time_frame.feature_set.all()]
    d = {
        'type': 'FeatureCollection',
        'features': features
    }
    return render_to_json_response(d)   

def add_relation(request):
    feature1 = request.GET.get("feature1", None)
    feature2 = request.GET.get("feature2", None)
    relation = request.GET.get("relation", None)
    if feature1 == None or feature2 == None or relation == None:
        return render_to_json_response({'error': 'bad request'})

    if not request.user.is_staff:
        return render_to_json_response({'error': 'insufficient permissions error. try logging in again? are you staff / admin?'})

    feature1 = get_object_or_404_json(Feature, pk=feature1)
    feature2 = get_object_or_404_json(Feature, pk=feature2)
    verb = rel_obj = None
    try:
        rel_obj = Relationship.objects.get(feature1=feature1, feature2=feature2)
        verb = "deleted"
    except ObjectDoesNotExist:
        rel_obj = Relationship(feature1=feature1, feature2=feature2, relationship_type=relation)
        verb = "created"
    if relation == "":
        if verb == "deleted":
            rel_obj.delete()
            if relation == "conflates":
                feature2.is_primary = True
                feature2.save()
        else:
             return render_to_json_response({'error': 'relation is already deleted'})
    else:
        rel_obj.save()
        if relation == "conflates":
            feature2.is_primary = False
            feature2.save()
    return render_to_json_response({'success': 'relation %s successfully.' % verb})
