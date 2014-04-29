from django.conf.urls.defaults import *
from os.path import join
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^gazetteer/', include('gazetteer.foo.urls')),
    (r'^$', 'places.views.search'),
    ('^search/?$', 'places.views.search'),
    ('^feature/search.json$', 'places.views.search_json'),
    ('^feature/(?P<id>\d+).json$', 'places.views.feature_json'),
    ('^feature/(?P<id>\d+)/similar.json$', 'places.views.search_related_json'),
    ('^feature/(?P<id>\d+)/', 'places.views.feature_detail'),
    ('^auth_record.json$', 'places.views.auth_record_json'),
    ('^time_frame.json$', 'places.views.time_frame_json'),
    ('^add_relation$', 'places.views.add_relation'),
    # Uncomment the admin/doc line below to enable admin documentation:
#    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^ajax_select/', include('ajax_select.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

)

#if settings.LOCAL_DEVELOPMENT:
##
#  urlpatterns += patterns('',
##
#  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': join(settings.PROJECT_ROOT, "static")}),
##
#)

