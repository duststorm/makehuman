#
#	mhx_diff.py
#	Utility that lists differences between two mhx files
#	Usage from terminal: 
#		python mhx_diff.py
#
#

import os

#
#	tokenizeMhxFile(filePath):
#

def tokenizeMhxFile(filePath):	
	fileName = os.path.expanduser(filePath)
	(shortName, ext) = os.path.splitext(fileName)
	if ext != ".mhx":
		print("Error: Not a mhx file: " + fileName)
		return
	print( "Opening MHX file "+ fileName )

	ignore = False
	stack = []
	tokens = []
	key = "toplevel"
	level = 0

	fp= open(fileName, "rU")
	print( "Tokenizing" )
	lineNo = 0
	for line in fp: 
		# print(line)
		lineSplit= line.split()
		lineNo += 1
		if len(lineSplit) == 0:
			pass
		elif lineSplit[0] == '#':
			pass
		elif lineSplit[0] == 'end':
			try:
				sub = tokens
				tokens = stack.pop()
				if tokens:
					tokens[-1][2] = sub
				level -= 1
			except:
				print( "Tokenizer error at or before line %d" % lineNo )
				print( line )
				dummy = stack.pop()
		elif lineSplit[-1] == ';':
			if lineSplit[0] == '\\':
				key = lineSplit[1]
				tokens.append([key,lineSplit[2:-1],[]])
			else:
				key = lineSplit[0]
				tokens.append([key,lineSplit[1:-1],[]])
		else:
			key = lineSplit[0]
			tokens.append([key,lineSplit[1:],[]])
			stack.append(tokens)
			level += 1
			tokens = []
	fp.close()

	if level != 0:
		raise NameError("Tokenizer out of kilter %d" % level)	
	return tokens

#
#	findKey(fkey, tokens):
#	findKeyValue(fkey, args, nCheck, tokens, addr):
#

def findKey(fkey, tokens):
	if tokens == [] or tokens == None:
		return (None, None)
	for (key, val, sub) in tokens:
		if fkey == key:
			return (val, sub)
	return (None, None)

def findKeyValue(fkey, args, nCheck, tokens, addr):
	if tokens == [] or tokens == None:
		#print("No tokens", addr, fkey, args)
		return None
	for (key, val, sub) in tokens:
		if fkey == key:
			if nCheck == 0:
				return sub
			elif nCheck == 1 and val[0] == args[0]:
				return sub
			elif val[0] == args[0] and val[1] == args[1]:
				return sub
	#print("No find", addr, fkey, args)
	return None

def notFound(fp, tokens, addr):
	global nDiffs
	if tokens == None:
		fp.write("Not found: ")
		printAddr(fp, addr)
		fp.write("\n")
		nDiffs += 1
		return True
	return False
#
#
#
			
def diffMhx(fp, tokens1, tokens2):
	for (key1, val1, sub1) in tokens1:
		if key1 == 'Armature':
			print(val1)
			sub2 = findKeyValue('Armature', val1, 1, tokens2, "Arm")
			diffBones(fp, sub1, sub2, ["Arm"])

	for (key1, val1, sub1) in tokens1:
		if key1 == 'Pose':
			print(val1)
			sub2 = findKeyValue('Pose', val1, 1, tokens2, "Pose")
			diffPoseBones(fp, sub1, sub2, ["Pos"])

	for (key1, val1, sub1) in tokens1:
		if key1 == 'Object':
			print(val1)
			sub2 = findKeyValue('Object', val1, 1, tokens2, "Arm")
			diffObject(fp, sub1, sub2, ["Fcu"])

	return

#
#	diffObject(fp, tokens1, tokens2, addr):
#	diffAData(fp, tokens1, tokens2, addr):
#	diffFCurve(fp, tokens1, tokens2, addr):
#	diffDriver(fp, tokens1, tokens2, addr):
#	diffDriverVariable(fp, tokens1, tokens2, addr):
#	diffTarget(fp, tokens1, tokens2, addr):
#
#

def diffObject(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'AnimationData':
			sub2 = findKeyValue('AnimationData', val1, 0, tokens2, addr)			
			diffAData(fp, sub1, sub2, addr+[val1])
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[val1])

def diffAData(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'FCurve':
			sub2 = findKeyValue('FCurve', val1, 2, tokens2, addr)			
			diffFCurve(fp, sub1, sub2, addr+[val1])
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[val1])

def diffFCurve(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'Driver':
			sub2 = findKeyValue('Driver', val1, 0, tokens2, addr)			
			diffDriver(fp, sub1, sub2, addr+[val1])
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[val1])

def diffDriver(fp, tokens1, tokens2, addr):
	for (key1, val1, sub1) in tokens1:
		if key1 == 'DriverVariable':
			sub2 = findKeyValue('DriverVariable', val1, 1, tokens2, addr)			
			diffDriverVariable(fp, sub1, sub2, addr+[val1])
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[val1])

def diffDriverVariable(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'Target':
			sub2 = findKeyValue('Target', val1, 0, tokens2, addr)			
			listDiff(fp, sub1, sub2, addr+[val1])
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[val1])



#
#	diffBones(fp, tokens1, tokens2, addr):
#	diffBone(fp, tokens1, tokens2, addr):
#

def diffBones(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'Bone':
			sub2 = findKeyValue('Bone', val1, 1, tokens2, addr)			
			diffBone(fp, sub1, sub2, addr+[val1])
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[val1])

def diffBone(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'layer' or key1 == 'head' or key1 == 'tail' or key1 == 'roll' or key1 == 'restrict_select':
			pass
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[key1])

#
#	diffPoseBones(fp, tokens1, tokens2, addr):
#	diffPoseBone(fp, tokens1, tokens2, addr):
#

def diffPoseBones(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'Posebone':
			sub2 = findKeyValue('Posebone', val1, 1, tokens2, addr)
			diffPoseBone(fp, sub1, sub2, addr+[val1])
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[key1])

def diffPoseBone(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'Constraint':
			sub2 = findKeyValue('Constraint', val1, 1, tokens2, addr)
			listDiff(fp, sub1, sub2, addr+[val1])
		elif key1 == 'Property':
			pass
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[key1])

#
#	listDiff(fp, tokens1, tokens2, addr):
#	compareValues(fp, args1, args2, addr):
#	diffValue(arg1, arg2):
#

def listDiff(fp, tokens1, tokens2, addr):
	if notFound(fp, tokens2, addr): return
	for (key1, val1, sub1) in tokens1:
		if key1 == 'original_length':
			pass
		else:
			(val2, sub2) = findKey(key1, tokens2)
			compareValues(fp, val1, val2, addr+[key1])

def compareValues(fp, args1, args2, addr):
	global nDiffs

	diff = False
	try:
		if len(args1) != len(args2):
			diff = True
	except:
		diff = True

	if not diff:
		n = 0
		for arg1 in args1:
			diff |= diffValue(arg1, args2[n])
			n += 1

	if not diff:
		return

	printAddr(fp, addr)
	fp.write(" %s != %s\n" % (args1, args2))
	nDiffs += 1
	return

def printAddr(fp, addr):
	for x in addr:
		try:
			if type(x) == str:
				fp.write("%s." % x)
			else:
				fp.write("%s." % x[0])
		except:		
			fp.write("%s." % x)

def diffValue(arg1, arg2):
	if arg1 == arg2:
		return False
	try:
		val1 = eval(arg1)
		val2 = eval(arg2)
	except:
		print("No eval", arg1, arg2)
		return True

	if val1 == val2:
		return False
	elif type(val1) == float and type(val2) == float:
		diff = abs(val1 - val2)
		if diff < 0.01:
			return False
	return True

#
#	mhxDiff(filename1, filename2):
#

def mhxDiff(filename1, filename2):
	global theDir, nDiffs
	tokens1 = tokenizeMhxFile(filename1)
	tokens2 = tokenizeMhxFile(filename2)
	nDiffs = 0
	fp = open(theDir + 'diff.txt', 'w')
	diffMhx(fp, tokens1, tokens2)
	fp.close()
	print("Diffs", nDiffs)
	return
#
#
#

theDir = '/home/thomas/myblends/sintel/'
mhxDiff(theDir+'simple1.mhx', theDir+'simple2.mhx')
#mhxDiff(theDir+'simple1.mhx', '/home/thomas/makehuman/exports/foo-sintel-25.mhx')

