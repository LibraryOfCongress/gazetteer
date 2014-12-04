import sys, json, os, datetime

from shapely.geometry import shape, mapping
import fiona

from core import Dump
import core
import codecs


#Tiger Line shapefiles 2012 - http://www.census.gov/cgi-bin/geo/shapefiles2012/main
#tl_2012_us_county.zip
#t1_2012_us_state.zip


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
        #optionally simplify geometry
        if simplify_tolerance:
            geometry = mapping(geom_obj.simplify(simplify_tolerance))
        

        name = properties["NAME"].decode("ISO-8859-1").encode("utf-8")
        properties["NAME"] = properties["NAME"].decode("ISO-8859-1").encode("utf-8")
        
        #name, name_long, formal_en, formal_fr, name_sort, name_alt, 
        #alternate names
        alternates = []
        if properties.get("NAMELSAD") and properties["NAMELSAD"] != name:
            properties["NAMELSAD"] = properties["NAMELSAD"].decode("ISO-8859-1").encode("utf-8")
            alternates.append({"lang": "en", "name": properties["NAMELSAD"].decode("ISO-8859-1").encode("utf-8")})

        if properties.get("STUSPS"):
            alternates.append({"lang": "en", "name": properties["STUSPS"].decode("ISO-8859-1").encode("utf-8")})
            
        #feature code mapping
        feature_code = "ADM2" 
        if "tl_2012_us_state" in shapefile:
            feature_code = "ADM1" 
   
        population = None
        
        #to km2
        if properties.get("ALAND"):
            area = "%.2f" % (properties["ALAND"] / 1000000)
            
        
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id. 
        uri = uri_name + "#" + properties["GEOID"]
        
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
            "population": population,
            "area": area,
        }
        

        dump.write(uri, place)
        
    
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    #http://www2.census.gov/geo/tiger/TIGER2012/STATE/tl_2012_us_state.zip
    #http://www2.census.gov/geo/tiger/TIGER2012/COUNTY/tl_2012_us_county.zip
    
    uri_name = "http://www2.census.gov/geo/tiger/TIGER2012/COUNTY/tl_2012_us_county.zip"
    if "tl_2012_us_state" in shapefile:
        uri_name = "http://www2.census.gov/geo/tiger/TIGER2012/STATE/tl_2012_us_state.zip"
        
    
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = .0001
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    dump.max_rows = "1000"
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()
    


#python tiger_line.py ../../../tiger_line/tl_2012_us_state/tl_2012_us_state.shp tigerdump
#python tiger_line.py ../../../tiger_line/tl_2012_us_county/tl_2012_us_county.shp tigerdump


#Layer name: tl_2012_us_state
#Geometry: 3D Polygon
#Feature Count: 56
#Extent: (-179.231086, -14.601813) - (179.859681, 71.441059)
#Layer SRS WKT:
#GEOGCS["GCS_North_American_1983",
    #DATUM["North_American_Datum_1983",
        #SPHEROID["GRS_1980",6378137,298.257222101]],
    #PRIMEM["Greenwich",0],
    #UNIT["Degree",0.017453292519943295]]
#REGION: String (2.0)
#DIVISION: String (2.0)
#STATEFP: String (2.0)
#STATENS: String (8.0)
#GEOID: String (2.0)
#STUSPS: String (2.0)
#NAME: String (100.0)
#LSAD: String (2.0)
#MTFCC: String (5.0)
#FUNCSTAT: String (1.0)
#ALAND: Real (14.0)
#AWATER: Real (14.0)
#INTPTLAT: String (11.0)
#INTPTLON: String (12.0)


#Layer name: tl_2012_us_county
#Geometry: 3D Polygon
#Feature Count: 3234
#Extent: (-179.231086, -14.601813) - (179.859681, 71.441059)
#Layer SRS WKT:
#GEOGCS["GCS_North_American_1983",
    #DATUM["North_American_Datum_1983",
        #SPHEROID["GRS_1980",6378137,298.257222101]],
    #PRIMEM["Greenwich",0],
    #UNIT["Degree",0.017453292519943295]]
#STATEFP: String (2.0)
#COUNTYFP: String (3.0)
#COUNTYNS: String (8.0)
#GEOID: String (5.0)
#NAME: String (100.0)
#NAMELSAD: String (100.0)
#LSAD: String (2.0)
#CLASSFP: String (2.0)
#MTFCC: String (5.0)
#CSAFP: String (3.0)
#CBSAFP: String (5.0)
#METDIVFP: String (5.0)
#FUNCSTAT: String (1.0)
#ALAND: Real (14.0)
#AWATER: Real (14.0)
#INTPTLAT: String (11.0)
#INTPTLON: String (12.0)


