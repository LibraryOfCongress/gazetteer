wget -c http://planet.openstreetmap.org/pbf/planet-latest.osm.pbf

sudo apt-get -y install build-essential libxml2-dev libgeos-dev libpq-dev \
    libbz2-dev proj libtool automake libprotobuf-c0-dev postgresql-9.1-postgis \
    protobuf-c-compiler postgresql-contrib zlib1g-dev libshp-dev libsqlite3-dev \
    libgd2-xpm-dev libexpat1-dev libgeos-dev libxml2-dev libsparsehash-dev \
    libv8-dev libicu-dev libgdal1-dev  libprotobuf-dev protobuf-compiler \
    devscripts debhelper  fakeroot doxygen libboost-dev git-core libgeos++-dev \
    gdal-bin

sudo apt-get -y install libgeos-dev libxml2-dev libpq-dev libbz2-dev \
    protobuf-c-compiler libprotobuf-c0-dev build-essential devscripts debhelper \
    libgeos++-dev

git clone https://github.com/schuyler/osm2pgsql.git
cd osm2pgsql/
dpkg-buildpackage -rfakeroot
cd ..
sudo dpkg -i osm2pgsql*.deb

sudo vi /etc/postgresql/9.1/main/postgresql.conf 

# Tune up PostgreSQL
#
shared_buffers = 8GB 			# about 1/4 of RAM
checkpoint_segments = 128
checkpoint_completion_target = 0.9
effective_cache_size = 16GB		# about 1/2 of RAM
autovacuum = off
work_mem = 32MB				# min 64kB
maintenance_work_mem = 256MB		# min 1MB

sudo vi /etc/sysctl.conf

# Allow PostgreSQL to allocate 6GB of shared memory
#
kernel.shmmax=6615089152

sudo sysctl -w kernel.shmmax=9000000000
sudo sysctl -w kernel.shmall=9000000000
sudo /etc/init.d/postgresql restart

sudo su -c 'createuser -s sderle' postgres
createdb template_postgis
psql template_postgis < /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql template_postgis < /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql

time osm2pgsql --latlong --multi-geometry --cache 36000 \
    --input-reader pbf --create --unlogged \
    --hstore-column "name:" --extra-attributes \
    --style ~/gazetteer/conflate/osm2pgsql/place.style \
    planet-latest.osm.pbf

export OPID=`ps a | grep osm2pgsql | grep -v grep | cut -c1-6`
while kill -0 $OPID; do sleep 1; done && \
    pg_dump -t planet_osm_point -t planet_osm_line -t planet_osm_polygon \
        --blobs --no-privileges gis \
        | bzip2 > osm_dump.sql.bz2 

bzcat osm_dump.sql.bz2 | time psql conflation
8.46user 5.78system 14:23.43elapsed 1%CPU (0avgtext+0avgdata 20080maxresident)k


