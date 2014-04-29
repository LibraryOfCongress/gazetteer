import gzip,json,hashlib,time,sys,uuid
from core import Dump

#python history.py '/path/to/dump001.gz' '/path/to/putdumps/' 'placeindex'
#python history.py 'tmp/gaz.01.gz' 'history/dump' 'gazetteer'

#generates history.001.gz files in the /path/to/putdumps/historydump' directory
#use history_import.sh to import them or unpacked manually:
#curl -s -XPOST http://localhost:9200/_bulk --data-binary @history1.0001.json

def generate_history(gz_file, dump_path, place_index):
    f = gzip.open(gz_file, 'rb')
    uid = uuid.uuid4()
    unique_name = uid.hex
    dump = Dump(dump_path + "/historydump/history"+unique_name+".%04d.json.gz")
    histindex = place_index+"-history"  #i.e. gazetest2-history
    
    for line in f:
        index_json = line
        doc_id = json.loads(index_json)["index"]["_id"]
        
        doc_json = f.next()  #nextline
        doc = json.loads(doc_json)

        digest = hashlib.sha1(json.dumps(doc, sort_keys=True)).hexdigest()

        #SAVE HISTORY (the records tied to a place which have revisions)
        history_doc = {"index" : place_index, "type": "place", "id" : doc_id, "revisions": [{"user_created":"ETL", "created_at":time.time(),"digest":digest}]}
        
        dump.write_bulk(histindex, "place", doc_id, history_doc)

    f.close()
    dump.close()

if __name__ == "__main__":
    gz_file, dump_path, place_index = sys.argv[1:4]
    generate_history(gz_file, dump_path, place_index)
    
