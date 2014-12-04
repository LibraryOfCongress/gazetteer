import sys, json, os, datetime
import csv
import codecs
from shapely.geometry import shape, mapping
import fiona

from core import Dump
import core


#using natural earth shapefiles - version 2.0.0
#admin 0 http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip
#admin 1 http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces_shp.zip


def extract_shapefile(shapefile, uri_name, simplify_tolerance=None):
    csvfile = open('admin_csv_file', 'wb')
    csv_writer = csv.writer( csvfile, delimiter='\t') 
    
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
        

        name = properties["name"]
        
        #name, name_long, formal_en, formal_fr, name_sort, name_alt, 
        #alternate names
        alternates = []
        if properties.get("name_long") and properties["name_long"] != name:
            alternates.append({"lang": "en", "name": properties["name_long"]})
            
        if properties.get("name_sort") and properties["name_sort"] != name:
            alternates.append({"lang": "en", "name": properties["name_sort"]})
            
        if properties.get("abbrev"):
            alternates.append({"lang": "en", "name": properties["abbrev"]})
        
        if properties.get("iso_a3"):
            alternates.append({"lang": "en", "name": properties["iso_a3"]})
            
        if properties.get("formal_en") and properties["formal_en"] != name:
            alternates.append({"lang": "en", "name": properties["formal_en"]})
            
        if properties.get("formal_fr"):
            alternates.append({"lang": "fr", "name": properties["formal_fr"]})
            
        if properties.get("name_alt"):
            alternates.append({"lang": "en", "name": properties["name_alt"]})
            
        #name_local is all garbled...
        #if properties.get("name_local"):

        #feature code mapping
        feature_code = "ADM1" 
        if properties["featurecla"] == "Admin-0 country":
            feature_code = "ADM0" 
   
        population = None
        if properties.get("pop_est"):
            population = properties["pop_est"]
        
        del properties["wikipedia"]
        
        source = properties  #keep all fields anyhow
        
        # unique URI which internally gets converted to the place id. 
        uri = uri_name + "#" + feature["id"]
        
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
        }
        
        es_uuid = core._id(uri)
        #uuid, name, feature_code, geom
        row = [es_uuid, name, feature_code, geom_obj.wkt]
        csv_writer.writerow([s.encode("utf-8") for s in row])
        
        dump.write(uri, place)
        
    
        

if __name__ == "__main__":
    shapefile, dump_path = sys.argv[1:3]
    
    
    uri_name = "http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/"
    if "ne_10m_admin_1_states" in shapefile:
        uri_name = "http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/"
        
    
    #simplify_tolerance = .01 # ~ 11km (.001 = 111m)
    simplify_tolerance = None
    
    dump_basename = os.path.basename(shapefile)
    dump = Dump(dump_path + "/shapefile/"+ dump_basename + ".%04d.json.gz")
    
    extract_shapefile(shapefile, uri_name, simplify_tolerance)
    
    dump.close()
    

#python admin_0_1_natearth.py ../../../natural_earth/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp admindump
#python admin_0_1_natearth.py ../../../natural_earth/ne_10m_admin_1_states_provinces_shp/ne_10m_admin_1_states_provinces_shp.shp admindump

#see models.py for table creation sql
#"python manage.py sqlall gazetteer"  to show the generated sql 
#python manage.py syncdb to create the table

#psql commands
#1. Import the csv file
#copy gazetteer_adminboundary (uuid, name, feature_code, raw_geom) from '/home/tim/work/gazatteer/gazetteer/etl/parser/admin_csv_file'
#2. Convert any polygons to multipolygons
#update gazetteer_adminboundary set geom = ST_Multi(ST_GeomFromText(raw_geom, 4326));
