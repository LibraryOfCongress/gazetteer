import sys, json, os, datetime

from shapely.geometry import shape, mapping
import fiona

from core import Dump


def extract_shapefile(shapefile, uri_name, simplify_tolerance=None):
    
    for feature in fiona.open(shapefile, "r"):
        
        geometry = feature["geometry"]
        properties = feature["properties"]
        
        #calculate centroid
        geom_obj = shape(geometry)

        try:
            centroid = [geom_obj.centroid.x , geom_obj.centroid.y]    
        except AttributeError:
            print "Error: ", feature
            continue

        name = properties.get("NAME")

        #feature code mapping
        feature_code = "HSTS"
                
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id
        # Must be unique!
        
        
        uri = uri_name + properties["LP_Number"]

        timeframe = {}
       
        updated = datetime.datetime.utcnow().replace(second=0, microsecond=0).isoformat()

        place = {
            "name":name,
            "centroid":centroid,
            "feature_code": feature_code,
            "geometry":geometry,
            "is_primary": True,
            "source": source,
            "alternate": [],
            "updated": updated,
            "uris":[uri],
            "relationships": [],
            "timeframe":timeframe,
            "admin":[]

        }

        dump.write(uri, place)
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    uri_name = "https://data.cityofnewyork.us/Cultural-Affairs/Historic-district-maps/d4dh-78mx#LPChistoricDistricts/" 
    
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()

#python nyc_landmarks_polygons.py  ../../../LPC_districts_001/LPChistoricDistricts_4326.shp lpcdistricts_dump
#python shapefile.py "/path/to/shapefile/buildings.shp"  /path/to/gz_dump 
