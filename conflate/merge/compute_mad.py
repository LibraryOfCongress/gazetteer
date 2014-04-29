import numpy, sys

THRESHOLD = float(sys.argv[1])

values = [float(line) for line in sys.stdin]
median = numpy.median(values)
mad = numpy.median([abs(x-median) for x in values])
discard = [x for x in values if abs(x-median) > mad * THRESHOLD]
discard.sort()

print "Median:", median
print "MAD:", mad
print "%.1f x MAD: %f" % (THRESHOLD, mad * THRESHOLD)
print "Discarded: %d (%.2f%%)" % (len(discard), float(len(discard))/len(values)*100.0)
print "Discards: %s ... %s" % (discard[:12], discard[-12:])


