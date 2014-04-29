INSERT INTO gazetteer
    SELECT 'O', 'node/' || osm_id::text, COALESCE("name:en", name),
        CASE WHEN "natural" IS NOT NULL THEN 'natural'
             WHEN "place" IS NOT NULL THEN 'place'
             WHEN "historic" IS NOT NULL THEN 'historic'
             WHEN "landuse" IS NOT NULL THEN 'landuse'
             WHEN "man_made" IS NOT NULL THEN 'man_made'
             WHEN "military" IS NOT NULL THEN 'military'
             WHEN "tourism" IS NOT NULL THEN 'tourism'
             WHEN "leisure" IS NOT NULL THEN 'leisure'
             WHEN "railway" IS NOT NULL THEN 'railway'
             WHEN "aeroway" IS NOT NULL THEN 'aeroway'
             WHEN "amenity" IS NOT NULL THEN 'amenity'
             WHEN "building" IS NOT NULL THEN 'building'
             ELSE 'unknown'
        END,
        COALESCE(
            "natural",
            "place",
            "historic",
            "landuse",
            "man_made",
            "military",
            "tourism",
            "leisure",
            "railway",
            "aeroway",
            "amenity",
            "building"),
        NULL, NULL, admin_level, NULL, osm_timestamp::timestamp, way
        FROM planet_osm_point;

INSERT INTO gazetteer
    SELECT 'O', 'way/' || osm_id::text, COALESCE("name:en", name),
        CASE WHEN "natural" IS NOT NULL THEN 'natural'
             WHEN "place" IS NOT NULL THEN 'place'
             WHEN "historic" IS NOT NULL THEN 'historic'
             WHEN "landuse" IS NOT NULL THEN 'landuse'
             WHEN "man_made" IS NOT NULL THEN 'man_made'
             WHEN "military" IS NOT NULL THEN 'military'
             WHEN "tourism" IS NOT NULL THEN 'tourism'
             WHEN "leisure" IS NOT NULL THEN 'leisure'
             WHEN "boundary" IS NOT NULL THEN 'boundary'
             WHEN "railway" IS NOT NULL THEN 'railway'
             WHEN "aeroway" IS NOT NULL THEN 'aeroway'
             WHEN "amenity" IS NOT NULL THEN 'amenity'
             WHEN "building" IS NOT NULL THEN 'building'
             ELSE 'unknown'
        END,
        COALESCE(
            "natural",
            "place",
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
            "building"),
        NULL, NULL, admin_level, NULL, osm_timestamp::timestamp, way
        FROM planet_osm_polygon;

INSERT INTO alt_names
    SELECT 'O', 'node/' || osm_id::text, 'unknown', name
        FROM planet_osm_point
        WHERE "name:en" <> name;

INSERT INTO alt_names
    SELECT 'O', 'way/' || osm_id::text, 'unknown', name
        FROM planet_osm_polygon
        WHERE "name:en" <> name;

INSERT INTO alt_names
    SELECT 'O', 'node/' || osm_id::text, each("name:")
        FROM planet_osm_point;

INSERT INTO alt_names
    SELECT 'O', 'node/' || osm_id::text, each("name:")
        FROM planet_osm_point;
