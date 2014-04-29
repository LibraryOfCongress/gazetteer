drop table gazetteer;
create table gazetteer (
    source char(1),
    id varchar(255),
    name varchar(255),
    feature_class varchar(255),
    feature_type varchar(255),
    feature_code char(5),
    admin_level char(2),
    country char(4),
    admin1 char(8),
    updated timestamp with time zone,
    geom geometry
);

drop table alt_names;
create table alt_names (
    source char(1),
    id varchar(255),
    lang varchar(255),
    name varchar(255)
);

create index gazetteer_source_id on gazetteer (source, id);
create index gazetteer_geom_gist on gazetteer using gist (geom);
create index alt_names_source_id on alt_names (source, id);
