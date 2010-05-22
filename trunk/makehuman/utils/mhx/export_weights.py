""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Utility for exporting vertex groups from Blender 2.5

"""

import bpy
import os

def exportVertexGroups(filePath):
	fileName = os.path.expanduser(filePath)
	fp = open(fileName, "w")
	ob = bpy.context.object
	me = ob.data
	for vg in ob.vertex_groups:
		index = vg.index
		weights = []
		for v in me.verts:
			for grp in v.groups:
				if grp.group == index and grp.weight > 0.00005:
					weights.append((v.index, grp.weight))

		if len(weights) > 0:
			fp.write("\n# weights %s\n" % vg.name)
			for (vn,w) in weights:
				fp.write("  %d %.4g\n" % (vn, w))
	fp.close()
	return

exportVertexGroups('~/vgroups.txt')

