#!/bin/bash

#sh gazetteer_import.sh dump_folder localhost:9200 index_name 

defaulthost="localhost:9200"
defaultindex="gaztest2"
TYPE="place"

DUMP=${1:-dump}
HOST=${2:-$defaulthost}
INDEX=${3:-$defaultindex}

API=${HOST}/${INDEX}

#
# Uncomment the following 3 lines if you want to replace the data
#
#echo -n "Refreshing gazetteer... "
#curl -s -XDELETE ${API} > /dev/null # quash missing index errors
#curl -s -XPOST -d @../mapping/place.json ${API}


echo
echo "Loading content..."
time find ${DUMP} -type f | sort | while read i; do
    echo $i 
    zcat $i | \
        curl -s -X POST --data-binary @- ${API}/${TYPE}/_bulk >/dev/null
done

echo "Refresh index"
curl -s -XPOST ${API}/_refresh >/dev/null
