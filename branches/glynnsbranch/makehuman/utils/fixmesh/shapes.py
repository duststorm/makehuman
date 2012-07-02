#
#	shapes.py
#
#	import or export all .vgroup files in the target directory.
#
#	Edit the directories at the top and the chosen command at the bottom.
#
#	But first import the obj file and rename the mesh "Human"
#



import Blender
from Blender import *
from Blender.Mathutils import *
import os

#MHDir = "/home/thomas/svn/makehuman/makehuman/"
MHDir = "/home/svn/"
OldDir = MHDir+"data/targets/shapes/"
NewDir = MHDir+"utils/fixmesh/data/new/targets/shapes/"
Epsilon = 1e-6

def exportVertgroups(me):
	vertgroups = me.getVertGroupNames()
	for g in vertgroups:
		fp = open(OldDir + g + ".vgroup", "w")
		vgroup = me.getVertsFromGroup(g, True)
		for (v, w) in vgroup:
			fp.write("%d %f \n" % (v, w) )
		fp.close()

def exportShapes(me):
	if me.key:
		if me.key.relative == False:
			Draw.Pupmenu("Keys should be relative")
		blocks = me.key.blocks
		for b in blocks:
			fp = open(OldDir + b.name + ".target", "w")
			for (n,v) in enumerate(b.data):
				dv = v - me.verts[n].co
				if dv.length > Epsilon:
					fp.write("%d %f %f %f \n" %(n, dv[0], dv[1], dv[2]))
			fp.close()

def exportAll():
	ob = Object.Get("Human")
	me = ob.getData(False, True)
	exportVertgroups(me)
	exportShapes(me)

def importShape(name, me, ob):
	fp = open(NewDir + name + ".target", "r")
	print "parsing shape ", name
	ob.insertShapeKey()
	me.key.relative = True
	block = me.key.blocks[-1]
	block.name = name
	for line in fp: 
		val= line.split()
		if len(val) == 0:
			return
		index = int(val[0])
		block.data[index] += Vector(float(val[1]), float(val[2]), float(val[3]))
	fp.close()

def importVertGroup(grp, me):
	fp = open(NewDir + grp + ".vgroup", "r")
	print "parsing group ", grp
	me.addVertGroup(grp)
	for line in fp: 
		val= line.split()
		if len(val) == 0:
			return
		me.assignVertsToGroup(grp, [int(val[0])], float(val[1]), Mesh.AssignModes.REPLACE)
	fp.close()

def importAll():
	ob = Object.Get("Human")
	me = ob.getData(False, True)
	importShape('Basis', me, ob)
	for path in os.listdir(NewDir):
		(name, ext) = os.path.splitext(path)
		if ext == '.target':
			if name != 'Basis':
				importShape(name, me, ob)
		elif ext == '.vgroup':
			importVertGroup(name, me)
		else:
			print "What? ", name, ext


print "Starting"
#exportAll()
importAll()
print "Done"