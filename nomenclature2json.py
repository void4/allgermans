import csv
from collections import defaultdict, Counter
import json

csvfile = open("nomenclature.csv")

reader = csv.reader(csvfile, delimiter="\t", quotechar='"')

hierarchy = {"name":"root", "children":[]}#defaultdict(lambda:defaultdict(lambda:defaultdict(dict)))

hname = ["","",""]

def find(d,n,leaf=False):
    for l in d["children"]:
        if l["name"] == n:
            return l
    if leaf:
        d["children"].append({"name":n, "value":1})
    else:
        d["children"].append({"name":n, "children":[]})
    return d["children"][-1]


counter = 0
for row in list(reader)[1:]:
    code = row[0]
    depth = int(row[4])
    name = row[6]
    if depth > 8:
        continue
    elif depth < 8:
        hname[(depth-2)//2] = name
        print(hname)
        continue
    counter += 1
    #print(depth, name)

    #hierarchy[code[:2]][code[2:6]][code[6:8]][code[8:]] = " - ".join(hname + [name])
    #hierarchy[hname[]]
    find(find(find(find(hierarchy, hname[0]), hname[1]), hname[2]), name, True)

print(counter)
print(hierarchy)
"""
result = {"name":"root", "children":[]}

for na,a in hierarchy.items():
    for nb,b in a.items():
        for nc, c in b.items():
            for nd,d in c.items():
                result["root"]
"""

with open("nomenclature.json", "w+") as outfile:
    outfile.write(json.dumps(hierarchy, indent=4))
