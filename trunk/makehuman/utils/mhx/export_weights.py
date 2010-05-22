import bpy

def exportVertexGroups(fileName):
	fp = open(fileName, "w")
	ob = bpy.context.object
	me = ob.data
	for vg in ob.vertex_groups:
		index = vg.index
		fp.write("# weights %s\n" % vg.name)
		for v in me.verts:
			for grp in v.groups:
				if grp.group == index and grp.weight > 0.00005:
					fp.write("  %d %.4g\n" % (v.index, grp.weight))
	fp.close()
	return

exportVertexGroups('/home/thomas/myblends/vgroups.txt')

