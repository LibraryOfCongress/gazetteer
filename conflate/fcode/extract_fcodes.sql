-- UPDATE gazetteer SET geom = SetSRID(geom, 4326) WHERE SRID(geom) <> 4326;
 
DROP TABLE fcode_joins;
CREATE TABLE fcode_joins
    AS SELECT o.feature_class, o.feature_type, g.feature_code
        FROM gazetteer o JOIN gazetteer g LEFT JOIN osm_fcode_map m ON o.id = m.id
        WHERE o.geom && st_expand(g.geom, 0.01)
        AND o.name = g.name
        AND o.feature_type IS NOT NULL AND o.feature_type <> ''
        AND g.feature_code IS NOT NULL AND g.feature_code <> ''
        AND m.id IS NULL;

DROP TABLE fcode_matches_new;
CREATE TABLE fcode_matches_new
    AS SELECT fcode_joins.feature_class, feature_type, count(*) AS freq, feature_code, name
        FROM fcode_joins, fcode
        WHERE feature_type IS NOT NULL AND feature_type <> ''
        AND feature_code IS NOT NULL AND feature_code <> ''
        AND code = feature_code
        GROUP BY fcode_joins.feature_class, feature_type, feature_code, name;

DROP TABLE fcode_best;
CREATE TABLE fcode_best
    AS SELECT feature_class, feature_type, freq, feature_code, name
        FROM (
            SELECT *, rank() OVER
                (PARTITION BY feature_class, feature_type ORDER BY freq ASC)
                FROM fcode_matches_new
        ) AS foo
        WHERE rank=1;

select * from fcode_best b left join fcode_matches m on (b.feature_class||b.feature_type = m.feature_class||m.feature_type)
    where m.feature_class is null; 
    and freq >= 19



COPY (SELECT * FROM fcode_map ORDER BY freq ASC) TO '/tmp/fcode_map.csv';
