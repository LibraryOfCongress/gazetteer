#!/usr/bin/env python
import sys
counts = {}
for line in sys.stdin:
    try:
        name, count = line.strip().split("\t")
    except ValueError:
        continue
    counts.setdefault(name, 0)
    counts[name] += int(count)

for name, count in counts.items():
    print "\t".join((name, str(count)))
