#!/bin/bash

#given a directory of json files, assigns admin boundaries to them and exports
#sh admin_assign.sh src_dump_dir  dest_dump_dir

newdump="admin_parsed"

DUMP=${1:-dump}
NEWDUMP=${2:-$newdump}


echo "Converting dumps"
time find ${DUMP} -type f | sort | while read i; do
    echo $i 
    python ../../gazetteer/admin_place_assign.py $i ${NEWDUMP}
done
