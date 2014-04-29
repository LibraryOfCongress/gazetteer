import shapely.wkb, shapely.geometry 
import osgeo.ogr
import sys, os.path

def read_with_ogr (filename, fatal_errors=True):
    """Read features out of a shapefile and yield a tuple of (geometry, attrs)
       for each feature."""
    source = osgeo.ogr.Open(filename, False)
    layer = source.GetLayer(0)
    defn = layer.GetLayerDefn()
    fields = [defn.GetFieldDefn(i).GetName().lower() for i in range(defn.GetFieldCount())]

    layer.ResetReading()
    ogr_feature = layer.GetNextFeature()
    while ogr_feature:
        try:
            geometry = shapely.wkb.loads(ogr_feature.GetGeometryRef().ExportToWkb())
        except Exception, e:
            if fatal_errors:
                raise
            else:
                print >>sys.stderr, "Shapely error:", str(e)
            ogr_feature.Destroy()
            ogr_feature = layer.GetNextFeature()
            continue
        attrs = []
        for n, name in enumerate(fields):
            value = ogr_feature.GetField(n)
            if isinstance(value, basestring):
                try:
                    value = value.decode("utf-8")
                except UnicodeDecodeError:
                    value = value.decode("latin-1") 
            attrs.append(value)
        ogr_feature.Destroy()
        yield geometry, attrs
        ogr_feature = layer.GetNextFeature()
    source.Destroy()

for shpfile in sys.argv[1:]:
    year = os.path.basename(shpfile).split(".")[0][-4:]
    print >>sys.stderr, year
    for geometry, attrs in read_with_ogr(shpfile, False):
        attrs += [year, geometry.simplify(.01).to_wkt()]
        for n, val in enumerate(attrs):
            if val is None: attrs[n] = ""
        print "\t".join(map(unicode,attrs)).encode("utf8")
