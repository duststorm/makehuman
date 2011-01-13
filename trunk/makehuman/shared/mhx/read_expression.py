
import os

Expressions = [
	'smile',
	'hopefull',
	'innocent',
	'tender',
	'seductive',

	'grin',
	'excited',
	'ecstatic',

	'proud',
	'pleased',
	'amused',
	'laughing1',
	'laughing2',

	'so-so',
	'blue',
	'depressed',
	'sad',
	'distressed',
	'crying',
	'pain',

	'disappointed',
	'frustrated',
	'stressed',
	'worried',
	'scared',
	'terrified',

	'shy',
	'guilty',
	'embarassed',
	'relaxed',
	'peaceful',
	'refreshed',

	'lazy',
	'bored',
	'tired',
	'drained',
	'sleepy',
	'groggy',

	'curious',
	'surprised',
	'imporessed',
	'puzzled',
	'shocked',
	'frown',
	'upset',
	'angry',
	'enraged',

	'skeptical',
	'vindictive',
	'pout',
	'furious',
	'grumpy',
	'arrogant',
	'sneering',
	'haughty',
	'disgusted',
]

def readExpressions():
	exprList = []
	for name in Expressions:
		filename = 'data/targets/expression/female_young/neutral_female_young_%s.target' % name
		try:
			fp = open(filename, "rU")
		except:
			print("Cannot open %s" % filename)
			fp = 0

		if fp:
			expr = []
			for line in fp:
				words = line.split()
				expr.append((int(words[0]), float(words[1]), -float(words[3]), float(words[2])))
			fp.close()
			exprList.append((name, expr))
			print("%s copied" % filename)
	return exprList


			



