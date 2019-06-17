f = open("americans.htm", "rb")
from collections import OrderedDict
import json
from bs4 import BeautifulSoup

text = f.read().decode(errors='ignore')

soup = BeautifulSoup(text, "html.parser")

cats = {"name":"flare", "children":[]}

for tr in soup.find("tbody").findAll("tr"):
    th = tr.find("th")
    if th is None:
        continue
    p = th.find("p")
    name = th.text

    if name == "Total employed":
        continue

    cls = p.get("class", None)[0]

    if cls is None:
        continue

    data = []
    for td in tr.findAll("td"):
        if td.text != "-":
            data.append(float(td.text.replace(",",".")))
        else:
            data.append(None)

    if cls == "sub0":
        sub0 = {"name":name, "children":[]}
        cats["children"].append(sub0)
    elif cls == "sub1":
        sub1 = {"name":name, "children":[]}
        sub0["children"].append(sub1)
    elif cls == "sub2":
        #TODO age = "-" edge case
        sub2 = {"name":name, "size":data[0]*1000, "age":data[-1]}
        sub1["children"].append(sub2)

    print(name)



jdata = json.dumps(cats, indent=4)
#print(jdata)
f = open("americans.json", "w+")
f.write(jdata)
f.close()
