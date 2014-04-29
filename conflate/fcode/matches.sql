CREATE TABLE fcode_joins
    AS SELECT o.feature_class, o.feature_type, g.feature_code
        FROM gazetteer o LEFT JOIN osm_fcode_map m ON o.id = m.id, gazetteer g                                                                               
        WHERE o.geom && st_expand(g.geom, 0.01)
        AND o.name = g.name
        AND o.feature_type IS NOT NULL AND o.feature_type <> ''                                                                                                 
        AND g.feature_code IS NOT NULL AND g.feature_code <> ''                                                                                                 
        AND m.id IS NULL 

;
