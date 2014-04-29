#!/usr/bin/python
#
# The main 'geoname' table has the following fields :
# ---------------------------------------------------
# geonameid         : integer id of record in geonames database
# name              : name of geographical point (utf8) varchar(200)
# asciiname         : name of geographical point in plain ascii characters, varchar(200)
# alternatenames    : alternatenames, comma separated varchar(5000)
# latitude          : latitude in decimal degrees (wgs84)
# longitude         : longitude in decimal degrees (wgs84)
# feature class     : see http://www.geonames.org/export/codes.html, char(1)
# feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
# country code      : ISO-3166 2-letter country code, 2 characters
# cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
# admin1 code       : fipscode (subject to change to iso code),  varchar(20)
# admin2 code       : code for the second administrative division, varchar(80) 
# admin3 code       : code for third level administrative division, varchar(20)
# admin4 code       : code for fourth level administrative division, varchar(20)
# population        : bigint (8 byte int) 
# elevation         : in meters, integer
# dem               : digital elevation model, srtm3 or gtopo30
# timezone          : the timezone id (see file timeZone.txt) varchar(40)
# modification date : date of last modification in yyyy-MM-dd format
#
# alternate names table
# ---------------------
#
# alternateNameId   : the id of this alternate name, int
# geonameid         : geonameId referring to id in table 'geoname', int
# isolanguage       : iso 639 language code 2- or 3-characters; 4-characters
#                     'post' for postal codes and 'iata','icao' and faac for airport codes, fr_1793
#                     for French Revolution names,  abbr for abbreviation, link for a website,
#                     varchar(7)
# alternate name    : alternate name or name variant, varchar(200)
# isPreferredName   : '1', if this alternate name is an official/preferred name
# isShortName       : '1', if this is a short name like 'California' for 'State of California'
# isColloquial      : '1', if this alternate name is a colloquial or slang term
# isHistoric        : '1', if this alternate name is historic and was used in the past
# 
# Remark : the field 'alternatenames' in the table 'geoname' is a short version
# of the 'alternatenames' table without links and postal codes but with ascii
# transliterations. You probably don't need both.  If you don't need to know the
# language of a name variant, the field 'alternatenames' will be sufficient. If
# you need to know the language of a name variant, then you will need to load the
# table 'alternatenames' and you can drop the column in the geoname table.

# N.B. allCountries.sorted.txt and alternateNames.sorted.txt are pre-sorted as follows:
#   
#   sort -n allCountries.txt > allCountries.sorted.txt
#   sort -k2 -n alternateNames.txt > alternateNames.sorted.txt

from core import Dump, tab_file, transliterate

columns = {
    "geoname": ["geoname_id", "name", "ascii_name", "alternate_names", "latitude", "longitude",
                "feature_class", "feature_code", "admin0", "alternate_admin0", "admin1", "admin2",
                "admin3", "admin4", "population", "elevation", "dem", "timezone", "changed_at"],
    "alternate": ["alternate_name_id", "geoname_id", "lang", "name", "is_preferred", "is_short",
                  "is_colloquial", "is_historic"]
}

def extract_geonames(data_path, dump_path):
    alt_names = tab_file(data_path + "/alternateNames.sorted.txt", columns["alternate"])
    geonames = tab_file(data_path + "/allCountries.sorted.txt", columns["geoname"])
    dump = Dump(dump_path + "/geonames/geonames.%04d.json.gz")
    extra_alt_name = {}
    for geoname in geonames:
        alt_name_list = []
        if extra_alt_name.get("geoname_id") == geoname["geoname_id"]:
            alt_name_list.append(extra_alt_name)
            extra_alt_name = {}
        for alt_name in alt_names:
            if alt_name["geoname_id"] == geoname["geoname_id"]:
                alt_name_list.append(alt_name)
            else:
                extra_alt_name = alt_name
                break
        geoname["alternate_names"] = alt_name_list
        try:
            for col in ("latitude", "longitude"):
                geoname[col] = float(geoname[col])
        except ValueError:
            ### busted coordinates
            continue
        centroid = [geoname["longitude"], geoname["latitude"]]
        population = None
        try:
            population = int(geoname["population"])
        except ValueError:
            pass
        uri = "http://geonames.org/" + geoname["geoname_id"]
        names = []
        alt_name_list.append({
            "name": geoname["name"],
            "lang": "",
            "type": "preferred"
        })
        for alt_name in alt_name_list:
            name_type = ""
            if alt_name.get("is_colloquial"): name_type = "colloquial"
            if alt_name.get("is_historic"): name_type = "historic"
            if alt_name.get("is_preferred"): name_type = "preferred"
            if alt_name.get("is_short"): name_type = "short"
            alt_name = {
                "lang": alt_name["lang"], 
                "type": name_type, 
                "name": alt_name["name"]
            }
            names.append(alt_name)
            ascii_name = transliterate(alt_name)
            if ascii_name: names.append(ascii_name)
        place = {
            "name": geoname["name"],
            "centroid": centroid,
            "feature_code": geoname["feature_code"],
            "geometry": {"type": "Point", "coordinates": centroid},
            "is_primary": True,
            "source": geoname,
            "alternate": names,
            "updated": geoname["changed_at"],
            "population": population,
            "uris": [uri],
            "relationships": [],
            "timeframe": {},
            "admin": []
        }
        dump.write(uri, place)

    dump.close()

if __name__ == "__main__":
    import sys
    data_path, dump_path = sys.argv[1:3]
    extract_geonames(data_path, dump_path)
