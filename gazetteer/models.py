from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

import csv

class AdminBoundary(models.Model):
    uuid = models.CharField(max_length=24, blank=False, unique=True)
    name = models.CharField(max_length=256)
    alternate_names = models.TextField()
    feature_code = models.CharField(max_length=8)
    uri = models.CharField(max_length=256)
    geom = models.MultiPolygonField(blank=True, null=True)
    queryable_geom = models.MultiPolygonField(blank=True, null=True)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "<%s %s, %s, %s>" % (self.__class__, self.uuid, self.name, self.feature_code) 
    
    def to_place_json(self):
        return {"id" : str(self.uuid), "feature_code" : self.feature_code,
                     "name" : self.name, "alternate_names": self.alternate_names}

class FeatureCode(models.Model):
    cls = models.CharField(max_length=3, blank=True)
    typ = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.typ

    def to_json(self):
        return {
            'id': self.typ,
            'cls': self.cls,
            'typ': self.typ,
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def import_from_csv(kls, path):
        csvfile = csv.reader(open(path), delimiter="\t")
        for row in csvfile:
            cls, typ = row[0].split(".")
            fcode = kls(cls=cls, typ=typ, name=row[1], description=row[2])
            fcode.save()
            print "saved " + row[1]

#an Origin represents a URI source, with a name etc
#example - an example URI from a place
#code - the code to use in the query string (uris:*loc.gov*)
#TO load in the data from fixtures: python manage.py loaddata origins_nypl.json
class Origin(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    example = models.CharField(max_length=128, blank=True)
    code = models.CharField(max_length=128, unique=True)
    
    def __unicode__(self):
        return "%s %s, %s" % (self.__class__, self.name, self.code) 
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'example' : self.example,
            'code' : self.code
        }

#admin model to handle upload of a CSV file for import
class BatchImport(models.Model):
    name = models.CharField(max_length=64, blank=False)
    user = models.ForeignKey(User)
    start_import = models.BooleanField(default=False)
    imported_at = models.DateField(blank=True, null=True)
    record_count = models.BigIntegerField(blank=True, null=True)
    batch_file = models.FileField(null=True, blank=True, upload_to=settings.BATCH_UPLOAD_FILE_PATH)
    core_fields = ["ID", "WKT", "NAME", "FEATURE_CODE", "URIS", "ALTERNATE", "START", "END", "START_RANGE", "END_RANGE"]
    optional_fields = ["NUMBER", "STREET", "CITY", "STATE", "POSTCODE"]

    def __unicode__(self):
        return "%s %s, %s, %s" % (self.__class__, self.name, self.user, self.batch_file )

    def save(self):
        if self.start_import == True and not self.imported_at:
            self.parseFile()
        return super(BatchImport, self).save()

    def clean(self):
        if self.batch_file and self.batch_file.file:
            csvfile = csv.DictReader(self.batch_file.file, delimiter="\t")
            row = csvfile.next()
            for field in self.core_fields:
                if field not in row.keys():
                    raise ValidationError('CSV File does not have the necessary field: '+ field)

            uris = []
            for row in csvfile:
                fcode = row.get("FEATURE_CODE")
                if not fcode:
                    raise ValidationError("A Feature code is missing")
                uri = row.get("URIS").split("|")[0]
                if not uri:
                    raise ValidationError('CSV file is missing a uri')
                if uri in uris:
                    raise ValidationError('duplicate URI detected')
            uris.append(uri)
            
    
    def parseFile(self):
        import hashlib, datetime
        from gazetteer.place import Place
        from shapely import wkt
        from shapely.geometry import mapping
        
        place_defaults = {
            "updated":datetime.datetime.utcnow().replace(second=0, microsecond=0).isoformat(),
            "is_primary": True,
            "relationships": [],
            "admin":[] 
            }
            
        CsvFile = csv.DictReader(self.batch_file.file, delimiter="\t")
        count = 0
        for row in CsvFile:
            
            name = row.get("NAME")
            if not name:
                continue

            count = count + 1
            
            if row.get("WKT"):
                shapelygeom =  wkt.loads(row.get("WKT"))
                centroid = [shapelygeom.centroid.x , shapelygeom.centroid.y]
                geometry = mapping(shapelygeom)
            else:
                centroid = []
                geometry = {}
                
            alternates = []
            if row.get("ALTERNATE"):
                alt_list = row.get("ALTERNATE").split("|")
                for alt_name in alt_list:
                    alternates.append({"name": alt_name, "lang": "en"})
                
            uris = row.get("URIS").split("|")

            action = ""
            if row.get("ID"):
                place_id = row.get("ID")
                action = "updated"
            else:
                place_id = hashlib.md5(uris[0]).hexdigest()[:16]
                action = "added"
                  
            timeframe = {}
            if row.get("START") or row.get("END"):
                timeframe = {"start": row.get("START"), "end": row.get("END"), "start_range": row.get("START_RANGE"), "end_range": row.get("END_RANGE") }

            place_dict = {
                "id": place_id, 
                "name":  name,
                "feature_code": row.get("FEATURE_CODE"),
                "timeframe": timeframe, 
                "geometry":geometry,
                "centroid": centroid,
                "alternate": alternates,
                "uris": uris 
                }

            add_optional = False
            for field in self.optional_fields:
                if row.get(field):
                    add_optional = True
            if add_optional:
                optional = {"address":{"number":row.get("NUMBER"), "street":row.get("STREET"), "city":row.get("CITY"), "state":row.get("STATE"), "postcode": row.get("POSTCODE")}}
                place_dict.update(optional)
                
            place_dict.update(place_defaults)
            
            place = Place(place_dict)
            metadata = {
                'user': self.user.username,
                'user_id': str(self.user.id),
                'comment': "Place "+ action +" via batch import id:" + str(self.id)
            }
            
            place.save(metadata=metadata)
            if settings.DEBUG:
                print "BatchImport: place " + action, place.id

        if settings.DEBUG:
                print "BatchImport done: count: " + str(count)
        self.record_count = count
        self.imported_at = datetime.datetime.utcnow()
        
     

        
