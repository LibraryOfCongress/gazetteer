import urllib, json, sys, os, time, random

APPID = os.environ["YAHOO_APPID"]
lookup_geoname = 'http://where.yahooapis.com/v1/concordance/geonames/%s?format=json&appid='+APPID
#lookup_geoname = 'http://where.yahooapis.com/v1/concordance/iso/US-CA?format=json&appid='+APPID
lookup_woeid = 'http://where.yahooapis.com/v1/place/%s?format=json&appid='+APPID

def call_geoplanet(query):
    time.sleep(86400.0/50000+0.01)
    try:
        result = urllib.urlopen(query).read()
        return json.loads(result)
    except IOError:
        return None
    except ValueError:
        return None

for line in sys.stdin:
    if random.random() > 1/5.0: continue # sample 1 in 5
    geoname_id, name = line.strip().split(None,1)
    result = call_geoplanet(lookup_geoname % geoname_id)
    if not result or 'error' in result: continue
    if "woeid" in result:
        place = call_geoplanet(lookup_woeid % result["woeid"])
        if place and "place" in place: result["place"] = place["place"]
    print json.dumps(result)
