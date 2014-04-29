#
# After conflate_admin_states this should be run
# Will create an adminbondary for each record
# WIll delete existing admin boundary records first!
# 

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon
from django.core.management import setup_environ
import settings
import itertools
setup_environ(settings)

from gazetteer.models import FeatureCode
from gazetteer.models import AdminBoundary
from django.db import connection, transaction
from gazetteer.place import *

es_settings = settings.ELASTICSEARCH["default"]
conn = ElasticHistory(es_settings["HOST"], timeout=120)
index = es_settings["INDEX"]
doc_type = es_settings["DOC_TYPE"]

## NOTE!
AdminBoundary.objects.all().delete()

#3234 admin2 (us counties)
#3674 admin1 (international states etc)
#254 admin0 (countries
levels = ["ADM0", "ADM1", "ADM2"]

for level in levels:
    results = Place.objects.search("* feature_code:"+level, per_page=10000)
    admin_places = results["places"]

    count = 0

    for admin_place in admin_places:

        admin_geometry = admin_place.geometry
        
        if admin_geometry["type"] == "Polygon" or admin_geometry["type"] == "MultiPolygon":
            pass
        else:
            continue
        #force these polygons into multipolygons
        if admin_geometry["type"] == "Polygon":
            admin_geometry["type"] = "MultiPolygon"
            admin_geometry["coordinates"] = [admin_geometry["coordinates"]] 
            
        geometry = GEOSGeometry(json.dumps(admin_geometry))
        
        alternate_list = []
        if admin_place.alternate:
            for alternate in admin_place.alternate:
                alternate_list.append(alternate["name"])
            
        alt_names = " ".join(alternate_list)
        
        new_admin = AdminBoundary(uuid=admin_place.id, name=admin_place.name, feature_code=level, geom=geometry, uri=admin_place.uris[0], alternate_names=alt_names)
       
        if "http://www2.census.gov/geo/tiger" in admin_place.uris[0]:
            new_admin.queryable_geom = new_admin.geom
            
        new_admin.save()

        count = count + 1
        print count, new_admin

    #now buffer the geom properly    
    print "Executing buffer operation on these "+ str(count) + " "+ level+ " records." 
    cursor = connection.cursor()
    cursor.execute("UPDATE gazetteer_adminboundary SET queryable_geom = ST_Multi(ST_Buffer(geom, 0.144927536)) WHERE queryable_geom IS NULL")
    transaction.commit_unless_managed()
    print "All done for " + level 

print "All done for sure."

