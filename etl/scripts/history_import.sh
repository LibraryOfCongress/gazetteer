#!/bin/bash

#sh history_import.sh dump_folder localhost:9200 index_name 

defaulthost="localhost:9200"
defaultindex="gaztest2"

TYPE="place"
DUMP=${1:-historydump}
HOST=${2:-$defaulthost}
INDEX=${3:-$defaultindex}-history

API_INDEX=${HOST}/${INDEX}

echo ${DUMP} ${API_INDEX} ${HOST}

#echo -n "Refreshing gazetteer history... "
#curl -s -XDELETE ${API_INDEX} > /dev/null # quash missing index errors
#echo
echo "Loading content..."
time find ${DUMP} -type f | sort | while read i; do
    echo $i 
    zcat $i | \
        curl -s -X POST --data-binary @- ${HOST}/_bulk >/dev/null
done
