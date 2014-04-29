create table geoname_osm_best as
select distinct * from geoname_osm_match a where a.osmid=(select
osmid from geoname_osm_match b where a.geonameid = b.geonameid order by
similarity desc limit 1);
