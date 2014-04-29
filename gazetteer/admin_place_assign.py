#
# Loads in a json place dump file, does point in polygon with the centroid and the adminboundary
# and assigns the admin record to the place file and saves the place record again  
# 
import gzip,json,sys,os
from django.contrib.gis.geos import GEOSGeometry

from django.core.management import setup_environ
import settings
setup_environ(settings)


from gazetteer.models import AdminBoundary
from gazetteer.place import *



def parse_file(gz_file, new_dump_path):
    file_base, gz_tail = os.path.split(gz_file)
    new_dump_file = new_dump_path + "/"+ gz_tail
    
    f_out = gzip.open(new_dump_file, 'wb')
    
    #print ascasc
    f = gzip.open(gz_file, 'rb')
    count = 0
    for line in f:
        index_json = line
        f_out.write(line) #contains the newline character
        
        doc_json = f.next()  #nextline
        
        doc = json.loads(doc_json)
        if doc.get("centroid"):
            centroid_json = "{'type': 'Point', 'coordinates': "+ str(doc["centroid"]) +"}"
            
            place_geometry = GEOSGeometry(centroid_json) 
            contains_results = AdminBoundary.objects.filter(queryable_geom__contains=place_geometry)
            
            admins_list = []
            for admin in contains_results:
                admins_list.append({"id" : admin.uuid, "feature_code" : admin.feature_code , "name" : admin.name, "alternate_names": admin.alternate_names })
            
            doc["admin"] = admins_list
        
        new_json_doc =  json.dumps(doc, sort_keys=True)
        
        f_out.write(new_json_doc + "\n")
        
        count = count+1
        if count % 100  == 0L:
            print count
            
    f.close()
    f_out.close()

if __name__ == "__main__":
    gz_file, new_dump_path = sys.argv[1:3]
    parse_file(gz_file, new_dump_path)

