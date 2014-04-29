import json, sys

"""
{
    "geonames": "4046230", 
    "osm": "151583177", 
    "place": {
        "admin1": "Texas", 
        "admin1 attrs": {
            "code": "US-TX", 
            "type": "State"
        }, 
        "admin2": "San Saba", 
        "admin2 attrs": {
            "code": "", 
            "type": "County"
        }, 
        "admin3": "", 
        "areaRank": 2, 
        "boundingBox": {
            "northEast": {
                "latitude": 30.99086, 
                "longitude": -98.697662
            }, 
            "southWest": {
                "latitude": 30.972679, 
                "longitude": -98.718857
            }
        }, 
        "centroid": {
            "latitude": 30.98177, 
            "longitude": -98.70826
        }, 
        "country": "United States", 
        "country attrs": {
            "code": "US", 
            "type": "Country"
        }, 
        "lang": "en-US", 
        "locality1": "Cherokee", 
        "locality1 attrs": {
            "type": "Town"
        }, 
        "locality2": "", 
        "name": "Cherokee", 
        "placeTypeName": "Town", 
        "placeTypeName attrs": {
            "code": 7
        }, 
        "popRank": 1, 
        "postal": "76832", 
        "postal attrs": {
            "type": "Zip Code"
        }, 
        "uri": "http://where.yahooapis.com/v1/place/2378920", 
        "woeid": 2378920
    }, 
    "wiki": "6680949", 
    "woeid": "2378920"
}
"""

for line in file(sys.argv[1]):
    r = json.loads(line)
    print "\t".join(map(str, [
        r["woeid"],
        r["place"]["name"],
        r["place"]["centroid"]["longitude"],
        r["place"]["centroid"]["latitude"],
        r["place"]["placeTypeName"],
        r["place"]["areaRank"],
        r["place"]["popRank"],
        r.get("geonames", ""),
        r.get("osm", ""),
        r.get("wiki", ""),
    ]))
