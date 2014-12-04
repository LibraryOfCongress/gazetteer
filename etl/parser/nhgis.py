import sys, json, os, datetime, glob

from shapely.geometry import shape, mapping
import fiona

from core import Dump

#
# Opens a directory containing all the shapefiles, and extracts
#

def extract_shapefile(shapefile, uri_name, simplify_tolerance):
    #with collection(shapefile, 'r') as source:
    #  #print country_code, geo_type, year, os.path.basename(shapefile), source.schema["properties"].keys()
    
    for feature in fiona.open(shapefile, "r"):
        
        geometry = feature["geometry"]
        properties = feature["properties"]
        geom_obj = shape(geometry)
        
        if simplify_tolerance:
            geometry = mapping(geom_obj.simplify(simplify_tolerance))

        try:
            centroid = [geom_obj.centroid.x , geom_obj.centroid.y]
        except AttributeError:
            print "Error: ", feature
            continue
        
	admin = []    
        alternates = []
        name = None
        feature_code = "ADM2H"
	geo_type = "county"	
	if len(properties.get("NHGISNAM")) < 2 or properties.get("NHGISNAM") == None:
	    feature_code = "ADM1H"
            geo_type = "state"
	    name = properties.get("STATENAM")

        if geo_type == "county":
            name = properties.get("NHGISNAM")
	    admin = [{"id": "", "feature_code": "ADM1H", "name": properties.get("STATENAM")}]
            
        if name == None:
            continue
            
        timeframe = {}
	start_year = properties.get("START_DATE")
	end_year = properties.get("END_DATE")
        
        timeframe = {"start": str(int(start_year))+"-01-01", "start_range":0,
                     "end": str(int(end_year-1))+"-12-31", "end_range":0}

        source = properties
        updated = datetime.datetime.utcnow().replace(second=0, microsecond=0).isoformat()
        
        uri = uri_name + "/" + geo_type + "/" + feature["id"]
        
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
            "admin":admin
        }
        dump.write(uri, place)
        

 
if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
   
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    uri_name = "http://nhgis.org/"
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()

    
   # #print shapefile_list
   # for shapefile_path in shapefile_list:
   #     dump_basename = os.path.basename(shapefile_path)
   #     country_code,geo_type,year = dump_basename[:-4].split("_")
   #     uri_name = "http://nhgis.org/"+country_code+"/"+geo_type+"/"+year

    #    simplify_tolerance = .001
  
    #    dump = Dump(dump_path + "/shapefile/"+  dump_basename.strip() + ".%04d.json.gz", max_rows=1000)
        
    #    extract_shapefile(shapefile_path, uri_name, simplify_tolerance, country_code, geo_type, year)
        
    #    dump.close()

#python nhgis.py nhgis_merged.shp nhgisdump

#python nhgis.py  /home/tim/work/gazatteer/nhgis/reprojected nhgisdump

#python nhgis.py "/path/to/directory"   /path/to/gz_dump2
