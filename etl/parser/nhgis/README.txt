# new database
createdb -Ttemplate_postgis nhgis

# import the NHGIS shapefiles
unzip /home/tim/nhgis_shapefiles/nhgis_reprojected.zip 
cd reprojected/
for i in *.shp; do shp2pgsql -s4326 $i ${i%%.shp}; done | psql nhgis

# create the all_tables view
echo '\d' | psql nhgis >view.sql
vi view.sql # a whole bunch of munging by hand with regexes in vim
psql nhgis <view.sql

# group and extract the objects
psql nhgis <extract.sql
cd ..
mkdir merged
pgsql2shp -f merged/nhgis_merged.shp nhgis merged
