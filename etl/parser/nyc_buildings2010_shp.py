import sys, json, os, datetime

from shapely.geometry import asShape, mapping
from fiona import collection

from core import Dump
from feature_type_maps.digitizer_types import use_types_map, use_sub_types_map


def extract_shapefile(shapefile, uri_name, simplify_tolerance=None):
    
    for feature in collection(shapefile, "r"):
        
        geometry = feature["geometry"]
        properties = feature["properties"]

        #calculate centroid
        geom_obj = asShape(geometry)

        if simplify_tolerance:
            geom_obj = geom_obj.simplify(simplify_tolerance)
        
        try:
            centroid = [geom_obj.centroid.x , geom_obj.centroid.y]    
        except AttributeError:
            print "Error: ", feature
            continue
        geometry = mapping(geom_obj)
        

        #Set name.
        #If a building has no name, give it Number and Street Address.
        number = properties["LHND"]
        street = ""
        if number:
            street = " "
        street = street + properties["STNAME"].title()
        addr_name = number + street 
        name = addr_name 
                        
        alternates = []
        
        number = properties["LHND"]
        street = ""
        if number:
            street = " "
        street = street + properties["STNAME"]
        addr_name = number + street 
        name = addr_name
                    
        
        city = ""
        cities = {   "1" :"Manhattan", 
                     "2":  "Bronx", 
                     "3": "Brooklyn", 
                     "4": "Queens",
                     "5":  "Staten Island" }
                  
        if properties["BORO"]:          
            city = cities[properties["BORO"]]
       
        
        address = {
                "number" : properties["LHND"],
                "street" : properties["STNAME"].title(),
                "city" : city,
                "state" : "NY",
                "postcode": properties["ZIPCODE"]
        }
        #feature code mapping
        feature_code = "BLDG" #default code (building)
                
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id. 
        # WFS getFeature link / Warper Layer link? both?
        uri = uri_name + "." + feature["id"]
        
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
            "admin":[],
            "address": address
            
        }
        
        dump.write(uri, place)
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    uri_name = "http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml"
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()
    

#python shapefile.py "/path/to/shapefile/buildings.shp" /path/to/gz_dump 
#python shapefile.py "/home/tim/projects/gaz/queens_buildings/buildings/buildings.shp" dump/shp 

# {'BIN': 1050593.0, 'ADDRTYPE': u'', 'STNAME': u'YORK AVENUE', 'ZIPCODE': u'10128', 'BORO': u'1', 'BLOCK': u'01567', 'LOT': u'0028', 'HHND': u'1671', 'LHND': u'1671'}
