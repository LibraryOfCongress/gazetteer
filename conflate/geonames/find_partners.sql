-- select b.osmtype, b.osmid, c.osmtype, c.osmid, similarity(c.name, b.name) as similarity, st_distance_sphere(c.pt, b.pt) as dist  from osm b, osm c where c.osmid=(select a.osmid from osm a where a.pt && st_buffer(b.pt,5/111.1) and a.osmid <> b.osmid order by similarity(a.name,b.name) desc limit 1);

select b.geonameid, c.geonameid, similarity(c.name, b.name) as similarity, st_distance_sphere(c.pt, b.pt) as dist
    from geoname b, geoname c 
    where c.geonameid=(select a.geonameid from geoname a 
                    where a.pt && st_buffer(b.pt,5/111.1) and a.geonameid <> b.geonameid 
                    order by similarity(a.name,b.name) desc limit 1) limit 1000;

