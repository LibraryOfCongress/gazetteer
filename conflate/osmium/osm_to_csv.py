import json, shapely.wkt, sys

wanted_keys = [
    "natural",
    "place",
    "historic",
    "landuse",
    "man_made",
    "military",
    "tourism",
    "leisure",
    "boundary",
    "railway",
    "aeroway",
    "amenity",
    "building",
];

# {"geom":[-116.8646118,34.9483727],"tags":{"name":"Calico ghosttown","place":"village"},"type":"node","id":670761}

count = 0
for line in sys.stdin:
    item = json.loads(line)
    lon, lat = 0, 0
    if "geom" not in item: continue
    if type(item["geom"]) is list:
        lon, lat = item["geom"]
    else:
        geom = shapely.wkt.loads(item["geom"])
        centroid = geom.convex_hull.centroid
        lon, lat = centroid.x, centroid.y
    feature_class = feature_type = None
    for key in wanted_keys:
        if item["tags"].get(key):
            feature_class = key
            feature_type = item["tags"][key]
            break
    name = item["tags"].get("name") or item["tags"].get("place_name")
    output = "\t".join(map(unicode, (item["id"], name, item["type"], feature_class, feature_type, lon, lat)))
    print output.encode("utf-8")
    count += 1
    if count % 100 == 0: print >>sys.stderr, "\r", count,

print >>sys.stderr, "done."

