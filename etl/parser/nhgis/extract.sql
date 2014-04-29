create table merged as
    select nhgisnam, statenam, geom,
           min(decade)::integer as start_date,
           max(decade)::integer+10 as end_date 
        from all_tables
        group by nhgisnam, statenam, geom;
