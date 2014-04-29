import sys, json, os, datetime

from shapely.geometry import asShape, mapping
from fiona import collection

from core import Dump
from feature_type_maps.digitizer_types import use_types_map, use_sub_types_map


def extract_shapefile(shapefile, uri_name, simplify_tolerance=None):
    
    for feature in collection(shapefile, "r"):
        
        geometry = feature["geometry"]
        properties = feature["properties"]
        
        del properties["user_id"]
        del properties["layer_id"]
        del properties["created_at"]
        del properties["updated_at"]
        
        #calculate centroid
        geom_obj = asShape(geometry)
        try:
            centroid = [geom_obj.centroid.x , geom_obj.centroid.y]    
        except AttributeError:
            print "Error: ", feature
            continue
        #optionally simplify geometry
        if simplify_tolerance:
            geometry = mapping(geom_obj.simplify(simplify_tolerance))
        
        #Set name.
        #If a building has no name, give it Number and Street Address.
        number = properties["number"]
        street = ""
        if number:
            street = " "
        street = street + properties["street"]
        addr_name = number + street 
        name = addr_name
        
        #alternate names
        alternates = []
        
        #If a building has a name, put the address in as alternate.
        if properties["name"]:
            name = properties["name"]
            
            if addr_name:
                alternates = [{
                    "lang": "en", 
                    "name": addr_name
                }]

        #TODO fill in city and state if known
        address = {
                "number" : properties["number"],
                "street" : properties["street"],
                "city" : "",
                "state" : "",
        }
        #feature code mapping
        feature_code = "BLDG" #default code (building)
        
        if properties["use_type"]:
            feature_code = use_types_map[properties["use_type"]]
        if properties["use_subt82"]:
            try:
                feature_code = use_sub_types_map[properties["use_subt82"]]
            except KeyError:
                pass
        
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id. 
        # WFS getFeature link / Warper Layer link? both?
        uri = uri_name + "." + feature["id"]
        
        timeframe = {"start_date": properties["layer_year"], "end_date": properties["layer_year"]}
        
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
            "admin":[],
            "address": address
            
        }
        dump.write(uri, place)
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:2]
    
    #TODO uncomment and change this:
    #uri_name = "http://maps.nypl.org/warper/"
    
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()
    

#python shapefile.py "/path/to/shapefile/buildings.shp"  /path/to/gz_dump
#python shapefile.py "/home/tim/projects/gaz/buildings/buildings.shp"  dump/shp 
