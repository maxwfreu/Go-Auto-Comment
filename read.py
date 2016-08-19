import re

class Func(object):
    name = ""
    params = 0
    returns = ""

    def __init__(self,name, params, returns):
        self.name = name
        self.params = params
        self.returns = returns

# Given a go file pathname, opens the file and creates the func objects from the functions in the file
def findFuncs(pathname):
	lines = [line.rstrip('\n') for line in open(pathname)]
	allFuncs = []
	for s in lines:
		ns = s.split()
		# print ns
		if len(ns) == 0:
			continue
		if ns[0] == 'func':
			m = re.search('\((.*?)\)', s)
			funcName = ns[1].rsplit("(", 1)[0]
			if m:
				found = m.group(1)
			r = re.search('\)(.*?)\{', s)
			if r:
				z = r.group(1)
				t = re.search('\((.*?)\)', z)
				if t:
					rt = t.group(1)
					func = Func(funcName, found, rt)
					allFuncs.append(func)
				else:
					func = Func(funcName, found, z)
					allFuncs.append(func)

	return allFuncs;

# Builds the comments to insert into the file
def buildComments():
	for p in params:
		comment = "//---------------------------\n// func: "+ p.name + "\n// params:\n"
		args = p.params.split(",")
		for arg in args:
			comment += "         - "+ arg + "\n"
		comment += "// returns:\n"
		returns = p.returns.split(",")
		for rt in returns:
			empty = re.search('[a-zA-Z]', rt)
			if not empty:
				comment += "         - nothing\n"
			else:
				comment += "         - "+ rt + "\n"
		comment += "// desc: [DESCRIPTION HERE]\n"
		comment += "//---------------------------"
		print comment

# Generate comments
var = raw_input("pathname: ")
params = findFuncs(var)
buildComments()