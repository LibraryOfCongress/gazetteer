from django.db import connection
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
try:
    import json
except:
    import simplejson as json


class AuthorityRecord(models.Model):
    uri = models.CharField(max_length=512)
    preferred_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['preferred_name']

    def __unicode__(self):
        return self.preferred_name

class FeatureSearchManager(models.GeoManager):
    def set_threshold(self, threshold):
        """Set the limit for trigram similarity matching."""
        cursor = connection.cursor()
        cursor.execute("""SELECT set_limit(%f)""" % threshold)

    def find(self, bbox=None, text=None, adm1=None, adm2=None, is_primary=True, threshold=0.5, srid=4326):
        qset = self.get_query_set().filter(is_primary=is_primary)
        if bbox:
            (minx, miny, maxx, maxy) = bbox
            bbox = Polygon(((minx,miny),(minx,maxy),(maxx,maxy),(maxx,miny),(minx,miny)),srid=srid)
            if srid != 4326: bbox.transform(4326) # convert to lon/lat
            qset = qset.filter(geometry__bboverlaps=bbox)
        if text:
            self.set_threshold(threshold)
            # use the pg_trgm index
            qset = qset.extra(select={"similarity":"similarity(preferred_name, %s)"},
                              select_params=[text],
                              where=["preferred_name %% %s"],
                              params=[text],
                              order_by=["-similarity"])
        if adm1: qset = qset.filter(admin1__exact=adm1)
        if adm2: qset = qset.filter(admin2__exact=adm2)
        return qset

class Feature(models.Model):
    authority_record = models.ForeignKey(AuthorityRecord, null=True, blank=True)
    url = models.CharField(max_length=512, unique=True, verbose_name="URI")
    preferred_name = models.CharField(max_length=512)
    feature_type = models.ForeignKey("FeatureType", null=True, blank=True)
    admin1 = models.CharField(max_length=2, blank=True, verbose_name="State", db_index=True)
    admin2 = models.CharField(max_length=255, blank=True, verbose_name="County", db_index=True)
    geometry = models.GeometryField()
    is_primary = models.BooleanField(default=True)
    time_frame = models.ForeignKey("TimeFrame", null=True, blank=True)
    relationships = models.ManyToManyField("Feature", through='Relationship', blank=True)
    objects = models.GeoManager()
    search = FeatureSearchManager()

    class Meta:
        ordering = ['preferred_name']

    def __unicode__(self):
        return self.preferred_name

    def feature_type_name(self):
        return self.feature_type.name.title()
    feature_type_name.short_description = "Feature Type"

    def get_geojson(self, srid=4326):
        geom = json.loads(self.geometry.transform(srid, True).geojson)

        if self.feature_type is None:
            feature_type = ''
        else:
            feature_type = self.feature_type.name

        properties = {
            'id': self.id,
            'uri': self.url,
            'preferred_name': self.preferred_name,
            'feature_type': feature_type,
            'admin1': self.admin1,
            'admin2': self.admin2
        }
        return {
            'type': 'Feature',
            'properties': properties,
            'geometry': geom
        }        

    def time_start(self):
        tf = self.time_frame
        if tf is not None:
            return str(tf.start_date)
        else:
            return '' 
    time_start.short_description = "Start Date"

    def time_end(self):
        tf = self.time_frame
        if tf is not None:
            return str(tf.end_sate)
        else:
            return ''
    time_end.short_description = "End Date"

    def similar_features(self, max_distance=30000, scale_factor=2000, threshold=0.35, limit=20):
	type(self).search.set_threshold(threshold)
        sql = """
            SELECT DISTINCT *, %s * similarity / (distance + 1.0) AS score FROM (
                SELECT f.*, r.feature1_id, r.feature2_id, r.relationship_type,
                       similarity(preferred_name, %s) AS similarity,
                       st_distance_sphere(geometry, %s) AS distance
                       FROM places_feature f, places_relationship r
		       WHERE (r.feature1_id = %s AND r.feature2_id = f.id)
                       OR    (r.feature2_id = %s AND r.feature1_id = f.id)
                UNION
                SELECT f.*, r.feature1_id, r.feature2_id, r.relationship_type,
                       similarity(preferred_name, %s) AS similarity,
                       st_distance_sphere(geometry, %s) AS distance
                       FROM places_feature f LEFT JOIN places_relationship r
                       ON (f.id = r.feature1_id or f.id = r.feature2_id)
                       WHERE geometry && st_buffer(%s, %s)
                       AND preferred_name %% %s
                       AND f.id <> %s
                       AND (r.feature1_id IS NULL or r.feature1_id = %s or r.feature2_id = %s)
                       LIMIT %s
                ) AS whatever
                ORDER BY %s * similarity / (distance + 1.0) DESC"""
	qset = type(self).objects.raw(sql, [scale_factor,
                        self.preferred_name, "SRID=4326;" + self.geometry.centroid.wkt,
                        self.id, self.id,
                        self.preferred_name, "SRID=4326;" + self.geometry.centroid.wkt,
			self.geometry.centroid.wkt, max_distance*0.00001,
			self.preferred_name, self.id, self.id, self.id, limit, scale_factor])
	return qset

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('un', 'Unknown'),
    ('xx', '(code)'),
)

NAME_TYPE_CHOICES = (
    ('alternate', 'alternate'),
    ('abbreviation', 'abbreviation'),
    ('colloquial', 'colloquial'),
    ('historic', 'historic'),
    ('official', 'official'),
    ('icao', 'ICAO code'),
    ('iata', 'IATA code'),
    ('postcode', 'ZIP code'),

)

class Name(models.Model):
    feature = models.ForeignKey(Feature)
    text = models.CharField(max_length=512)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    name_type = models.CharField(max_length=64, choices=NAME_TYPE_CHOICES)

    def __unicode__(self):
        return self.text

GRANULARITY_CHOICES = (
    ('day', 'day'),
    ('month', 'month'),
    ('year', 'year'),
    ('decade', 'decade'),
    ('century', 'century'),
)

class TimeFrame(models.Model):
    description = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField() #add default to now
    start_granularity = models.CharField(max_length=64, choices=GRANULARITY_CHOICES)
    end_granularity = models.CharField(max_length=64, choices=GRANULARITY_CHOICES)

    class Meta:
        ordering = ['description']

    def __unicode__(self):
        return self.description


class FeatureType(models.Model):
    feature_class = models.CharField(max_length=1)
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField()

    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return self.code + ": " + self.name


RELATIONSHIP_CHOICES = (
    ('conflates', 'conflates'),
    ('contains', 'contains'),
    ('replaces', 'replaces'),
    ('supplants', 'supplants'),
)

class Relationship(models.Model):
    feature1 = models.ForeignKey(Feature, related_name="feature_from")
    feature2 = models.ForeignKey(Feature, related_name="feature_to")
    relationship_type = models.CharField(max_length=64, choices=RELATIONSHIP_CHOICES)

    def __unicode__(self):
        return "%s %s %s" % (self.feature1.preferred_name, self.relationship_type, self.feature2.preferred_name,)

    class Meta:
        verbose_name = "Relation"
        verbose_name_plural = "Relations"

'''
class Place(models.Model):
    url = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    fcode = models.ForeignKey("FeatureCode")
    country = models.CharField(max_length=2)
    admin1 = models.CharField(max_length=2)
    point = models.PointField()

    def __unicode__(self):
        return self.name


class FeatureCode(models.Model):
    fcode = models.CharField(max_length=10, primary_key=True, unique=True)
    letter = models.CharField(max_length=2)
    short_name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.fcode + ": " + self.short_name
'''    
    

