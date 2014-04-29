import csv
import sys
csv.field_size_limit(1000000000)
#python parse_geonames.py /home/tim/work/gazatteer/allCountries.txt  /home/tim/work/gazatteer/alternateNames/alternateNames.txt  | psql gaztest


def parse_geonames_csv(geonames_file):
    csv_reader = csv.reader(open(geonames_file, 'rb'), dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for row in csv_reader:
            out_line = ['G', row[0], row[1], row[6], row[7], row[8], row[10], row[18]+" 00:00:00+00", "POINT("+row[5]+" "+row[4]+")" ] 
            print "\t".join(out_line)
            
    return geonames_file
    


def parse_alt_csv(alt_file):
    csv_reader = csv.reader(open(alt_file, 'rb'), dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for row in csv_reader:
            out_line = ['G', row[1], row[2], row[3]] 
            print "\t".join(out_line)
            
    return alt_file

if __name__ == '__main__':
    geonames_file = sys.argv[1]
    alt_file = sys.argv[2]
    print("BEGIN TRANSACTION;");
    print "COPY gazetteer (source, id, name, feature_class, feature_code, country, admin1, updated, geom) FROM stdin;"
    parse_geonames_csv(geonames_file)
    print("\\.");
    print("COPY alt_names (source, id, lang, name) FROM stdin;");
    parse_alt_csv(alt_file)
    print("\\.");
    print("COMMIT;");
    
    
    
    
    
    
#The main 'geoname' table has the following fields :
#---------------------------------------------------
#geonameid         0: integer id of record in geonames database
#name              1: name of geographical point (utf8) varchar(200)
#asciiname         2: name of geographical point in plain ascii characters, varchar(200)
#alternatenames    3: alternatenames, comma separated varchar(5000)
#latitude          4: latitude in decimal degrees (wgs84)
#longitude         5: longitude in decimal degrees (wgs84)
#feature class     6: see http://www.geonames.org/export/codes.html, char(1)
#feature code      7: see http://www.geonames.org/export/codes.html, varchar(10)
#country code      8: ISO-3166 2-letter country code, 2 characters
#cc2               9: alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
#admin1 code       10: fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
#admin2 code       11: code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
#admin3 code       12: code for third level administrative division, varchar(20)
#admin4 code       13: code for fourth level administrative division, varchar(20)
#population        14: bigint (8 byte int) 
#elevation         15: in meters, integer
#dem               16: digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
#timezone          17: the timezone id (see file timeZone.txt) varchar(40)
#modification date 18: date of last modification in yyyy-MM-dd format
#G, geonameid, name, feature class, feature code, country code, admin1, modification date, [latitude - longitude]

#G', row[0], row[1], row[6], row[7], row[8], row[10], row[18], geom(row[4] row[5]

    #source char(1),
    #id varchar(255),
    #name varchar(255),
    #feature_class varchar(255),
    #feature_type varchar(255),
    #feature_code char(5),
    #country char(2),
    #admin1 char(2),
    #updated timestamp with time zone,
    #geom geometry
    
    
        #create table alt_names (
    #source char(1),
    #id varchar(255),
    #lang varchar(32),
    #name varchar(255)
#);
#alternateNameId   0: the id of this alternate name, int
#geonameid         1: geonameId referring to id in table 'geoname', int
#isolanguage       2: iso 639 language code 2- or 3-characters; 4-characters 'post' for postal codes and 'iata','icao' and faac for airport codes, fr_1793 for French Revolution names,  abbr for abbreviation, link for a website, varchar(7)
#alternate name    3: alternate name or name variant, varchar(200)
#isPreferredName   : '1', if this alternate name is an official/preferred name
#isShortName       : '1', if this is a short name like 'California' for 'State of California'
#isColloquial      : '1', if this alternate name is a colloquial or slang term
#isHistoric        : '1', if this alternate name is historic and was used in the past

##ID 
##0         1 2   3
##3556001	1	fa	-e Zardar	
##"A", row[1], row[2], row[3]]
