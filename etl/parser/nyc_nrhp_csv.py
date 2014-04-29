import sys, json, os, datetime

from shapely.geometry import asShape, mapping
from fiona import collection

from core import Dump, tab_file

columns = {
    "nrhp": ["Historic_Place_Name", "Address", "City", "County", "State","Latitude", "Longitude",
                "NPS_Reference_Number", "Date_Listed", "Notes", "Type", "Geocode_Match"]
                }

def extract_shapefile(shapefile, uri_name, simplify_tolerance=None):
    
    features = tab_file(shapefile, columns["nrhp"])
   
    for feature in features:
        for k,v in feature.items():
            feature[k] = v.strip()


        if feature["Historic_Place_Name"] == "Historic_Place_Name":
            continue
            
        centroid = [float(feature["Longitude"]), float(feature["Latitude"])]
        geometry =  {"type": "Point", "coordinates": centroid}
                   
        addr = ""
        if feature["Address"]:
            name = feature["Address"]
            addr = name
            
        alternates = []    
            
        if feature["Historic_Place_Name"]:
            name = feature["Historic_Place_Name"]
            if addr:
                alternates = [ {
                    "lang": "en", 
                    "name": addr
                } ]

        address = {
                "number" : '',
                "street" : feature["Address"],
                "city" : feature["City"],
                "state" : feature["State"]
        }
        #feature code mapping
        feature_code = "HSTS"
                
        source = feature  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id
        # Must be unique!
        uri = uri_name + "." + feature["NPS_Reference_Number"]
         
        timeframe = {}
        
        updated = "2009-06-23"
        
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
        #print place
        dump.write(uri, place)
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    uri_name = "http://nrhp.focus.nps.gov/natreg/docs/Download.html"
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()


#python shapefile.py "/path/to/shapefile/buildings.shp" /path/to/gz_dump 


