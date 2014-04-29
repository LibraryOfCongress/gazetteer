import sys, json, os, datetime

from shapely.geometry import asShape, mapping
from fiona import collection

from core import Dump


def extract_shapefile(shapefile, uri_name, simplify_tolerance=None):
    
    for feature in collection(shapefile, "r"):
        
        geometry = feature["geometry"]
        properties = feature["properties"]
        
        #calculate centroid
        geom_obj = asShape(geometry)

        try:
            centroid = [geom_obj.centroid.x , geom_obj.centroid.y]    
        except AttributeError:
            print "Error: ", feature
            continue

        boros = {"1":"Manhattan", "2": "Bronx", "3":"Brooklyn", "4": "Queens", "5": "Staten Island"}
        name = "Block "+str(properties["BLOCK"])
        if properties.get("BORO"):
            borough = boros[properties["BORO"]]
            name = borough + ", Block "+ str(properties["BLOCK"])
                
        
        #feature code mapping
        feature_code = "ADM6"
                
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id
        # Must be unique!
        
        bb = str(properties.get("BORO"))+str(properties["BLOCK"])
        
        uri = uri_name + bb +"/"+feature["id"]
        uri_bb = "bb:"+bb
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
            "uris":[uri,uri_bb],
            "relationships": [],
            "timeframe":timeframe,
            "admin":[]

        }
        #print place
        dump.write(uri, place)
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    uri_name = "https://data.cityofnewyork.us/Property/Department-of-Finance-Digital-Tax-Map/smk3-tmxj#block/" 
    
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()


#python shapefile.py "/path/to/shapefile/buildings.shp"  /path/to/gz_dump 
#python nyc_tax_block.py ../../../NYPL_Gazetteer_Data/lots_blocks/DTM_1212_Tax_Block_Polygon_4326.shp  block_dump
