from django.contrib.gis import admin
from models import *
# from forms import BaseRelationsFormSet
from django import forms
#from django.contrib.admin import SimpleListFilter
from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField


'''
class FeatureTypeFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Feature Type'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'feature_type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        fts = []
        for ft in FeatureType.objects.all():
            if ft.feature_set.count() > 0:
                t = (ft.id, ft.__unicode__(),)
                fts.append(t)
        
        return fts

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        val = self.value()
        return queryset.filter(feature_type=val)        
'''

class authRecordForm(forms.ModelForm):
    uri = forms.CharField(label="URI", required=True, widget=forms.TextInput(attrs={'size': '50'}))

    class Meta:
        model = AuthorityRecord  

class featuresForm(forms.ModelForm):
    url = forms.CharField(label='URI',
                              required=True,
                              widget=forms.TextInput(attrs={'size': '50'}))
    authority_record = AutoCompleteSelectField('authority_record', required=False)
    time_frame = AutoCompleteSelectField('time_frame', required=False)
    feature_type = AutoCompleteSelectField('feature_type', required=False)

#  exclude = ('info',)

    class Meta:
        model = Feature

class relationsForm(forms.ModelForm):
    feature1 = AutoCompleteSelectField('feature', required=True)
    feature2 = AutoCompleteSelectField('feature', required=True)

    class Meta:
        model = Relationship

class AuthorityRecordAdmin(admin.ModelAdmin):
    form = authRecordForm
    list_display = ('__unicode__', 'uri',)
    search_fields = ['preferred_name']

class RelationshipAdmin(admin.ModelAdmin):
#    form = relationsForm
    readonly_fields = ['feature1', 'feature2']

class FeatureNamesInline(admin.TabularInline):
    model = Name
    extra = 0

'''
class FeatureRelationInline(admin.TabularInline):
    model = Feature.relationships.through
    extra = 1
    fk_name = 'feature1'
    formset = BaseRelationsFormSet
'''


class FeatureAdmin(admin.OSMGeoAdmin):
    fields = ('preferred_name', 'feature_type', 'admin1', 'admin2', 'geometry', 'url', 'authority_record', 'time_frame', 'is_primary',)
    search_fields = ['preferred_name']
#    list_filter = ('feature_type',)
    inlines = [FeatureNamesInline]
    list_display = ('__unicode__', 'feature_type_name', 'admin1', 'admin2', 'time_start', 'time_end',)
    list_per_page = 30
#    list_filter = (FeatureTypeFilter,)
    openlayers_url = 'http://openlayers.org/dev/OpenLayers.js'
    openlayers_img_path = None
    form = featuresForm
#    readonly_fields = ['geometry']
#    map_template = 'gis/admin/osm.html'
#    default_lon = 72.855211097628413
#    default_lat = 19.415775291486027
#    default_zoom = 4
#    extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js', 'http://openlayers.org/dev/OpenLayers.js']

class FeatureTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description', 'feature_class',)

class TimeFrameAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', 'end_date', 'start_granularity', 'end_granularity',)

admin.site.register(Feature, FeatureAdmin)
admin.site.register(TimeFrame, TimeFrameAdmin)
admin.site.register(FeatureType, FeatureTypeAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(AuthorityRecord, AuthorityRecordAdmin)
