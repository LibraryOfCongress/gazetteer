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
        borough = ""
        boros = {"1":"Manhattan", "2": "Bronx", "3":"Brooklyn", "4": "Queens", "5": "Staten Island"}
        if properties.get("BORO"):
            borough = boros[properties["BORO"]] + ", "
        
        block = ""
        if properties.get("BLOCK"):
            block = "Block " + str(properties["BLOCK"]) +", "
        name = borough + block + "Lot " + str(properties["LOT"])

        bbl = properties.get("BBL")  #stored with uris
        
        #feature code mapping
        feature_code = "ADM7"
                
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id
        # Must be unique!
        uri = uri_name  + bbl
        uri_bbl = "bbl:"+bbl
         
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
            "uris":[uri, uri_bbl],
            "relationships": [],
            "timeframe":timeframe,
            "admin":[]

        }
        #print place
        dump.write(uri, place)
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    uri_name = "https://data.cityofnewyork.us/Property/Department-of-Finance-Digital-Tax-Map/smk3-tmxj#lot/" 
    
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()


#python shapefile.py "/path/to/shapefile/buildings.shp"  /path/to/gz_dump 

