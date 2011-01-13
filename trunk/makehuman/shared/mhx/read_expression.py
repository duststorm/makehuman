""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------


TO DO

"""

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


			



