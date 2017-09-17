f = open("data.txt")
f2 = open("customdata.txt")
f3 = open("gb.txt")
from collections import OrderedDict
import json

cats = {"name":"flare", "children":[]}

def idlen(a):
    return len(a.split(" ")[0])

lines = sorted([line.strip() for line in f.readlines()+f2.readlines()], key=idlen)

gblines = sorted([line.strip().split("\t") for line in f3.readlines()])

def findline(starts):
    for line in gblines:
        if line[0].split(" ")[0] == starts:
            return line

def clearnum(s):
    num = s.replace(",","").replace("*","")
    if num in ["", "-"]:
        num = 0
    else:
        num = int(num)
    return num

totalnum = 0

for line in lines:
    line = line.strip().split("\t")
    if len(line)>=1:
        cid, cname = line[0].split(" ",1)
        #
        root = cats["children"]
        for i in range(2,len(cid)):
            skey = cid[:i]
            key = [d for d in root if d["name"].startswith(skey)][0]
            root = key["children"]
        if len(cid)==4:
            if len(line)>1:
                gbnum = findline(cid)
                num = clearnum(line[1])
                if gbnum:
                    num += clearnum(gbnum[1])
            else:
                num = 0
            if num and len(line)>2:
                males = float(clearnum(line[2]))/num
            else:
                males = 0.5
            root.append({"name":line[0].strip(), "size":num, "males":males})
            totalnum += num
        else:
            root.append({"name":line[0].strip(), "children":[]})
    else:
        print("LIENSIGNSING", line)

print(totalnum)

jdata = json.dumps(cats, indent=4)
#print(jdata)
f = open("flare.json", "w+")
f.write(jdata)
f.close()
