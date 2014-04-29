Search Ranking
---------------

This process uses key ideas from mattb's [Where 2.0 workshop](https://github.com/mattb/where2012-workshop).

1. Get `geo_coordinates_en.nt.bz2` from [DBPedia](http://dbpedia.org/Downloads)

2. Use `bzcat` and `perl` to convert the NTriples into a single page name per line in `geo_features.txt`

2. Spin up an EC2 server in us-east-1, clone [Wikipedia Page Counts v2](http://aws.amazon.com/datasets/4182) to EBS, and mount it

3. Install whirr from [whirr.apache.org](http://whirr.apache.org/)

4. Use whirr to spin up an EC2 cluster using hadoop-cdh.properties as the configuration

5. Use `hadoop dfs` to chmod `/user` in HDFS, and mkdir `/user/pagecounts`

6. `hadoop dfs -copyFromLocal /mnt/wikistats/pagecounts/**/*gz /user/pagecounts`. This took about 12 hours.

7. Run `launch.sh` to launch a Hadoop Streaming map-reduce job to filter out
the geotagged pages from the logs and count the occurrences. This only takes 2
hours on a cluster of 6 Hadoop nodes.

8. `hadoop -cat /user/pagecounts.out/* | zcat > geo_counts.txt` or something to that effect.

9. `bzgrep georss geo_coordinates_en.nt.bz2 | python extract_coordinates.py | tee geo_features.txt`
