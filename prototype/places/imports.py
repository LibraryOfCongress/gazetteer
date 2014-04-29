import csv
from settings import DATA_DIR
from os.path import join
from places.models import Feature, FeatureType
from django.contrib.gis.geos import Point

def import_ftypes(f):
    t = csv.reader(f, delimiter="\t")
    for row in t:
        ft = FeatureType()
        ft.feature_class = row[0]
        ft.code = row[1]
        ft.name = row[2]
        try:
            ft.description = row[3]
        except:
            ft.description = ''
        ft.save()
        print "saved " + ft.name


def import_gazetteer(f, limit):
    t = csv.reader(f, delimiter="\t")
    i = 0
    for row in t:
        ft = Feature()
        if Feature.objects.filter(url=row[0]).count() > 0:
            print "duplicate row " + row[0]
        else:
            ft.url = row[0]
            ft.preferred_name = row[1]

            try:
                fcode = FeatureType.objects.get(code=row[2])
            except:
                fcode = None

            ft.feature_type = fcode
            ft.admin1 = row[4]
            ft.admin2 = row[5]
            ft.geometry = Point(float(row[7]), float(row[6]))
            ft.save()
            print "saved " + ft.preferred_name
            i += 1
            if i > limit:
                break

