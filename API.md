Gazetteer API Documentation
===========================

API outline
-----------

* Entity search
* Name
* Bounding box
* Hierarchy
* Concordance
* Time frame, feature type, language filters
* Entity retrieval
* Entity revision history retrieval
* Entity revision
* Entity revision rollback
* Geographic hierarchy query
* Incremental conflation methods
* API sketch

API Methods
-----------

* `GET /place/{id}.json`
* `PUT /place/{id}.json`
* `POST /place.json`
* `DELETE /place/{id}.json`
* `GET /place/search.json`
* `GET /place/{id}/similar.json`
* `GET /place/{id}/hierarchy.json`
* `GET /place/{id}/history.json`
* `GET /place/{id}/{revision}.json`
* `PUT /place/{id}/{revision}.json`
* `GET /place/{id}/relations.json`
* `PUT /place/{id}/{relation}/{id}.json`
* `DELETE /place/{id}/{relation}/{id}.json`

(relation = conflates, supersedes, subsumes, etc.)

Example Place
-------------

    {
      "_id": "0123456789abcd",
      "name": "Ham",
      "feature_code": "PPL", 
      "updated": "2012-08-31T09:56:58.010448+02:00", 
      “is_primary”: true,
      "geometry": {“type”: “polygon”, “coordinates”: [...]}, 
      “centroid”: [ -0.5, 52.3 ],
      “population”: 355,
      “area”: 650, # sq km
      “importance”: 0.05, # 0.0-1.0
      “alternate_names”: [
        { “lang”: “en”, “name”: “Ham Town”, “type”: “informal” },
        { “lang”: “ru”, “name”: “Xam” }
        ...
      ],
      “relationships”: [
        { “type”: “conflates”, “id”: “geonames.org/feature/39128192” },
        { “type”: “superseded_by”, “id”: “osm.org/browse/node/23947201” }
      ],
      “timeframe”: {
        “start_date”: “1320”,
        “end_date”: “1983”,
        “start_precision”: “365250”, # days
        “end_precision”: “365”
      },
      “admin”: {
         “admin0”: “United Kingdom”, # or maybe the primary ID for the UK
         “admin1”: “England”, # or wherever Ham is
         “admin2”: “Essex” # blah
      },
      “source”: {
        “origin”: “osm”, # this could also be “geonames” etc.
        “properties”: {
          “place”: “hamlet”,
          … # other OSM tags
        }
      },
    }

