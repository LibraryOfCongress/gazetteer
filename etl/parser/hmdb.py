import sys, json, os, datetime

from shapely.geometry import asShape, mapping
from fiona import collection

from core import Dump
import core
import codecs

#name, cmt, desc, link1_href

def extract_shapefile(shapefile, uri_name, simplify_tolerance=None):

    
    for feature in collection(shapefile, "r"):
    
        geometry = feature["geometry"]
        properties = feature["properties"]
        
        #calculate centroid
        geom_obj = asShape(geometry)
        centroid = feature["geometry"]["coordinates"]

        name = properties["name"]
        
        address = {
                "street" : feature.get("cmt")
            }

        #alternate names
        alternates = []
        feature_code = "HSTS"
        
        source = properties  #keep all fields anyhow

        # unique URI which internally gets converted to the place id. 
        uri = properties.get("link1_href") + "#"+feature["id"]
        
        timeframe = {}
        
        updated = datetime.datetime.utcnow().replace(second=0, microsecond=0).isoformat()
    
        place = {
            "name":name,
            "centroid":centroid,
            "feature_code": feature_code,
            "geometry":geometry,
            "is_primary": True,
            "source": source,
            "alternate": alternates,
            "updated": updated,
            "uris":[uri],
            "relationships": [],
            "timeframe":timeframe,
            "admin":[]
        }
        
        dump.write(uri, place)


if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]

    uri_name = "http://www.hmdb.org/"

    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    dump.max_rows = "1000"
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()
    

#python hmdb.py ../../../hmdb.shp hmdbdump
