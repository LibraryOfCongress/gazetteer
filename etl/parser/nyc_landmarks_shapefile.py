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
            
        addr_name = ""
        if properties["DESIG_ADDR"]:
            addr_name = properties["DESIG_ADDR"]
            name = addr_name
            
        alternates = []
        if properties["LM_NAME"]:
            name = properties["LM_NAME"]
            if addr_name:
                alternates = [{
                    "lang": "en", 
                    "name": addr_name
                }]
    
        address = {
                "number" : properties["HOUSE_NUMB"],
                "street" : properties["STREET_NAM"],
                "city" :  properties["BOROUGH"],
                "state" : "NY"
        }
        
        #feature code mapping
        #Scenic landmark
        #Interior landmark
        #Historic District
        feature_code = "BLDG"
                
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id
        # Must be unique!
        uri = uri_name + "." + properties["BBL"] + "."+ feature["id"]
         
        timeframe = {}
        
        #admin?
        
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

        dump.write(uri, place)
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    uri_name = "http://www.nyc.gov/html/datamine/html/data/terms.html?dataSetJs=geo.js&theIndex=89"
    
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()


#python shapefile.py "/path/to/shapefile/buildings.shp" /path/to/gz_dump 

#COUNT_BLDG (Integer) = 1
#NON_BLDG (String) = (null)
#VACANT_LOT (Integer) = 0
#SECND_BLDG (Integer) = 0
#BIN_NUMBER (Integer) = 3030162
#BBL (String) = 3012090050
#BOROUGH (String) = BK
#BLOCK (Integer) = 1209
#LOT (Integer) = 50  
#LP_NUMBER (String) = LP-2204
#LM_NAME (String) = Crown Heights North Historic District
#OTHER_NAME (String) = (null)
#HOUSE_NUMB (String) = 1407
#STREET_NAM (String) = DEAN STREET
#DESIG_ADDR (String) = 1407 DEAN STREET
#DESIG_DATE (Date) = 2007/04/24
#PUBLIC_HEA (String) = (null)
#LM_TYPE (String) = Historic District
#HIST_DISTR (String) = Yes, Crown Heights North
#BOUNDARIES (String) = Block & Lot
#NOTES (String) = (null)
#STATUS (String) = DESIGNATED
#POINT (1000326.79629946150817 185800.306167847127654)
