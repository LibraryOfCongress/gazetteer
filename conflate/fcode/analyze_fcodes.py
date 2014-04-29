import sys, json

wanted_keys = [
    "place",
    "natural",
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


fcodemap, osmjson = sys.argv[1:3]

osm_fcode = {}
count = 0
for line in file(fcodemap):
    osmtype, osmid, fcode = line.strip().split("\t")
    osmid = int(osmid)
    is_area = 1 if osmtype == 'area' else 0
    osm_fcode[osmid, is_area] = fcode
    count += 1
    if count % 1000 == 0:
        print >>sys.stderr, "\rReading fcode map...", count,
print >>sys.stderr, "\rReading fcode map...", count, "= done."

fcode_tags = {}
count = 0
for line in file(osmjson):
    item = json.loads(line)
    is_area = 1 if item["type"] == 'area' else 0
    fcode = osm_fcode.get((item["id"], is_area))
    if fcode:
        fcode_tags.setdefault(fcode, {})
        for key, value in item["tags"].items():
            #if key in ('name','place_name'): continue
            if key not in wanted_keys: continue
            fcode_tags[fcode].setdefault((key, value), 0)
            fcode_tags[fcode][key, value] += 1
    count += 1
    if count % 1000 == 0:
        print >>sys.stderr, "\rReading OSM records...", count,
print >>sys.stderr, "\rReading OSM records...", count, "= done."

count = 0
for fcode, tags in fcode_tags.items():
    freqs = list(reversed(sorted([(freq, tag) for tag, freq in tags.items()])))
    total = sum(freq[0] for freq in freqs)
    print >>sys.stderr, "\rHandling fcode:", fcode, "=", total, "found..."
    for freq, (key, value) in freqs:
        if freq / float(total) < 1.0 / len(freqs): break
        thunk = "\t".join(map(unicode, [fcode, key, value, freq, "%.3f" % (freq/float(total))]))
        print thunk.encode("utf8")
print >>sys.stderr, ""
