f = open("americans2024.html", "rb")
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
    name = th.text.strip()

    if name == "Total employed":
        continue

    cls = p.get("class", None)[0]

    if cls is None:
        continue

    data = []
    for td in tr.findAll("td"):
        if td.text != "-":
            data.append(float(td.text.replace(",","")))
        else:
            data.append(None)

    if cls == "sub0":
        sub0 = {"name": name, "children": [], "size": data[0] * 1000, "age": data[-1]}
        cats["children"].append(sub0)
    elif cls == "sub1":
        sub1 = {"name": name, "children": [], "size": data[0] * 1000, "age": data[-1]}
        sub0["children"].append(sub1)
    elif cls == "sub2":
        #TODO age = "-" edge case
        sub2 = {"name": name, "children": [], "size": data[0] * 1000, "age": data[-1]}
        sub1["children"].append(sub2)
    elif cls == "sub3":
        sub3 = {"name": name, "children": [], "size": data[0] * 1000, "age": data[-1]}
        sub2["children"].append(sub3)
    else:
        print("not processing cls", cls)

    print(name)

total = 0
def recurse(node):
    global total
    if len(node["children"]) == 0:
        del node["children"]
        total += node["size"]
    else:
        if "size" in node:
            del node["size"]
        if "age" in node:
            del node["age"]
        for node in node["children"]:
            recurse(node)

recurse(cats)

print("total:", total)

jdata = json.dumps(cats, indent=4)
#print(jdata)
f = open("americans.json", "w+")
f.write(jdata)
f.close()
