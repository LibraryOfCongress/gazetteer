-------------------
Topomancy Gazetteer
-------------------
Release: 8 Oct 2012

1) Ensure that you have ElasticSearch running.

2) Edit `gazetteer_import.sh` to reflect your ElasticSearch installation.
   Sensible defaults are provided.

3) Run `gazetteer_import.sh`. The process takes about 45 minutes on our
   development server.

4) Try the following queries:

    curl -s http://localhost:9200/gazetteer/place/_search?q=name:New+York\&pretty=true

    curl -s -d @sample_query.json http://localhost:9200/gazetteer/place/_search?pretty=true


Please contact team@topomancy.com if you have any questions.

---
Notes for history and gazetter import for development:
---

1. Generate history dumps from standard records

add new directory in scripts file called "dump" - place in here the gz files for import

in scripts/ run "sh history_generate.sh dump_folder index_name"  where dump_folder is the directory where the dumps are (defaults to dump) and index is the index (default gaztest2)
(this reads in the standard data gz dump files and created appropriate history files for import)
these history dumps are in scripts/historydump.

2. Import standard records

Import standard records dumps
sh gazetteer_import.sh dump

(sh gazetteer_import.sh dump_folder localhost:9200 index_name )

3. Import history dumps

(sh history_import.sh dump_folder localhost:9200 index_name )
sh history_import.sh 



