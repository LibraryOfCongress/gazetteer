import hashlib, json, os, gzip, sys, re
from unidecode import unidecode

def tab_file(fname, cols):
    for line in file(fname).readlines():
        vals = line.strip().split("\t")
        yield dict(zip(cols, vals))

def _id(uri):
    return hashlib.md5(uri).hexdigest()[:16]

has_unicode = re.compile(r'[^\0x00-0x7f]')
def transliterate(alt_name):
    if has_unicode.search(alt_name["name"]):
        try:
            xlit = unidecode(alt_name["name"].decode("utf8"))
        except (UnicodeDecodeError, UnicodeEncodeError):
            try:
                xlit = unidecode(alt_name["name"].decode("latin1"))
            except (UnicodeEncodeError, UnicodeEncodeError):
                return
        if xlit != alt_name["name"]:
            addl_name = alt_name.copy()
            addl_name["lang"] = alt_name["lang"] + ":ascii"
            addl_name["name"] = xlit
            return addl_name

def Result(cursor, arraysize=10000):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        cols = [c.name for c in cursor.description]
        for result in results:
            yield dict(zip(cols, result))

class Dump(object):
    def __init__(self, template, max_rows=1000):
        self.max_rows = max_rows
        self.rows = 0
        self.content = ""
        self.template = template
        path = os.path.dirname(template)
        if not os.path.exists(path): os.makedirs(path)
    
    def write_bulk(self, index, doc_type, doc_id, place):
        self.content += json.dumps({"index": {"_id": doc_id, "_index":index, "_type": doc_type}})
        self.write_place(place) 

    def write(self, uri, place):
        self.content += json.dumps({"index": {"_id":_id(uri)}})
        try:
            self.write_place(place)
        except(UnicodeDecodeError):
            print place

    def write_place(self, place):
        self.content += "\n" + json.dumps(place, sort_keys=True) + "\n"
        self.rows += 1
        if self.rows % (long(self.max_rows) / 10) == 0L: print >>sys.stderr, "\r% 9d" % self.rows,
        if self.rows % long(self.max_rows) == 0L: self.flush()

    def flush(self, final=0):
        fname = self.template % (int(self.rows/long(self.max_rows))+final)
        print >>sys.stderr, " ", fname
        out = gzip.open(fname, "wb")
        out.write(self.content)
        out.close()
        self.content = ""

    def close(self):
        self.flush(final=1)
