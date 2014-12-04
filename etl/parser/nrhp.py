import sys, json, os, datetime, glob, codecs

from shapely.geometry import shape, mapping
import fiona

from core import Dump, tab_file

columns = {
            "nrhp": ["main.REFNUM", "RESNAME", "ADDRESS", "CITY", "VICINITY", "COUNTY", "STATE","CERTDATE", "MULTNAME","point.REFNUM", "UTMZONE", "UTMEASTING", "UTMNORTHIN", "Latitude",  "Longitude"]
                }

import osgeo.osr

def transform_utm_to_wgs84(easting, northing, zone):
    utm_coordinate_system = osgeo.osr.SpatialReference()
    utm_coordinate_system.SetWellKnownGeogCS("WGS84") 
    is_northern = northing > 0    
    utm_coordinate_system.SetUTM(zone, is_northern)
    wgs84_coordinate_system = utm_coordinate_system.CloneGeogCS() 
    utm_to_wgs84_transform = osgeo.osr.CoordinateTransformation(utm_coordinate_system, wgs84_coordinate_system)
    return utm_to_wgs84_transform.TransformPoint(easting, northing, 0) # returns lon, lat, altitude


def extract_geojson(csvfile, uri_name, simplify_tolerance):
    features = tab_file(csvfile, columns["nrhp"])

    for feature in features:
        for k,v in feature.items():
            feature[k] = v.strip()
        
        if feature["main.REFNUM"] == "main.REFNUM":
            continue
            
        coords = transform_utm_to_wgs84(int(feature["UTMEASTING"]), int(feature["UTMNORTHIN"]), int(feature["UTMZONE"]))

        centroid = [coords[0], coords[1]]
        geometry =  {"type": "Point", "coordinates": centroid}

        name = feature["RESNAME"]
        if feature["ADDRESS"] and len(feature["ADDRESS"]) > 3:
            address = {
                "number" : '',
                "street" : feature["ADDRESS"],
                "city" : feature["CITY"],
                "state" : feature["STATE"]
            }
        feature_code = "HSTS"
        source = feature
        timeframe = {}
        updated = datetime.datetime.utcnow().replace(second=0, microsecond=0).isoformat()
        uri = uri_name  + str(feature["main.REFNUM"])
        
        alternates = []
        if feature["MULTNAME"] and len(feature["MULTNAME"]) > 3:
            alternates = [{
                    "lang": "en", 
                    "name": feature["MULTNAME"]
                } ]

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
            "admin":[]
        }
        
        dump.write(uri, place)
        

 
if __name__ == "__main__":
    csvfile, dump_path = sys.argv[1:3]
   
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    uri_name = "http://nrhp.focus.nps.gov?referenceNumber:"
    #http://nrhp.focus.nps.gov/natregadvancedsearch.do?referenceNumber:73001435
    
    dump_basename = os.path.basename(csvfile)
    dump = Dump(dump_path + "/json/"+ dump_basename + ".%04d.json.gz")
    extract_geojson(csvfile, uri_name, simplify_tolerance)
    
    dump.close()



#python nrhp.py nhrp.csv nrhpdump

#python nrhp.py "/path/to/directory"   /path/to/gz_dump2
