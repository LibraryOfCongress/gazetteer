import sys, json, os, datetime

from shapely.geometry import shape, mapping
from shapely import wkt
import fiona

from feature_type_maps.digitizer_types import use_types_map, use_sub_types_map

from core import Dump, tab_file


columns = {
    "perris": ["FID","user_id", "layer_id", "created_at", "updated_at", "comment", "additional_information",
    "secondary_address_temp", "secondary_street", "secondary_number", "boilers", "skylights", "buildings_communicating",
    "stores", "roof_type", "class", "name", "number", "street", "materials", "use_type", "use_subtype", "geom", "layer_year" ]
           }

def extract_shapefile(shapefile, uri_name, simplify_tolerance=None):
    
    features = tab_file(shapefile, columns["perris"])

    for feature in features:
        
        
        if feature["geom"] == "geom":
            #skip first item
            continue
            
        del feature["user_id"]
        del feature["layer_id"]
        del feature["created_at"]
        del feature["updated_at"]
        
        for k,v in feature.items():
            feature[k] = v.strip()
    
        wkt_geom = feature["geom"]
        del feature["geom"]
        
        geom_obj = wkt.loads(wkt_geom)
        
        if simplify_tolerance:
            geom_obj = geom_obj.simplify(simplify_tolerance)
        
        try:
            centroid = [geom_obj.centroid.x , geom_obj.centroid.y]    
        except AttributeError:
            print "Error: ", feature
            continue
        geometry = mapping(geom_obj)
       
        
        number = feature["number"]
        street = ""
        if number:
            street = " "
        street = street + feature["street"]
          
        addr_name = number + street

        name = addr_name
        
        #alternate names
        alternates = []
        
        if feature["name"]:
            name = feature["name"]
            
            #put address in alternate names
            if addr_name:
                alternates = [ {
                    "lang": "en", 
                    "name": addr_name
                } ]
                
        if feature["secondary_address_temp"]:
            alternates.append( { "lang":"en",  "name":  feature["secondary_address_temp"] } )
                
        address = {
                "number" : feature["number"],
                "street" : feature["street"],
                "city" : "New York City",
                "state" : "NY"
        }

            
        #feature code mapping
        feature_code = "BLDG" #default code (building)
        
        if feature["use_type"]:
            feature_code = use_types_map[feature["use_type"]]
        if feature["use_subtype"]:
            try:
                feature_code = use_sub_types_map[feature["use_subtype"]]
            except KeyError:
                pass
                
        source = feature  #keep all fields  in source
        
        # unique URI which internally gets converted to the place id
        # Must be unique!
        uri = uri_name + "." + feature["FID"]
         
        timeframe = {"start": "1854-01-01", "start_range":0,
                     "end": "1854-01-01", "end_range":0}
        
        updated = "2012-10-01"

        place = {
            "name":name,
            "centroid":centroid,
            "feature_code": feature_code,
            "geometry": geometry,
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
    uri_name = "http://maps.nypl.org/warper/layers/861"
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()
    


#python shapefile.py "/path/to/shapefile/buildings.shp" /path/to/gz_dump

#python nyc_perris_digitizer_csv.py ../../../GazetteerData/Manhattan\ Buildings\ Perris\ 10_23_2012/FinalCleanedData_Perris1854_tab.csv nydump

