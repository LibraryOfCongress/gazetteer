import array, re, math, json

def ngrams(text, n=3):
    # this bit is special for Geonames:
    text = re.sub(r'\s*\(.*?\)\s*', '', text)
    text = re.sub(r'[^a-z]', '', text.strip().lower())
    text = " " * (n-1) + text + " " * (n-1)
    grams = []
    for i in range(len(text)-n+1):
        grams.append(text[i:i+n])
    return grams

def ngram_similarity(text1, text2, n=3):
    ngrams1, ngrams2 = ngrams(text1), ngrams(text2)
    match = 0
    for ngram in set(ngrams1):
        match += 2 * min(ngrams1.count(ngram), ngrams2.count(ngram))
    return match / float(len(ngrams1) + len(ngrams2))

NGRAM_BASE = ord('z')-ord('a')+2 # " " == 0
NGRAM_MIN = ord('a')-1
_ngram_cache = {}
def index_ngram(text):
    if text in _ngram_cache: return _ngram_cache[text]
    k = 0
    for c in text:
        k *= NGRAM_BASE
        k += 0 if c == " " else ord(c)-NGRAM_MIN
    _ngram_cache[text] = k
    return k

class NGramSet(object):
    def __init__(self, n=3):
        self.n = 3
        self.ngram_count = NGRAM_BASE ** self.n
        self.counts = array.array('L', (0 for i in range(self.ngram_count)))
        self.total = 0

    def add(self, text):
        for ngram in set(ngrams(text, self.n)):
            #print ngram, index_ngram(ngram)
            self.counts[index_ngram(ngram)] += 1
        self.total += 1

    def __getitem__(self, lookup):
        if type(lookup) is str: lookup = index_ngram(lookup)
        return self.counts[lookup]

    def __len__(self):
        return self.total

    def idf(self, lookup):
        return math.log(len(self)/self[lookup])

    def tf_idf(self, text):
        return sum(self.idf(ngram) for ngram in ngrams(text, self.n))

    def mutual_tf_idf(self, text1, text2):
        ngrams1 = ngrams(text1, self.n)
        ngrams2 = ngrams(text2, self.n)
        result  = sum(self.idf(ngram) for ngram in ngrams1 if ngram in ngrams2) \
                + sum(self.idf(ngram) for ngram in ngrams2 if ngram in ngrams1)
        return result / sum(self.idf(ngram) for ngram in (ngrams1 + ngrams2))

    def dump(self, f):
        self.counts[0] = self.total # because "   " isn't a legit trigram
        self.counts.tofile(f)

    def load(self, f):
        self.counts = array.array("L")
        self.counts.fromfile(f, self.ngram_count)
        self.total = self.counts[0]

class LessCleverNGramSet(NGramSet):
    def __init__(self, n=3):
        NGramSet.__init__(self, n)
        self.counts = {}

    def add(self, text):
        for ngram in set(ngrams(text, self.n)):
            self.counts.setdefault(ngram, 0)
            self.counts[ngram] += 1
        self.total += 1

    def __getitem__(self, lookup):
        return self.counts[lookup]

    def dump(self, f):
        self.counts["total"] = self.total # because "total" isn't a legit trigram
        json.dump(self.counts, f)

    def load(self, f):
        self.counts = json.load(f)
        self.total = self.counts["total"]


if __name__ == "__main__":
    import sys
    fname = sys.argv[1]
    store = LessCleverNGramSet()
    try:
        store.load(file(fname))
    except IOError:
        pass
    if len(sys.argv) < 3:
        print "BEGIN:", store.total
        for line in sys.stdin:
            store.add(line)
        store.dump(file(fname, "wb"))
        print "END:", store.total
    else:
        for word in sys.argv[2:]:
            print "%s (%s) tf_idf:%.5f" % (
                    word, ", ".join(("'%s':%d" % gram, store[gram]) for gram in ngrams(word)), 
                    store.tf_idf(word))
