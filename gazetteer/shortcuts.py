from place import Place
from pyelasticsearch.exceptions import ElasticHttpNotFoundError
from django.http import Http404

def get_place_or_404(id):
    '''
        This function was used to send a custom exception for 404s, but since ElasticSearch is propagating the error directly to the middleware, that is no longer needed. See if this function can be removed.
    '''
    return Place.objects.get(id)
