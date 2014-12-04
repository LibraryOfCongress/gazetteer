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
        if simplify_tolerance:
            geom_obj = geom_obj.simplify(simplify_tolerance)
        
        try:
            centroid = [geom_obj.centroid.x , geom_obj.centroid.y]    
        except AttributeError:
            print "Error: ", feature
            continue
        geometry = mapping(geom_obj)

            
        if properties["FULL_NAME"]:
            name = properties["FULL_NAME"]
                    
        #feature code mapping
        feature_code = "ADM1H"
                
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id
        # Must be unique!
        uri = uri_name + "." + properties["ID"] + "."+ str(properties["VERSION"])
        
        #1766/07/02  to 1766-01-01
        timeframe = {"start": properties["START_DATE"].replace('/','-'), "start_range":0, 
                     "end": properties["END_DATE"].replace('/','-'), "end_range":0}
        
        #TODO admin? for counties?
        
        updated = "2011-10-01"
        
        
        area = properties["AREA_SQMI"]
        place = {
            "name":name,
            "centroid":centroid,
            "feature_code": feature_code,
            "geometry":geometry,
            "is_primary": True,
            "source": source,
            "updated": updated,
            "uris":[uri],
            "relationships": [],
            "timeframe":timeframe,
            "admin":[],
            "area": area
            
        }
        
        dump.write(uri, place)
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    uri_name = "http://publications.newberry.org/ahcbp/downloads/united_states.html.states"
    simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    #simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()

#python shapefile.py "/home/tim/projects/gaz/NYPL_Gazetteer_Data/Historical County Boundaries/NY_Historical_Counties/NY_Historical_States.shp"  "dump2"

#python shapefile.py "/path/to/shapefile/buildings.shp"   /path/to/gz_dump2
