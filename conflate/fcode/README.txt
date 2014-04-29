Map OSM ID to prototype feature code (from the Fall 2011 gazetteer):

    copy (
        select replace(substr(url,37), 'area', 'way'), code
            from places_feature f, places_featuretype t
            where f.feature_type_id = t.id and url like
                'http://www.openstreetmap.org/browse/%'
    ) to '/tmp/osm_fcode_map.csv';

Meanwhile, in the conflation database:

    create table osm_fcode_map (id varchar, code varchar);
    copy osm_fcode_map from  '/tmp/osm_fcode_map.csv';
    create index osm_fcode_map_id on osm_fcode_map(id);

Generate the set of matches:

    DROP TABLE fcode_matches;
    create table fcode_matches as
        select g.feature_class, g.feature_type, count(*), m.code, f.name
        from osm_fcode_map m, fcode f, gazetteer g
        where g.source='O' and g.id=m.id and m.code=f.code 
        group by  g.feature_class, g.feature_type, m.code, f.name;

    -- throw away the relatively unused
    DELETE FROM fcode_matches WHERE count < 19;

    DROP TABLE fcode_best;
    CREATE TABLE fcode_best
        AS SELECT feature_class, feature_type, count, code, name
            FROM (
                SELECT *, rank() OVER
                    (PARTITION BY feature_class, feature_type
                         ORDER BY count ASC)
                    FROM fcode_matches
            ) AS foo
            WHERE rank=1;


    update gazetteer g set feature_code = code
        from fcode_best f
        where source = 'O' and feature_code is null 
        and g.feature_class = f.feature_class
        and g.feature_type = f.feature_type; 
