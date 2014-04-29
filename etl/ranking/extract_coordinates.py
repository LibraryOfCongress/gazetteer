# run as: bzgrep georss geo_coordinates_en.nt.bz2 | python extract_coordinates.py | tee geo_features.txt
import re, math, urllib, sys

print >>sys.stderr, "extracting coordinates"
# <http://dbpedia.org/resource/Alabama> <http://www.georss.org/georss/point> "33.0 -86.66666666666667"@en .
coord_regex = re.compile(r'.*/resource/(\S+?)>.*"(-?\d+\.\d+) (-?\d+\.\d+)"')
coords = {}
for line in sys.stdin:
    match = coord_regex.findall(line)
    if not match: continue
    name, lat, lon = match[0]
    coords[name] = (lon, lat)
    print >>sys.stderr, "\r", len(coords),

print >>sys.stderr, "\rextracting counts"
counts = {}
for line in file("geo_counts.txt"):
    name, count = line.strip().split("\t")
    counts[name] = math.log(float(count))
    print >>sys.stderr, "\r", len(counts),

high_count = max(counts.values())
for count, name in sorted((c, n) for n, c in counts.items()):
    count = float(count) / high_count
    lon, lat = coords[name] if name in coords else ("0", "0")
    name = urllib.unquote(name.replace("_", " ")).decode('utf8')
    print "\t".join(map(unicode, (name, count, lon, lat))).encode("utf-8")
