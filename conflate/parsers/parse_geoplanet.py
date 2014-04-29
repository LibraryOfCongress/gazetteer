import csv
import sys
csv.field_size_limit(1000000000)
#python parse_geoplanet.py /path/to/geoplanet/places.txt /path/to/geoplanet/admins.txt  /path/to/geoplanet/aliases.txt  | psql gaztest

#places, admins, aliases

#- 6 fields
  #* WOE_ID                      0- primary "place" key
  #* ISO                         1- ISO 3166-1 country/territory code
  #* Name                        2- preferred local language or english place name
  #* Language                    3- ISO 639-2(b) language code
  #* PlaceType                   4- code indicating place class
  #* Parent_ID                   5 - WOEID of direct parent feature
  #(source, id, name, feature_class, feature_code, country, admin1, updated, geom)

def parse_geoplanet_places_csv(csv_file):
    csv_reader = csv.reader(open(csv_file, 'rb'), dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for row in csv_reader:
            out_line = ['P', row[0], row[1], row[6], row[7], row[8], row[10], row[18]+" 00:00:00+00", "POINT("+row[5]+" "+row[4]+")" ] 
            print "\t".join(out_line)
            
    return csv_file


 #* WOE_ID                      0- primary "place" key
  #* ISO                         1- ISO 3166-1 country/territory code
  #* State                       2- WOEID of admin state
  #* County                      3- WOEID of admin county
  #* Local_Admin                 4- WOEID of local admin
  #* Country                     5- WOEID of country
  #* Continent                   6- WOEID of continent
  

def parse_geoplanet_admins_csv(csv_file):
    csv_reader = csv.reader(open(csv_file, 'rb'), dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for row in csv_reader:
            out_line = ['Q', row[0], row[1], row[6], row[7], row[8], row[10], row[18]+" 00:00:00+00", "POINT("+row[5]+" "+row[4]+")" ] 
            print "\t".join(out_line)
            
    return csv_file
    

  #* WOE_ID                      - primary "place" key
  #* Name                        - alternative place name
  #* Name_Type                   - mnemonic describing name
  #* Language                    - ISO 639-2(b) language code
    
def parse_geoplanet_aliases_csv(csv_file):
    csv_reader = csv.reader(open(csv_file, 'rb'), dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for row in csv_reader:
            out_line = ['A', row[1], row[2], row[3]] 
            print "\t".join(out_line)
            
    return csv_file
    


if __name__ == '__main__':
    geoplanet_places_file = sys.argv[1]
    geoplanet_admins_file = sys.argv[2]
    geoplanet_aliases_file = sys.argv[2]
    print("BEGIN TRANSACTION;");
    print "COPY gazetteer (source, id, name, feature_class, feature_code, country, admin1, updated, geom) FROM stdin;"
    parse_geoplanet_places_csv(geoplanet_places_file)
    print("\\.");
    parse_geoplanet_admins_csv(geoplanet_places_file)
    print("\\.");
    print("COPY alt_names (source, id, lang, name) FROM stdin;");
    parse_geoplanet_aliases_csv(geoplanet_places_file)
    print("\\.");
    print("COMMIT;");
    
#source char(1),
#id varchar(255),
#name varchar(255),
#feature_class varchar(255),
#feature_type varchar(255),
#feature_code char(5),
#country char(4),
#admin1 char(8),
#updated timestamp with time zone,
#geom geometry    

#source char(1),
#id varchar(255),
#lang varchar(32),
#name varchar(255)   
    
    
