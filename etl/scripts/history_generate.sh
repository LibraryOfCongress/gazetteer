#!/bin/bash

#sh history_generate.sh dump_folder index_name 

defaultindex="gaztest2"

DUMP=${1:-dump}
INDEX=${2:-$defaultindex}

echo "Converting dumps"
time find ${DUMP} -type f | sort | while read i; do
    echo $i 
    python ../parser/history.py $i 'historydump' ${INDEX}
done
