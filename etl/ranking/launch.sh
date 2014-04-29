hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.3.0.jar \
    -input /user/pagecounts \
    -output /user/pagecounts.out \
    -mapper wikistats.py \
    -combiner summer.py \
    -reducer summer.py \
    -file wikistats.py \
    -file summer.py \
    -file geo_features.txt
