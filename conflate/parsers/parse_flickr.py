import demjson  #flickr geojson is not quite valid json, suffers from trailing commas
import sys
from shapely.geometry import shape
import codecs
#python parse_flickr.py /path/to/flickrShapeFile.geojson | psql gaztest
#continents , counties, countries, localities, neighbourhoods, regions

def parse_flickr_geojson(flickr_file):
    json_data = codecs.open(flickr_file, "r", "utf-8").read()
    
    data = demjson.decode(json_data)

    features =  data['features']
    for feature in features:
        woe_id = str(feature['properties']['woe_id'])
      
        name = feature['properties']['label']
        
        if not name:
            continue
       
        feature_type = feature['properties']['place_type']
        feature_code = str(feature['properties']['place_type_id'])
        json_geometry  = feature['geometry']
        updated = "2011-01-08 00:00:00+00"  #i.e. as from http://code.flickr.com/blog/2011/01/08/flickr-shapefiles-public-dataset-2-0/
        geometry = shape(json_geometry).wkt

        out_line = ['F', woe_id, name, feature_type, feature_code, updated, geometry ]
        
        print "\t".join(out_line)
            
    return flickr_file
    

if __name__ == '__main__':
    flickr_file = sys.argv[1]
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)  #wtf python
    #alt_file = sys.argv[2]
    #print sys.stdout.encoding
    print("BEGIN TRANSACTION;");
    print "COPY gazetteer (source, id, name, feature_type, feature_code, updated, geom) FROM stdin;"
    parse_flickr_geojson(flickr_file)
    print("\\.");
    print("COMMIT;");
 
