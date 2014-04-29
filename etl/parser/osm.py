#!/usr/bin/python
#
#   Table "public.planet_osm_point"
#   Column    |   Type   | Modifiers 
# ------------+----------+-----------
# osm_id      | bigint   | 
# place       | text     | 
# name        | text     | 
# name:en     | text     | 
# timestamp   | text     | 
# admin_level | text     | 
# natural     | text     | 
# historic    | text     | 
# landuse     | text     | 
# man_made    | text     | 
# military    | text     | 
# tourism     | text     | 
# leisure     | text     | 
# railway     | text     | 
# aeroway     | text     | 
# amenity     | text     | 
# building    | text     | 
# name:       | hstore   | 
# way         | geometry | 
# Indexes:
#   "planet_osm_point_index" gist (way)

from core import Dump, Result, transliterate
from osm_types import feature_code_map, admin_level_map, key_tags
import re, psycopg2, json, binascii

def extract_osm(database, table, osm_type, dump):
    geom_col = "way"
    conn = psycopg2.connect("dbname=" + database)
    cursor = conn.cursor(table + "_get_items")
    cursor.execute("""SELECT *, X(st_centroid(%s)) AS centroid_x,
                                Y(st_centroid(%s)) AS centroid_y,
                                ST_AsGeoJSON(%s) AS geojson FROM %s
                                WHERE ST_GeometryType(ST_Centroid(way)) = 'ST_Point'"""
                                % (geom_col, geom_col, geom_col, table))
    for row in Result(cursor):
        preferred_name = row.get("name:en", row.get("name"))
        feature_code = admin_level_map.get(str(row["admin_level"]))
        if not feature_code:
            for tag in key_tags:
                if row.get(tag) and feature_code_map.get((tag, row[tag])):
                    feature_code = feature_code_map[tag, row[tag]]
                    break
        if not preferred_name or not feature_code:
            continue
        centroid = [row["centroid_x"], row["centroid_y"]]
        geometry = json.loads(row["geojson"])
        uri = "http://osm.org/browse/%s/%s" % (osm_type, row["osm_id"])
        if "way/-" in uri:
            uri = uri.replace("way/-", "relation/") + ("#%d" % (binascii.crc32(row["geojson"]) & 0xffffffff))
        names = []
        if row["name"]:
            names.append({"name": row["name"], "lang": "", "type": "preferred"})
        if row["name:"]:
            try:
                alt_names = json.loads("{" + row["name:"].replace("=>", ":") + "}")
                for lang, name in alt_names.items():
                    names.append({
                        "name": name,
                        "lang": lang,
                        "type": "preferred"
                    })
            except (ValueError, UnicodeDecodeError):
                pass
        for alt_name in names:
            ascii_name = transliterate(alt_name)
            if ascii_name and ascii_name["name"] != alt_name["name"]:
                names.append(ascii_name)
        source = dict(row)
        for key in source.keys():
            if not source[key] or key in ("geojson", "centroid_x", "centroid_y", "way"):
                del source[key]
        place = {
            "name": preferred_name,
            "centroid": centroid,
            "feature_code": feature_code, 
            "geometry": geometry,
            "is_primary": True,
            "source": source,
            "alternate": names,
            "updated": row["timestamp"],
            "uris": [uri],
            "relationships": [],
            "timeframe": {},
            "admin": []
        }
        dump.write(uri, place)

if __name__ == "__main__":
    import sys
    database, dump_path = sys.argv[1:3]
    dump = Dump(dump_path + "/osm/osm.%04d.json.gz")
    extract_osm(database, "planet_osm_point", "node", dump)
    extract_osm(database, "planet_osm_polygon", "way", dump)
    dump.close()
