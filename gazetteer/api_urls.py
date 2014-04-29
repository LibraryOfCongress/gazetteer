from django.conf.urls import patterns, include, url

urlpatterns = patterns('gazetteer.api_views',
    url(r'^feature_codes.json', 'feature_codes_autocomplete', name='feature_codes_json'),
    url(r'^search.json$', 'search', name='search_json'),
    url(r'^(?P<id>[0-9a-f]{16})/similar.json$', 'similar', name='similar_json'),    
    url(r'^(?P<id>[0-9a-f]{16})/hierarchy.json$', 'hierarchy', name='hierarchy_json'),
    url(r'^(?P<id>[0-9a-f]{16})/history.json$', 'history', name='history_json'),
    url(r'^(?P<id>[0-9a-f]{16})/(?P<revision>[0-9a-f]{40}).json$', 'revision', name='revision_json'),
    url(r'^(?P<id>[0-9a-f]{16})/relations.json$', 'relations', name='relations_json'),
#    url(r'^(?P<id>[0-9a-f]{16})/add_relation.json$', 'add_relation', name='add_relation'),
    url(r'^(?P<id1>[0-9a-f]{16})/(?P<relation_type>[a-z].*?)/(?P<id2>[0-9a-f]{16}).json$', 'add_delete_relation', name='add_relation'),         
    url(r'^(?P<id>[0-9a-f]{16}).json$', 'place_json', name='place_json'),
 
)
