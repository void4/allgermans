f = open("data.txt")
f2 = open("customdata.txt")
from collections import OrderedDict
import json

cats = {"name":"flare", "children":[]}

def idlen(a):
    return len(a.split(" ")[0])

lines = sorted([line.strip() for line in f.readlines()+f2.readlines()], key=idlen)

def clearnum(s):
    num = s.replace(",","").replace("*","")
    if num in ["", "-"]:
        num = 0
    else:
        num = int(num)
    return num

for line in lines:
    line = line.strip().split("\t")
    if len(line)>=2:
        cid, cname = line[0].split(" ",1)
        #
        root = cats["children"]
        for i in range(2,len(cid)):
            skey = cid[:i]
            key = [d for d in root if d["name"].startswith(skey)][0]
            root = key["children"]
        if len(cid)==4:
            num = clearnum(line[1])
            if num and len(line)>2:
                males = float(clearnum(line[2]))/num
            else:
                males = 0.5
            root.append({"name":line[0].strip(), "size":num, "males":males})
        else:
            root.append({"name":line[0].strip(), "children":[]})
    else:
        print("LIENSIGNSING", line)

jdata = json.dumps(cats, indent=4)
#print(jdata)
f = open("flare.json", "w+")
f.write(jdata)
f.close()
