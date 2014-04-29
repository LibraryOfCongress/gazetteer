import sys, ngram

#counts = ngram.LessCleverNGramSet()
#counts.load(file("/mnt/geonames/combined.ngrams"))

for line in sys.stdin:
    woeid, woe_name, geonameid, geoname_name, dist = line.strip().split("\t")
    #woe_score = counts.tf_idf(woe_name)
    #geoname_score = counts.tf_idf(geoname_name)
    #score = counts.mutual_tf_idf(woe_name, geoname_name)
    similarity = ngram.ngram_similarity(woe_name, geoname_name)
    if similarity < 1.0:
        print "\t".join(map(str, [woe_name, geoname_name, dist, similarity]))


