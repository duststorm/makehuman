
def readGroupFile(grfile):
	fp= open(grfile, "r")
	grp = ""
	groups = []
	for line in fp: 
		lineSplit= line.split()
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == 'g':
			grp = line
		elif lineSplit[0] == 'f':
			groups.append(grp)
	fp.close()
	return groups


def insertGroupsInFile(infile, outfile, groups):
	infp= open(infile, "r")
	outfp = open(outfile, "w")
	grp = ""
	n = 0
	for line in infp: 
		lineSplit= line.split()
		if len(lineSplit) > 0 and lineSplit[0] == 'f':
			if grp != groups[n]:
				grp = groups[n]
				outfp.write(grp)
			n += 1
		outfp.write(line)
	infp.close()
	outfp.close()

'''
I used this to create my group-free file
def deleteGroupsInFile(infile, outfile):
	infp= open(infile, "r")
	outfp = open(outfile, "w")
	for line in infp: 
		lineSplit= line.split()
		if len(lineSplit) >= 0 and lineSplit[0] == 'g':
			pass
		else:
			outfp.write(line)
	infp.close()
	outfp.close()

#deleteGroupsInFile("base.obj", "base1.obj")
'''

groupFile = "grbase.obj"
inFile = "base1.obj"
outFile = "base2.obj"

groups = readGroupFile(groupFile)
insertGroupsInFile(inFile, outFile, groups)





