#!/usr/bin/env python

import sys
places = {}
for line in file("geo_features.txt"):
    name = line.strip()
    places[name] = True

lang, name, count = None, None, None
for line in sys.stdin:
    try:
       lang, name, count, _ = line.split(" ")
    except ValueError:
       continue
    if lang != "en": continue
    if name in places: print "\t".join((name, count))
