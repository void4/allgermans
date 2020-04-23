from collections import defaultdict
import json

isco = open("isco08.txt").read().splitlines()

def isint(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def parse(fmt, line):
	result = []
	line = line.split()
	fmt = fmt.split()
	
	if "*" not in fmt and len(line) != len(fmt):
		return
	
	for i, word in enumerate(line):
		f = fmt[i]
		if f == "%s":
			result.append(word)
		elif f == "%i":
			if not isint(word):
				return
			result.append(int(word))
		elif f == "*":
			result += line[i:]
			break
		else:
			if word != f:
				return
			result.append(word)
	
	return result

major = None
submajor = None
minor = None
unit = None

mode = None

db = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"examples":[], "related":[], "excluded":[]}))))
jobs = 0
for line in isco:

	line = line.strip()

	p = parse("Major Group %i", line)
	if p:
		major = p[2]
		continue

	p = parse("Sub-major Group %i", line)
	if p:
		submajor = p[2]
		continue

	p = parse("Minor Group %i", line)
	if p:
		minor = p[2]
		continue

	p = parse("%i *", line)
	if p:
		unit = line
		continue

	p = parse("Examples of the occupations classified here:", line)
	if p:
		mode = "examples"
		continue

	p = parse("Some related occupations classified elsewhere:", line)
	if p:
		mode = "related"
		continue

	p = parse("Excluded from this group are:", line)
	if p:
		mode = "excluded"
		continue

	p = parse("▪ *", line)
	if p:
		job = " ".join(p[1:])
		#print(job)
		jobs += 1
		db[major][submajor][minor][unit][mode].append(job)
		continue
	else:
		print(line)


#print(db)

j = {"name":"flare", "children":[]}

for major, majchildren in db.items():
	j["children"].append({"name":major, "children":[]})
	for submajor, submajchildren in majchildren.items():
		j["children"][-1]["children"].append({"name":submajor, "children":[]})
		for minor, minchildren in submajchildren.items():
			j["children"][-1]["children"][-1]["children"].append({"name":minor, "children":[]})
			for unit, unitdata in minchildren.items():
				j["children"][-1]["children"][-1]["children"][-1]["children"].append({"name":unit, "children":[]})
				for example in unitdata["examples"]:
					j["children"][-1]["children"][-1]["children"][-1]["children"][-1]["children"].append({"name":example})

with open("occupations.json", "w+") as out:
	out.write(json.dumps(j, sort_keys=True, indent=4))

print(j)
print(jobs)
