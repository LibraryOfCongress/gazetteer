import sys, re, json

quoted = re.compile(r'"(.+)"')
verb = re.compile(r'.*[/#](.+)$')

item = {}
for line in sys.stdin:
    subj, pred, val = line.strip().split(" ", 2)
    if subj[0] == "<": subj = subj[1:-1] # strip <>
    (pred,) = verb.findall(pred[1:-1])
    val = val[:-2]
    string = quoted.findall(val)
    if string:
        if "@" in val and val.rsplit("@")[-1].lower() != "en":
            # skip this if it's not in English, we're not
            # prepared to deal with it.
            continue
        val = string[0]
    elif val[0] == "<":
        val = val[1:-1] # strip <>
    target = item.setdefault(subj, {"id": subj})
    if pred in target:
        #print >>sys.stderr, "subj[pred]:", subj[pred], "pred:", pred, "val:", val
        if type(target[pred]) is not list: target[pred] = [target[pred]]
        if val not in target[pred]: target[pred].append(val)
    else:
        target[pred] = val

# resolve references
for subj, struct in item.items():
    for key, vals in struct.items():
        if key == "id": continue
        if type(vals) is not list: vals = [vals]
        for val in vals:
            if val in item:
                struct[key] = item[val]

# break circular references, depth first
# prefer retaining http: references over bnodes
for prefix in ("http:", "_:"):
    for subj, struct in item.items():
        if not subj.startswith(prefix): continue
        stack = [struct]
        visited = {} 
        while stack:
            target = stack.pop()
            for key, val in target.items():
                if type(val) is dict:
                    if val["id"] == subj:
                        target[key] = val["id"] # replace ref with id
                    elif val["id"] not in visited:
                        visited[val["id"]] = True
                        stack.append(val)

# dump everything
for key, struct in item.items():
    if key.startswith("http://"):
        print json.dumps(struct)
